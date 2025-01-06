"""Utility functions for the Coolify API client.

This module provides utility functions for data manipulation and validation used across
the Coolify API client library.

Example:
    ```python
    from coolify_api._utils import create_data_with_kwargs

    # Merge existing data with new values
    base_data = {"name": "app1"}
    result = create_data_with_kwargs(base_data, port=8080, env="prod")
    # result = {"name": "app1", "port": 8080, "env": "prod"}

    # Create new data from kwargs only
    result = create_data_with_kwargs(port=8080, env="prod")
    # result = {"port": 8080, "env": "prod"}
    ```
"""
from typing import Optional


def create_data_with_kwargs(data: Optional[dict] = None, **kwargs) -> dict:
    """Create or update a dictionary with additional keyword arguments.

    This utility function merges keyword arguments into an existing dictionary or creates
    a new one. It's commonly used throughout the API client to handle optional parameters
    in a flexible way.

    Args:
        data: Base dictionary to update. If None, a new empty dictionary is created
        **kwargs: Additional key-value pairs to add to the dictionary

    Returns:
        Updated dictionary containing all key-value pairs from both sources

    Example:
        ```python
        # Update existing data
        base = {"name": "app1"}
        result = create_data_with_kwargs(base, port=8080)
        # result = {"name": "app1", "port": 8080}

        # Create new data
        result = create_data_with_kwargs(name="app1", port=8080)
        # result = {"name": "app1", "port": 8080}
        ```
    """
    if data is None:
        data = {}
    for key, value in kwargs.items():
        data[key] = value
    return data
