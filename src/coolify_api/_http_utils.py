"""HTTP utilities for the Coolify API client.

This module provides core HTTP functionality for interacting with the Coolify API, including:
- Request handling (sync and async)
- Rate limiting
- Response processing
- Error handling

The module supports both synchronous and asynchronous operations, automatically detecting the
appropriate mode based on the execution context.

Environment Variables:
    REQUESTS_PER_SECOND (int): Maximum requests per second (default: 4)
    REQUESTS_TIMEOUT (int): Request timeout in seconds (default: 10)
"""
import asyncio
from logging import getLogger, DEBUG, INFO, WARNING, ERROR
import os
import time
from typing import Any, Optional, Coroutine

import aiohttp
from aiohttp import ClientResponse, ClientError
import requests
from requests.models import Response

from ._logging import _log_message
from .exceptions import CoolifyError, CoolifyNotFoundError, CoolifyPermissionError, \
    CoolifyValidationError, CoolifyAuthenticationError, CoolifyRateLimitError


######################
# URL building:
def _build_v1_url(base_url: str, endpoint: str) -> str:
    """Build a v1 API URL from base URL and endpoint.

    Args:
        base_url: Base URL of the Coolify instance
        endpoint: API endpoint to append

    Returns:
        Complete URL for the v1 API endpoint
    """
    return f"{base_url}/api/v1/{endpoint}"


def _build_url(base_url: str, endpoint: str, version: str = "v1") -> str:
    """Build a complete API URL with version.

    Args:
        base_url: Base URL of the Coolify instance
        endpoint: API endpoint to append
        version: API version (only "v1" supported)

    Returns:
        Complete URL for the API endpoint

    Raises:
        ValueError: If version is not "v1"
    """
    if version != "v1":
        raise ValueError("Only API version 'v1' is currently supported")
    return _build_v1_url(base_url, endpoint)


class HTTPUtils:
    """Utility class for making HTTP requests with rate-limiting and error-handling.

    This class provides functionality for both synchronous and asynchronous HTTP
    operations with support for rate-limiting and response handling. It allows
    sending GET, POST, PATCH, and DELETE requests to the specified endpoints
    efficiently while managing API limits and exceptions.

    Attributes:
        _requests_per_second (float): Maximum requests per second (default: 4.0, supports fractional values)
        _timeout (int): Request timeout in seconds (default: 10)
        _last_request_time (float): Timestamp of last request for rate limiting
        _logger: Logger instance for this class
        _async (Optional[bool]): Whether class operates in async mode
        _base_url (str): Base URL for API requests
        _headers (dict): Headers to include in requests
        _session (Optional[aiohttp.ClientSession]): Async session for requests

    Args:
        base_url: Base URL for the API
        headers: Headers to be sent with each request
    """
    _requests_per_second: float = float(os.getenv("REQUESTS_PER_SECOND", "3.3"))
    _timeout: int = int(os.getenv("REQUESTS_TIMEOUT", "10"))
    _last_request_time: float = time.time() - 1
    _logger = getLogger(__name__)

    def __init__(self, base_url: str, headers: dict[str, str], async_mode: Optional[bool] = None) -> None:
        """Initialize HTTP utilities with base URL and headers.

        Automatically detects whether to use async or sync mode based on the current
        execution context.

        Args:
            base_url: Base URL for API requests
            headers: Headers to include in all requests
            async_mode: Whether to use async mode
    """
        self._base_url = base_url
        """Base URL for the class."""
        self._headers = headers
        """Headers for the class."""
        self._session: Optional[aiohttp.ClientSession] = None
        """Asyncio session for making HTTP requests."""
        self._override_async_mode: Optional[bool] = async_mode
        
    def detect_async_mode(self) -> bool:
        """Detect whether to use async or sync mode based on the current execution context."""
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False

    @property
    def _do_async(self) -> bool:
        if self._override_async_mode is not None:
            return self._override_async_mode
        return self.detect_async_mode()

    @classmethod
    async def _a_rate_limit(cls) -> bool:
        """Apply rate limiting for async requests.

        Ensures requests don't exceed the configured rate limit by introducing delays
        when necessary.

        Returns:
            bool: True if rate limiting was applied, False otherwise
        """
        limited: bool = False
        current_time: float = time.time()
        interval: float = 1 / cls._requests_per_second
        if current_time - cls._last_request_time < interval:
            limited = True
            sleep_time = interval - (current_time - cls._last_request_time)
            message = f"Rate limiting applied. Sleeping for {sleep_time} seconds."
            _log_message(cls._logger, WARNING, message)
            await asyncio.sleep(sleep_time)
        return limited


    @classmethod
    def _s_rate_limit(cls) -> bool:
        """Apply rate limiting for synchronous requests.

        Ensures requests don't exceed the configured rate limit by introducing delays
        when necessary.

        Returns:
            bool: True if rate limiting was applied, False otherwise
        """
        limited: bool = False
        current_time: float = time.time()
        interval: float = 1 / cls._requests_per_second
        if current_time - cls._last_request_time < interval:
            limited = True
            sleep_time = interval - (current_time - cls._last_request_time)
            message = f"Rate limiting applied. Sleeping for {sleep_time} seconds."
            _log_message(cls._logger, WARNING, message)
            time.sleep(sleep_time)
        return limited

    
    @classmethod
    async def _handle_response_async(cls,
                                    http_method: str,
                                    params: Optional[dict[str, str]],
                                    headers: dict,
                                    data: Optional[Any],
                                    response: ClientResponse,
                                    ) -> Any:
        # Gather the data:
        status_code = response.status
        log_level: int = ERROR
        return_value: Any = None
        error_to_raise: Optional[Exception] = None

        if 200 <= status_code < 300:
            log_level = INFO
            return_value = await response.json()
        elif 300 <= status_code < 400:
            log_level = WARNING
            error_message = f"Unhandled 3xx error: {status_code} - {response.text} - we shouldn't be redirecting."
            _log_message(cls._logger, DEBUG, error_message)
            error_to_raise = CoolifyError(error_message, response=response)
        elif 400 <= status_code < 500:
            if status_code == 400:
                error_message = f"UNSEEN 400 error - {response.text}"
                _log_message(cls._logger, DEBUG, error_message)
                error_to_raise = CoolifyError(error_message, response=response, data=data)
            elif status_code == 401:
                error_to_raise = CoolifyAuthenticationError(response=response, headers=headers)
            elif status_code == 403:
                error_to_raise = CoolifyPermissionError(response=response, headers=headers)
            elif status_code == 404:
                error_to_raise = CoolifyNotFoundError(response=response, headers=headers)
            elif status_code == 422:
                error_to_raise = await CoolifyValidationError.from_response_async(response=response, data=data)
            elif status_code == 429:
                error_to_raise = CoolifyRateLimitError(response=response, headers=headers)
            else:
                error_message = f"Unhandled 4xx error: {status_code} - {response.text} - please report this to maintainer."
                _log_message(cls._logger, DEBUG, error_message)
                error_to_raise = CoolifyError(error_message, response=response, data=data)
        else:
            error_message = f"Unhandled >= 500 error: {status_code} - {response.text}"
            error_to_raise = CoolifyError(error_message, response=response)

        # Log and raise / return:
        message: str = (f"CoolifyAPI: '{http_method}' operation on '{response.url}', "
                        f"with params: '{params}', responded with Status Code: '{status_code}:'")
        hidden_message: str = f"\n  Sent headers: {headers}\n"
        if data:
            hidden_message += f"  Sent data: {data}\n"
        _log_message(cls._logger, log_level, message, hidden_message)
        if error_to_raise:
            raise error_to_raise from None
        return return_value
    

    @classmethod
    def _handle_response_sync(cls,
                         http_method: str,
                         params: Optional[dict[str, str]],
                         headers: dict,
                         data: Optional[Any],
                         response: Response,
                         ) -> Any:
        """Process HTTP response and handle any errors.

        Args:
            http_method: HTTP method used (GET, POST, etc.)
            params: Query parameters sent with request
            headers: Headers sent with request
            data: Request body data
            response: Response from server

        Returns:
            Processed response data (usually JSON)

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: For authentication failures
            CoolifyValidationError: For validation errors
        """
        # Gather the data:
        status_code = response.status_code
        log_level: int = ERROR
        return_value: Any = None
        error_to_raise: Optional[Exception] = None

        if 200 <= status_code < 300:
            log_level = INFO
            return_value = response.json()
        elif 300 <= status_code < 400:
            log_level = WARNING
            error_message = f"Unhandled 3xx error: {status_code} - {response.text} - we shouldn't be redirecting."
            _log_message(cls._logger, DEBUG, error_message)
            error_to_raise = CoolifyError(error_message, response=response)
        elif 400 <= status_code < 500:
            if status_code == 400:
                error_message = f"UNSEEN 400 error - {response.text}"
                _log_message(cls._logger, DEBUG, error_message)
                error_to_raise = CoolifyError(error_message, response=response, data=data)
            elif status_code == 401:
                error_to_raise = CoolifyAuthenticationError(response=response, headers=headers)
            elif status_code == 403:
                error_to_raise = CoolifyPermissionError(response=response, headers=headers)
            elif status_code == 404:
                error_to_raise = CoolifyNotFoundError(response=response, headers=headers)
            elif status_code == 422:
                error_to_raise = CoolifyValidationError.from_response_sync(response=response, data=data)
            else:
                error_message = f"Unhandled 4xx error: {status_code} - {response.text} - please report this to maintainer."
                _log_message(cls._logger, DEBUG, error_message)
                error_to_raise = CoolifyError(error_message, response=response, data=data)
        else:
            error_message = f"Unhandled >= 500 error: {status_code} - {response.text}"
            error_to_raise = CoolifyError(error_message, response=response)

        # Log and raise / return:
        message: str = (f"CoolifyAPI: '{http_method}' operation on '{response.url}', "
                        f"with params: '{params}', responded with Status Code: '{status_code}:'")
        hidden_message: str = f"\n  Sent headers: {headers}\n"
        if data:
            hidden_message += f"  Sent data: {data}\n"
        _log_message(cls._logger, log_level, message, hidden_message)
        if error_to_raise:
            raise error_to_raise from None
        return return_value


    def do_sync_op(self, op: str, url: str, params: Optional[dict[str, str]] = None,
                   data: Any = None) -> Any:
        """Execute a synchronous HTTP operation.

        Args:
            op: HTTP method to use
            url: URL to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Processed response data

        Raises:
            requests.RequestException: If request fails
        """
        _log_message(self._logger, DEBUG, f"Starting {op} request to {url}")
        try:
            self._s_rate_limit()
            response = requests.request(op, url, params=params, headers=self._headers, json=data,
                                        timeout=self._timeout)
        except requests.RequestException as e:
            _log_message(self._logger, ERROR, f"Error sending {op} request to {url}: {e}")
            raise e
        _log_message(self._logger, DEBUG, f"Finished {op} request to {url}")
        return self._handle_response_sync(op, params, self._headers, data, response)


    async def do_async_op(self, op: str, url: str, params: Optional[dict[str, str]] = None,
                          data: Any = None) -> Any:
        """Execute an asynchronous HTTP operation.

        Args:
            op: HTTP method to use
            url: URL to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Processed response data

        Raises:
            ClientError: If request fails
        """
        if self._session is None:
            self._session = aiohttp.ClientSession(headers=self._headers)
        
        _log_message(self._logger, DEBUG, f"Starting {op} request to {url}")
        await self._a_rate_limit()
        try:
            async with self._session.request(op, url, params=params, headers=self._headers,
                                             json=data) as response:
                _log_message(self._logger, DEBUG, f"Finished {op} request to {url}")
                return await self._handle_response_async(op, params, self._headers, None, response)
        except ClientError as exc:
            _log_message(self._logger, ERROR,f"Error sending {op} request to {url}: {exc}")
            raise exc


    ##############
    # GET:
    def get(self, endpoint: str, params: Optional[dict[str, str]] = None
            ) -> Any | Coroutine[Any, Any, Any]:
        """Send GET request to specified endpoint.

        Args:
            endpoint: API endpoint to send request to
            params: Optional query parameters

        Returns:
            Response data (or Coroutine in async mode)

        Raises:
            RuntimeError: If class not properly initialized
        """
        url = _build_url(self._base_url, endpoint)
        _log_message(self._logger, DEBUG, f"Starting GET request to {url}")
        if self._do_async:
            return self.do_async_op("GET", url, params)
        return self.do_sync_op("GET", url, params)

    #####################
    # POST:
    def post(self, endpoint: str, params: Optional[dict] = None, data: Any = None
             ) -> Any | Coroutine[Any, Any, Any]:
        """Send POST request to specified endpoint.

        Args:
            endpoint: API endpoint to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Response data (or Coroutine in async mode)

        Raises:
            RuntimeError: If class not properly initialized
        """
        url = _build_url(self._base_url, endpoint)
        _log_message(self._logger, DEBUG, f"Starting POST request to {url}")
        if self._do_async:
            return self.do_async_op("POST", url, params, data)
        return self.do_sync_op("POST", url, params, data)

    #####################
    # PATCH:
    def patch(self, endpoint: str, params: Optional[dict] = None, data: Any = None
              ) -> Any | Coroutine[Any, Any, Any]:
        """Send PATCH request to specified endpoint.

        Args:
            endpoint: API endpoint to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Response data (or Coroutine in async mode)

        Raises:
            RuntimeError: If class not properly initialized
        """
        url = _build_url(self._base_url, endpoint)
        _log_message(self._logger, DEBUG, f"Starting PATCH request to {url}")
        if self._do_async:
            return self.do_async_op("PATCH", url, params, data)
        return self.do_sync_op("PATCH", url, params, data)

    #####################
    # DELETE:
    def delete(self, endpoint: str, params: Optional[dict] = None, data: Any = None
               ) -> Any | Coroutine[Any, Any, Any]:
        """Send DELETE request to specified endpoint.

        Args:
            endpoint: API endpoint to send request to
            params: Optional query parameters

        Returns:
            Response data (or Coroutine in async mode)

        Raises:
            RuntimeError: If class not properly initialized
        """
        url = _build_url(self._base_url, endpoint)
        _log_message(self._logger, DEBUG, f"Starting DELETE request to {url}")
        if self._do_async:
            return self.do_async_op("DELETE", url, params, data)
        return self.do_sync_op("DELETE", url, params, data)
