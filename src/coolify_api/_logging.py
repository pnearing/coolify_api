"""Logging utilities for the Coolify API client.

This module provides logging functionality with support for sensitive data handling.
It allows logging messages with optional hidden information that can be revealed
based on environment configuration.

Environment Variables:
    OUTPUT_IS_SHY (str): Controls whether sensitive data is hidden in logs.
        Set to "false" to show hidden information. Accepts various truthy/falsy values:
        - True values: "true", "1", "t", "yes", "y", "yup", "sure", "ok", "yep", "yeah", "shy"
        - Any other value is considered False

Example:
    ```python
    from logging import getLogger, DEBUG
    from ._logging import _log_message

    logger = getLogger(__name__)
    
    # Basic logging
    _log_message(logger, DEBUG, "Operation completed")
    
    # Logging with hidden data
    sensitive_data = {"api_key": "secret"}
    _log_message(logger, DEBUG, "API call made", sensitive_data)
    ```
"""
import os
from typing import Any
from logging import Logger

OUTPUT_IS_SHY = os.getenv("OUTPUT_IS_SHY", "true").lower() in ("true", "1", "t", "yes", "y", "yup",
                                                              "sure", "ok", "yep", "yeah", "shy")
"""bool: Global flag controlling visibility of sensitive data in logs."""


def _log_message(logger: Logger, log_level: int, message: str, hidden: Any = None) -> None:
    """Log a message with optional hidden information.

    This function logs messages with support for sensitive data that can be optionally
    hidden based on the OUTPUT_IS_SHY environment variable. When hidden data is provided,
    it's either displayed or replaced with a placeholder message depending on the
    configuration.

    Args:
        logger: Logger instance to use for logging
        log_level: Logging level (e.g., DEBUG, INFO, WARNING, ERROR)
        message: Main message to log
        hidden: Optional sensitive data to include in logs. Will be hidden if
            OUTPUT_IS_SHY is True

    Example:
        ```python
        _log_message(logger, DEBUG, "Request completed", {"sensitive": "data"})
        ```

        With OUTPUT_IS_SHY=true:
        ```
        Request completed
        ----> HIDDEN INFO FOLLOWS: <----
        <INFO HIDDEN, set OUTPUT_IS_SHY=false to see>
        ----> END HIDDEN INFO <----
        ```

        With OUTPUT_IS_SHY=false:
        ```
        Request completed
        ----> HIDDEN INFO FOLLOWS: <----
        {'sensitive': 'data'}
        ----> END HIDDEN INFO <----
        ```
    """
    message = f"{message}"
    if hidden is not None:
        message += "\n----> HIDDEN INFO FOLLOWS: <----\n"
        if OUTPUT_IS_SHY:
            message += "<INFO HIDDEN, set OUTPUT_IS_SHY=false to see>"
        else:
            message += f"{hidden}"
        message += "\n----> END HIDDEN INFO <----\n"
    logger.log(log_level, message)

