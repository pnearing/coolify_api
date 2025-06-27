"""Coolify Projects API client.

This module provides methods to manage Coolify projects, including:
- Listing all projects
- Getting project details
- Creating new projects
- Updating existing projects
- Deleting projects
- Managing project environments

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient(api_key="your_api_key")

    # List all projects
    projects = client.projects.list_all()

    # Create a new project
    new_project = client.projects.create({
        "name": "My Project",
        "description": "Project description"
    })

    # Get project details
    project = client.projects.get("project-uuid")

    # Update project
    client.projects.update("project-uuid", {
        "name": "Updated Name",
        "description": "New description"
    })

    # Delete project
    client.projects.delete("project-uuid")
    ```
"""

from logging import getLogger, DEBUG
from typing import Optional, Any, Coroutine, Dict, List

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyProjects:
    """Manages Coolify projects.

    This class provides methods to interact with projects in Coolify, including
    creating, updating, and managing project environments.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the projects manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all projects.

        Returns:
            List of project objects containing:
            - id (int): Internal project ID
            - uuid (str): Project UUID
            - name (str): Project name
            - description (str): Project description
            - environments (List[Dict]): List of project environments containing:
                - id (int): Environment ID
                - name (str): Environment name
                - project_id (int): Project ID
                - created_at (str): Creation timestamp
                - updated_at (str): Last update timestamp
                - description (str): Environment description

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all projects"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("projects")
        message = "Finish listing all projects"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, project_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get project details by UUID.

        Args:
            project_uuid: UUID of the project to retrieve

        Returns:
            Project object containing full details (same structure as list_all)

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If project UUID not found
        """
        message = f"Start to get project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"projects/{project_uuid}")
        message = f"Finish getting project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def create(self, data: Dict[str, Any], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Create a new project.

        Args:
            data: Project configuration containing:
                - name (str, required): Project name
                - description (str): Project description
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): UUID of the created project

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyValidationError: If required fields are missing
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = "Start to create a new project"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post("projects", data=data)
        message = "Finish creating a new project"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def update(self, project_uuid: str, data: Optional[Dict[str, Any]], **kwargs
               ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Update a project.

        Args:
            project_uuid: UUID of the project to update
            data: Updated project configuration containing:
                - name (str): Project name
                - description (str): Project description
            **kwargs: Additional configuration options

        Returns:
            Dictionary containing:
            - uuid (str): Project UUID
            - name (str): Updated name
            - description (str): Updated description

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If project UUID not found
            CoolifyValidationError: If validation fails
        """
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"projects/{project_uuid}", data=data)
        message = f"Finish updating project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def delete(self, project_uuid: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Delete a project.

        Args:
            project_uuid: UUID of the project to delete

        Returns:
            Dictionary containing confirmation:
            - message (str): "Project deleted."

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If project UUID not found
        """
        message = f"Start to delete project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(f"projects/{project_uuid}")
        message = f"Finish deleting project with uuid: {project_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def environment(self, project_uuid: str, environment_name: str = None, environment_uuid: str = None
                       ) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get project environment by name.

        Args:
            project_uuid: UUID of the project
            environment_name: Name of the environment to retrieve # One of environment_name or environment_uuid is required
            environment_uuid: The uuid of the environment to retrieve # One of environment_name or environment_uuid is required

        Returns:
            Environment object containing:
            - id (int): Environment ID
            - name (str): Environment name
            - project_id (int): Project ID
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp
            - description (str): Environment description

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If project or environment not found
        """
        if environment_uuid is not None:
            environment_value = environment_uuid
        elif environment_name is not None:
            environment_value = environment_name
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        message = f"Start to get environment {environment_value} for project: {project_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"projects/{project_uuid}/{environment_value}")
        message = f"Finish getting environment {environment_value}"
        _log_message(self._logger, DEBUG, message, results)
        return results
