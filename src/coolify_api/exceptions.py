"""Coolify API exception classes.

This module provides custom exception classes for handling various error conditions
that may occur when interacting with the Coolify API.

Example:
    ```python
    from coolify_api import CoolifyAPIClient
    from coolify_api.exceptions import CoolifyAuthenticationError, CoolifyValidationError

    client = CoolifyAPIClient()

    try:
        client.applications.get("invalid-uuid")
    except CoolifyValidationError as e:
        print(f"Validation failed: {e.message}")
    except CoolifyAuthenticationError as e:
        print(f"Authentication failed: {e.message}")
    ```
"""

from requests.models import Response
from aiohttp import ClientResponse


class CoolifyError(Exception):
    """Base class for Coolify API exceptions.

    All custom exceptions in this module inherit from this class, allowing for
    catch-all error handling of Coolify-specific errors.

    Attributes:
        message: Human-readable error description
    """
    def __init__(self, message: str, *args, **kw_args) -> None:
        """Initialize base error.

        Args:
            message: Error description
            *args: Additional positional arguments for Exception class
            **kw_args: Additional attributes to add to the exception
        """
        self.message: str = message
        self.__dict__.update(kw_args)
        super().__init__(message, *args)


class CoolifyAuthenticationError(CoolifyError):
    """Exception raised when authentication with the Coolify API fails.

    This can occur due to invalid API keys, expired tokens, or missing credentials.

    Attributes:
        message: Error description including the API response
        headers: Response headers that may contain auth-related information
    """
    def __init__(self, response: Response | ClientResponse, headers, *args, **kw_args) -> None:
        """Initialize authentication error.

        Args:
            response: HTTP response that triggered the error
            headers: Response headers
            *args: Additional positional arguments
            **kw_args: Additional keyword arguments
        """
        message = f"Coolify Authentication Error: {response.text}"
        super().__init__(message, *args, headers=headers, **kw_args)


class CoolifyPermissionError(CoolifyError):
    """Exception raised when the API request lacks required permissions.

    This occurs when trying to access resources or perform operations that require
    higher privilege levels than the current user has.

    Attributes:
        message: Error description including the API response
        headers: Response headers that may contain permission-related information
    """
    def __init__(self, response: Response | ClientResponse, headers, *args, **kw_args) -> None:
        """Initialize permission error.

        Args:
            response: HTTP response that triggered the error
            headers: Response headers
            *args: Additional positional arguments
            **kw_args: Additional keyword arguments
        """
        message = f"Coolify Permission Error: {response.text}"
        super().__init__(message, *args, headers=headers, **kw_args)


class CoolifyNotFoundError(CoolifyError):
    """Exception raised when a requested resource is not found.

    This occurs when trying to access a specific resource (like an application,
    database, or deployment) using an ID or UUID that doesn't exist.

    Attributes:
        message: Error description including the resource type and identifier
        resource_type: Type of resource that wasn't found (e.g., "application", "database")
        resource_id: Identifier that was used in the request
    """
    def __init__(self, response: Response | ClientResponse, *args, **kwargs) -> None:
        """Initialize not found error.

        Args:
            response: HTTP response that triggered the error
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        """
        message = f"Coolify Resource Not Found: {response.url}"
        if response.text:
            message += f" - {response.text}"
        super().__init__(message, *args, response=response, **kwargs)


class CoolifyValidationError(CoolifyError):
    """Exception raised when the API request fails validation.

    This occurs when the request contains invalid data, missing required fields,
    or violates API constraints. The error message includes detailed validation
    failures from the API response.

    Attributes:
        message: Formatted error description with validation details
        response: Full API response for additional error context
    """
    def __init__(self, message: str, *args, response=None, **kwargs):
        """
        Initialize validation error with a pre-built message.
        Use the async classmethod 'from_response' to construct this exception from an HTTP response.
        """
        super().__init__(message, *args, response=response, **kwargs)

    @classmethod
    async def from_response(cls, response: Response | ClientResponse, *args, **kwargs):
        """
        Asynchronously create a CoolifyValidationError from a response object.
        Use this in async code to ensure coroutines are awaited.
        """
        import inspect
        if hasattr(response, "json") and inspect.iscoroutinefunction(response.json):
            error_data = await response.json()
        else:
            error_data = response.json()
        message = "Coolify Validation Error:"
        if isinstance(error_data, dict):
            message += f" {error_data.get('message', '')}"
            if isinstance(error_data.get('errors'), list):
                message = ", ".join(error_data['errors'])
            elif isinstance(error_data.get('errors'), str):
                message = error_data['errors']
            elif isinstance(error_data.get('errors'), dict):
                for key, value in error_data['errors'].items():
                    message += f"\n\t{key}: {value}"
        elif isinstance(error_data, list):
            for item in error_data:
                message += f"\n\t{item}"
        return cls(message, *args, response=response, **kwargs)

    @classmethod
    def from_response_sync(cls, response: Response | ClientResponse, *args, **kwargs):
        """
        Synchronously create a CoolifyValidationError from a response object.
        Use this in sync code.
        """
        error_data = response.json()
        message = "Coolify Validation Error:"
        if isinstance(error_data, dict):
            message += f" {error_data.get('message', '')}"
            if isinstance(error_data.get('errors'), list):
                message = ", ".join(error_data['errors'])
            elif isinstance(error_data.get('errors'), str):
                message = error_data['errors']
            elif isinstance(error_data.get('errors'), dict):
                for key, value in error_data['errors'].items():
                    message += f"\n\t{key}: {value}"
        elif isinstance(error_data, list):
            for item in error_data:
                message += f"\n\t{item}"
        return cls(message, *args, response=response, **kwargs)
