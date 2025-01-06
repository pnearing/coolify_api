"""Coolify Private Keys API client.

This module provides methods to manage SSH private keys in Coolify, including:
- Listing all private keys
- Getting key details
- Creating new keys
- Updating existing keys
- Deleting keys

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all private keys
    keys = client.private_keys.list_all()

    # Create a new key
    new_key = client.private_keys.create({
        "name": "Deploy Key",
        "description": "Key for deployments",
        "private_key": "-----BEGIN RSA PRIVATE KEY-----\n..."
    })

    # Update a key
    client.private_keys.update("key-uuid", {
        "name": "Updated Name",
        "description": "Updated description"
    })

    # Delete a key
    client.private_keys.delete("key-uuid")
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyPrivateKeys:
    """Manages SSH private keys in Coolify.

    This class provides methods to interact with private keys used for Git authentication
    and other secure operations.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the private keys manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all private keys.

        Returns:
            List of private key objects containing:
            - id (int): Internal key ID
            - uuid (str): Key UUID
            - name (str): Key name
            - description (str): Key description
            - private_key (str): The private key content
            - is_git_related (bool): Whether key is used for Git
            - team_id (int): Team ID
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all private keys"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("security/keys")
        message = "Finish listing all private keys"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, key_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get private key details by UUID.

        Args:
            key_uuid: UUID of the private key to retrieve

        Returns:
            Private key object containing full details (same structure as list_all)

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If key UUID not found
        """
        message = f"Start to get private key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"security/keys/{key_uuid}")
        message = f"Finish getting private key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def create(self, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a new private key.

        Args:
            data: Key configuration containing:
                - name (str): Key name
                - description (str): Key description
                - private_key (str, required): The private key content
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the created key

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If required fields are missing
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = "Start to create a new private key"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post("security/keys", data=data)
        message = "Finish creating a new private key"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, key_uuid: str, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update a private key.

        Args:
            key_uuid: UUID of the key to update
            data: Updated key configuration containing:
                - name (str): Key name
                - description (str): Key description
                - private_key (str, required): The private key content
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the updated key

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If key UUID not found
            CoolifyValidationError: If required fields are missing
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"security/keys/{key_uuid}", data=data)
        message = f"Finish updating key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, key_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete a private key.

        Args:
            key_uuid: UUID of the key to delete

        Returns:
            Dictionary containing confirmation:
            - message (str): "Private Key deleted."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If key UUID not found
        """
        message = f"Start to delete key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(f"security/keys/{key_uuid}")
        message = f"Finish deleting key with uuid: {key_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
