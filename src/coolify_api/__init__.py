"""Coolify API Client Library.

This package provides a Python interface for interacting with the Coolify API. It enables management 
of Coolify resources including applications, databases, services, and deployments through a simple 
and intuitive API client.

Example:
    Basic usage of the Coolify API client:

    ```python
    from coolify_api import CoolifyAPIClient

    # Initialize the client
    client = CoolifyAPIClient(
        base_url="https://coolify.example.com", # Or use environment variable COOLIFY_BASE_URL
        api_key="your-api-key" # Or use environment variable COOLIFY_API_KEY
        )

    # Get application details
    app = client.applications.get("app-id")
    ```

Attributes:
    - CoolifyAPIClient: The main client class for interacting with the Coolify API.

License:
    Proprietary - All rights reserved
    See LICENSE file for full terms.

Author:
    Peter Nearing <pn@goldeverywhere.com>
"""
from .api_client import CoolifyAPIClient

__version__ = "0.1.0"
__author__ = "Peter Nearing"
__email__ = "pn@goldeverywhere.com"

__all__ = ["CoolifyAPIClient"]
