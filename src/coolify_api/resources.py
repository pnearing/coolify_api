"""Coolify Resources API client.

This module provides methods to list all resources in a Coolify instance, including:
- Applications
- Databases
- Services
- Projects
- Teams
And their associated metadata.

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # Get all resources
    resources = client.resources.list_all()
    ```
"""

from logging import getLogger, DEBUG
from typing import Coroutine, Any, Dict, List

from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyResources:
    """Manages Coolify resource listing.

    This class provides methods to get information about all resources in a Coolify
    instance, providing a comprehensive view of the deployment environment.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the resources manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all resources in the Coolify instance.

        Returns:
            List of resource objects containing details about:
            - Applications
            - Databases
            - Services
            - Projects
            - Teams
            And their associated metadata including:
            - IDs
            - Names
            - Types
            - Status
            - Configuration
            - Relationships

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails

        Note:
            The exact structure of the response is complex and depends on the types
            of resources deployed in your Coolify instance. Refer to the API
            documentation for detailed schema information.
        """
        _log_message(self._logger, DEBUG, "Listing all resources")
        results = self._http_utils.get("resources")
        _log_message(self._logger, DEBUG, "Finished listing resources", results)
        return results
