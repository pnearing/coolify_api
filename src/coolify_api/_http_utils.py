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
from typing import Any, NoReturn, Optional, Coroutine, Tuple

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
        self._override_async_mode: Optional[bool] = async_mode
        """Override async mode."""
        
    def _detect_async_mode(self) -> bool:
        """Detect whether to use async or sync mode based on the current execution context."""
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False

    @property
    def _do_async(self) -> bool:
        """Whether to use async mode."""
        if self._override_async_mode is not None:
            return self._override_async_mode
        return self._detect_async_mode()

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

    @classmethod # REDIRECTS:
    def _handle_300_response(cls, response: ClientResponse | Response) -> Exception:
        return CoolifyError(f"Unhandled 3xx error: {response.status} - we shouldn't be redirecting.")

    @classmethod # CLIENT ERRORS:
    def _handle_400_response(cls, response: ClientResponse | Response, status_code: int, headers: dict, data: Optional[Any]) -> Exception:
        # NEVER SEEN: 400
        if status_code == 401:
            return CoolifyAuthenticationError(response=response, headers=headers)
        elif status_code == 403:
            return CoolifyPermissionError(response=response, headers=headers)
        elif status_code == 404:
            return CoolifyNotFoundError(response=response, headers=headers)
        elif status_code == 422:
            try:
                return CoolifyValidationError.from_response_async(response=response, data=data)
            except Exception:
                return CoolifyValidationError.from_response_sync(response=response, data=data)
        elif status_code == 429:
            return CoolifyRateLimitError(response=response, headers=headers)
        else:
            return CoolifyError(f"Unhandled 4xx error: {status_code} - please report this to maintainer.")

    @classmethod # SERVER ERRORS:
    def _handle_500_response(cls, response: ClientResponse) -> Exception:
        return CoolifyError(f"Unhandled server error >= 500: {response.status}")

    @classmethod # ALL RESPONSES:
    def _handle_http_status_code(cls, status_code: int, response: ClientResponse | Response, headers: dict, data: Optional[Any]) -> Exception:
        if status_code < 300 or status_code >= 400:
            return cls._handle_300_response(response)
        elif status_code < 400 or status_code >= 500:
            return cls._handle_400_response(response, status_code, headers, data)
        else:
            return cls._handle_500_response(response)


    @classmethod
    async def _handle_response_async(cls,
                                    http_method: str,
                                    params: Optional[dict[str, str]],
                                    headers: dict,
                                    data: Optional[Any],
                                    response: ClientResponse,
                                    ) -> Any:
        """Process HTTP response and handle any errors.

        Args:
            http_method: HTTP method used (GET, POST, etc.)
            params: Query parameters sent with request
            headers: Headers sent with request
            data: Request body data
            response: Response from server

        Returns:
            Processed response data (usually JSON) if request was successful,
            otherwise raises an appropriate exception class.
        """
        _log_message(cls._logger, DEBUG, f"Starting to handle async response for {http_method} request to {response.url}")
        
        # Gather the data:
        status_code = response.status
        # Handle a successful response:
        if 200 <= status_code < 300:
            _log_message(cls._logger, INFO, f"{http_method} request to {response.url} using params {params} succeeded with status code {status_code}", "\n  Sent headers: {headers}\n")
            return await response.json()
        # Handle a failed response:
        error_to_raise = cls._handle_http_status_code(status_code, response, headers, data)
        _log_message(cls._logger, ERROR, f"{http_method} request to {response.url} using params {params} failed with status code {status_code}", "\n  Sent headers: {headers}\n")
        raise error_to_raise from None
   

    @classmethod
    def _handle_response_sync(cls,
                         http_method: str,
                         params: Optional[dict[str, str]],
                         headers: dict,
                         data: Optional[Any],
                         response: Response,
                         ) -> Any | NoReturn:
        """Process HTTP response and handle any errors.

        Args:
            http_method: HTTP method used (GET, POST, etc.)
            params: Query parameters sent with request
            headers: Headers sent with request
            data: Request body data
            response: Response from server

        Returns:
            Processed response data (JSON) if request was successful,
            otherwise raises an appropriate exception class.
        """
        # Gather the data:
        status_code = response.status_code
        # Handle a successful response:
        if 200 <= status_code < 300:
            _log_message(cls._logger, INFO, f"{http_method} request to {response.url} using params {params} succeeded with status code {status_code}", "\n  Sent headers: {headers}\n")
            return response.json()
        # Handle a failed response:
        error_to_raise = cls._handle_http_status_code(status_code, response, headers, data)
        _log_message(cls._logger, ERROR, f"{http_method} request to {response.url} using params {params} failed with status code {status_code}", "\n  Sent headers: {headers}\n")
        raise error_to_raise from None

    def do_sync_op(self, http_method: str, url: str, params: Optional[dict[str, str]] = None,
                   data: Any = None) -> Any | NoReturn:
        """Execute a synchronous HTTP operation.

        Args:
            http_method: HTTP method to use
            url: URL to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Processed response data (JSON) if request was successful,
            otherwise raises an appropriate exception class.
        """
        _log_message(self._logger, DEBUG, f"Starting {http_method} request to {url} with params {params}", "\n  Sent headers: {self._headers}\n")
        # Apply rate limit:
        self._s_rate_limit()
        _log_message(self._logger, DEBUG, f"Rate limit applied for sync {http_method} request to {url}")
        # Send the request:
        try:
            response: Response = requests.request(http_method, url, params=params, headers=self._headers, json=data,
                                        timeout=self._timeout)
            _log_message(self._logger, DEBUG, f"Finished {http_method} request to {url} with params {params}", "\n  Sent headers: {self._headers}\n")
        except requests.RequestException as e:
            _log_message(self._logger, ERROR, f"Error sending {http_method} request to {url} with params {params}: {e}", "\n  Sent headers: {self._headers}\n")
            raise e
        # Return the response:
        return self._handle_response_sync(http_method, params, self._headers, data, response)


    async def do_async_op(self, http_method: str, url: str, params: Optional[dict[str, str]] = None,
                          data: Any = None) -> Any:
        """Execute an asynchronous HTTP operation.

        Args:
            http_method: HTTP method to use
            url: URL to send request to
            params: Optional query parameters
            data: Optional request body

        Returns:
            Processed response data

        Raises:
            ClientError: If request fails
        """
        _log_message(self._logger, DEBUG, f"Starting async {http_method} request to {url} with params {params}", "\n  Sent headers: {self._headers}\n")
        # Create a new session for each request to avoid "Event loop is closed" errors
        # This is safer than reusing sessions across different event loops
        session = aiohttp.ClientSession(headers=self._headers)
        
        # Apply rate limit:
        await self._a_rate_limit()
        _log_message(self._logger, DEBUG, f"Rate limit applied for async {http_method} request to {url}")

        # Send the request:
        try:
            async with session.request(http_method, url, params=params, headers=self._headers,
                                      json=data) as response:
                _log_message(self._logger, DEBUG, f"Finished async {http_method} request to {url} with params {params}", "\n  Sent headers: {self._headers}\n")
                result = await self._handle_response_async(http_method, params, self._headers, data, response)
        except ClientError as e:
            _log_message(self._logger, ERROR, f"Error sending async {http_method} request to {url} with params {params}: {e}", "\n  Sent headers: {self._headers}\n")
            raise e
        finally:
            # Always close the session when done
            await session.close()
        # Return the response
        return result


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
        if self._do_async:
            return self.do_async_op("DELETE", url, params, data)
        return self.do_sync_op("DELETE", url, params, data)
