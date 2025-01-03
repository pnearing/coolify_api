import logging
import os
from typing import Optional, Any
from requests.models import Response

from ._logging import OUTPUT_IS_SHY


class CoolifyAPIError(Exception):
    """Base class for other Coolify API exceptions."""
    def __init__(self, message: str, *args, **kw_args) -> None:
        self.message: str = message
        super().__init__(message, *args, **kw_args)


class CoolifyAPIValidationError(CoolifyAPIError):
    """Exception raised for when the Coolify API responds with a 'validation failed' error."""
    def __init__(self, response):
        error_data = response.json()
        message = f"Coolify API Error: {error_data['message']}"
        if isinstance(error_data, dict):
            if isinstance(error_data['errors'], list):
                message = ", ".join(error_data['errors'])
            elif isinstance(error_data['errors'], str):
                message = error_data['errors']
            elif isinstance(error_data['errors'], dict):
                for key, value in error_data['errors'].items():
                    message += f"\n\t{key}: {value}"
        elif isinstance(error_data, list):
            for item in error_data:
                message += f"\n\t{item}"
        super().__init__(message)
        self.error_data = error_data
        self.response = response


class CoolifyAPIResponseError(CoolifyAPIError):
    """Exception raised for when the Coolify API responds with an error."""

    def __init__(self,
                 url: str,
                 headers: dict,
                 data: Optional[dict] = None,
                 response: Optional[Response] = None,
                 message_start: str = "Coolify API Error",
                 *args, **kw_args) -> None:
        # Store the args:
        self.url: str = url
        self.headers: dict = headers
        self.response: Response = response
        self.data: Optional[dict] = data
        self._kwargs: Optional[dict] = kw_args

        message = (f"\n{message_start}: \n",
                   f"\tUrl: {url},\n"
                   f"\tRecv Status Code: {response.status_code}")
        if not OUTPUT_IS_SHY:
            message += (f",\n",
                        f"\tSent Headers: {headers},\n",
                        f"\tSent Data: {data},\n",
                        f"\tRecv Response: {response.text}\n")
        # Init super:
        super().__init__(message, url, response, data, *args)


class CoolifyAuthenticationError(CoolifyAPIResponseError):
    """Exception raised for authentication errors in the Coolify API."""
    def __init__(self, *args, **kw_args) -> None:
        message = "Coolify Authentication Error, invalid bearer token."
        super().__init__(message, *args, **kw_args)


class CoolifyKeyUnknownError(CoolifyAPIError):
    """Exception raised when a key is not found in the known keys."""
    def __init__(self, key_name: str, *args, **kw_args) -> None:
        message = f"Coolify API Error, key '{key_name}' not found in known keys."
        super().__init__(message, *args, **kw_args)


class CoolifyKeyRequiredError(CoolifyAPIError):
    """Exception raised for required key errors in the Coolify API."""
    def __init__(self, key_name: str, *args, **kw_args) -> None:
        message = f"Coolify API Error, required key '{key_name}' not found."
        super().__init__(message, *args, **kw_args)


class CoolifyKeyValueTypeError(CoolifyAPIError):
    """Exception raised for key value type errors in the Coolify API."""
    def __init__(self, key_name: str, value: Any, key_type: type, *args, **kw_args) -> None:
        message = (f"Coolify API Error, key '{key_name}' has invalid type '{str(type(value))}', "
                   f"expected type '{str(key_type)}'.")
        super().__init__(message, *args, **kw_args)


class CoolifyKeyValueError(CoolifyAPIError):
    """Exception raised for key value errors in the Coolify API."""
    def __init__(self, key_name: str, value: Any, allowed: list[Any], *args, **kw_args) -> None:
        message = (f"Coolify API Error, key '{key_name}' has invalid value '{value}'."
                   f" Allowed values: {allowed}")
        super().__init__(message, *args, **kw_args)


class RequestsError(Exception):
    """Exception raised for errors that occur when making requests to Coolify API."""
    def __init__(self,
                 url: str,
                 headers: dict,
                 data: Optional[dict] = None,
                 exception: Exception = None,
                 *args, **kw_args) -> None:

        # Store the properties:
        self.url: str = url
        self.headers: dict = headers
        self.data: Optional[dict] = data
        self.requests_exception: Exception = exception
        self._kwargs: Optional[dict] = kw_args

        # Create the message:
        message = (f"\nError while making request:\n"
                   f"  Target Url: {url},"
                   f"  Got Exception type: {str(type(exception))}")
        if not OUTPUT_IS_SHY:
            message += (f",\n",
                        f"  Sent Headers: {headers},\n"
                        f"  Sent Data: {data},\n",
                        f"  Recv Exception: {exception}\n")
        super().__init__(message, url, headers, data, exception, *args)
