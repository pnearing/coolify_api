"""Coolify Deployments API client.

This module provides methods to manage Coolify deployments, including:
- Listing all deployments
- Getting deployment details
- Triggering deployments by UUID or tag

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all deployments
    deployments = client.deployments.list_all()

    # Get specific deployment
    deployment = client.deployments.get("deploy-uuid")

    # Trigger deployments
    result = client.deployments.deploy(tag="production")  # Deploy by tag
    result = client.deployments.deploy(deployment_uuid="deploy-uuid")  # Deploy by UUID
    ```
"""

from logging import getLogger, DEBUG
from typing import Optional, Any, Coroutine, Dict, List

from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyDeployments:
    """Manages Coolify deployments.

    This class provides methods to interact with deployments in Coolify, including
    listing, retrieving details, and triggering deployments.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the deployments manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all currently running deployments.

        Returns:
            List of deployment objects containing details like:
            - id (int): Internal ID
            - application_id (str): ID of the application
            - deployment_uuid (str): UUID of the deployment
            - pull_request_id (int): PR ID if from pull request
            - force_rebuild (bool): Whether rebuild was forced
            - commit (str): Git commit hash
            - status (str): Current status
            - is_webhook (bool): Whether triggered by webhook
            - is_api (bool): Whether triggered via API
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp
            - logs (str): Deployment logs
            - current_process_id (str): Current process ID
            - restart_only (bool): Whether only restart
            - git_type (str): Git provider type
            - server_id (int): ID of the server
            - application_name (str): Name of the application
            - server_name (str): Name of the server
            - deployment_url (str): Deployment URL
            - destination_id (str): Destination ID
            - only_this_server (bool): Whether limited to one server
            - rollback (bool): Whether this is a rollback
            - commit_message (str): Git commit message

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all deployments"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("deployments")
        message = "Finish listing all deployments"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, deployment_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get deployment details by UUID.

        Args:
            deployment_uuid: UUID of the deployment to retrieve

        Returns:
            Deployment object containing full details (same structure as list_all)

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If deployment UUID not found
        """
        message = f"Start to get deployment with uuid: {deployment_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"deployments/{deployment_uuid}")
        message = f"Finish getting deployment with uuid: {deployment_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def deploy(self, deployment_uuid: Optional[str] = None, tag: Optional[str] = None,
               force_rebuild: bool = False, pull_request_id: Optional[int] = None\
                ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Trigger deployment by UUID or tag.

        Args:
            deployment_uuid: UUID(s) of deployment(s) to trigger. Can be comma-separated.
            tag: Tag name(s) to deploy. Can be comma-separated.
            force_rebuild: Whether to force rebuild (without cache)
            pull_request_id: ID of the pull request to deploy, cannot be used with tag(s)

        Returns:
            Dictionary containing deployment details:
            - deployments (List[Dict]): List of triggered deployments containing:
                - message (str): Status message
                - resource_uuid (str): UUID of the resource
                - deployment_uuid (str): UUID of the new deployment

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            AttributeError: If neither deployment_uuid nor tag nor pull_request_id is specified
            AttributeError: If both tag and pull_request_id are specified
        """
        if deployment_uuid is None and tag is None and pull_request_id is None:
            raise AttributeError("Either deployment_uuid or tag or pull_request_id must be specified")
        if tag and pull_request_id:
            raise AttributeError("Cannot specify both tag and pull_request_id")
        params = {"force": force_rebuild}
        if deployment_uuid:
            params["uuid"] = deployment_uuid
        if tag:
            params["tag"] = tag
        if pull_request_id:
            params['pr'] = pull_request_id
        message = f"Start to deploy deployment with params: {params}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.post("deploy", params=params)
        _log_message(self._logger, DEBUG, "Finish deploying deployment.")
        return results
