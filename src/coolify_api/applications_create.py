"""Application creation functionality for the Coolify API client.

This module provides methods for creating different types of applications in Coolify, including:
- Public Git repositories
- Private Git repositories (via GitHub App or Deploy Key)
- Dockerfile-based applications
- Docker image-based applications
- Docker Compose applications

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # Create from public repository
    app = client.applications.create.public(
        project_uuid="proj-uuid",
        server_uuid="srv-uuid",
        environment_name="production",
        git_repository="https://github.com/user/repo",
        git_branch="main",
        build_pack="nixpacks",
        ports_exposes="3000"
    )

    # Create from Docker image
    app = client.applications.create.docker_image(
        project_uuid="proj-uuid",
        server_uuid="srv-uuid",
        environment_name="production",
        docker_registry_image_name="nginx",
        docker_registry_image_tag="latest",
        ports_exposes="80"
    )
    ```
"""
from logging import getLogger, DEBUG
from typing import Any, Coroutine

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyApplicationCreate:
    """Handles creation of different types of Coolify applications.

    This class provides methods for creating various types of applications supported by Coolify,
    including Git repositories, Dockerfiles, Docker images, and Docker Compose configurations.

    Attributes:
        _http_utils (HTTPUtils): HTTP client for making API requests
        _logger: Logger instance for this class
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the application creation manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def public(self, project_uuid: str, server_uuid: str, environment_name: str,
               git_repository: str, git_branch: str, build_pack: str, ports_exposes: str,
               **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a public Git repository.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment (e.g., "production")
            git_repository: URL of the Git repository
            git_branch: Branch to deploy from
            build_pack: Build pack type ("nixpacks", "static", "dockerfile", "dockercompose")
            ports_exposes: Ports to expose (e.g., "3000" or "80,443")
            **kwargs: Optional parameters including:
                - name (str): Application name
                - description (str): Application description
                - domains (str): Application domains
                - install_command (str): Custom install command
                - build_command (str): Custom build command
                - start_command (str): Custom start command
                - base_directory (str): Base directory for commands
                - publish_directory (str): Directory to publish
                - instant_deploy (bool): Deploy immediately after creation

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "build_pack": build_pack,
            "ports_exposes": ports_exposes
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating public application", data)
        result = self._http_utils.post("applications/public", data=data)
        _log_message(self._logger, DEBUG, "Public application created", result)
        return result

    def private_github_app(self, project_uuid: str, server_uuid: str, environment_name: str,
                          github_app_uuid: str, git_repository: str, git_branch: str,
                          build_pack: str, ports_exposes: str, **kwargs
                          ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a private repository using GitHub App authentication.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment
            github_app_uuid: UUID of the GitHub App for authentication
            git_repository: URL of the private Git repository
            git_branch: Branch to deploy from
            build_pack: Build pack type ("nixpacks", "static", "dockerfile", "dockercompose")
            ports_exposes: Ports to expose
            **kwargs: Optional parameters (same as public() method)

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "github_app_uuid": github_app_uuid,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "build_pack": build_pack,
            "ports_exposes": ports_exposes
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating private GitHub App application", data)
        result = self._http_utils.post("applications/private-github-app", data=data)
        _log_message(self._logger, DEBUG, "Private GitHub App application created", result)
        return result

    def private_deploy_key(self, project_uuid: str, server_uuid: str, environment_name: str,
                          private_key_uuid: str, git_repository: str, git_branch: str,
                          build_pack: str, ports_exposes: str, **kwargs
                          ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a private repository using deploy key authentication.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment
            private_key_uuid: UUID of the deploy key for authentication
            git_repository: URL of the private Git repository
            git_branch: Branch to deploy from
            build_pack: Build pack type ("nixpacks", "static", "dockerfile", "dockercompose")
            ports_exposes: Ports to expose
            **kwargs: Optional parameters (same as public() method)

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "private_key_uuid": private_key_uuid,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "build_pack": build_pack,
            "ports_exposes": ports_exposes
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating private deploy key application", data)
        result = self._http_utils.post("applications/private-deploy-key", data=data)
        _log_message(self._logger, DEBUG, "Private deploy key application created", result)
        return result

    def dockerfile(self, project_uuid: str, server_uuid: str, environment_name: str,
                  dockerfile: str, ports_exposes: str, **kwargs
                  ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Dockerfile.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment
            dockerfile: Content of the Dockerfile
            ports_exposes: Ports to expose
            **kwargs: Optional parameters including:
                - name (str): Application name
                - description (str): Application description
                - domains (str): Application domains
                - instant_deploy (bool): Deploy immediately after creation

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "dockerfile": dockerfile,
            "ports_exposes": ports_exposes
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating Dockerfile application", data)
        result = self._http_utils.post("applications/dockerfile", data=data)
        _log_message(self._logger, DEBUG, "Dockerfile application created", result)
        return result

    def docker_image(self, project_uuid: str, server_uuid: str, environment_name: str,
                    docker_registry_image_name: str, ports_exposes: str, **kwargs
                    ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker image.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment
            docker_registry_image_name: Name of the Docker image
            ports_exposes: Ports to expose
            **kwargs: Optional parameters including:
                - docker_registry_image_tag (str): Image tag (default: "latest")
                - name (str): Application name
                - description (str): Application description
                - domains (str): Application domains
                - instant_deploy (bool): Deploy immediately after creation

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "docker_registry_image_name": docker_registry_image_name,
            "ports_exposes": ports_exposes
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating Docker image application", data)
        result = self._http_utils.post("applications/dockerimage", data=data)
        _log_message(self._logger, DEBUG, "Docker image application created", result)
        return result

    def docker_compose(self, project_uuid: str, server_uuid: str, environment_name: str,
                      docker_compose_raw: str, **kwargs
                      ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker Compose configuration.

        Args:
            project_uuid: UUID of the project to create the application in
            server_uuid: UUID of the server to deploy the application to
            environment_name: Name of the environment
            docker_compose_raw: Raw content of the docker-compose.yml file
            **kwargs: Optional parameters including:
                - name (str): Application name
                - description (str): Application description
                - instant_deploy (bool): Deploy immediately after creation
                - use_build_server (bool): Whether to use build server

        Returns:
            Dictionary containing the created application details

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "environment_name": environment_name,
            "docker_compose_raw": docker_compose_raw
        }, **kwargs)

        _log_message(self._logger, DEBUG, "Creating Docker Compose application", data)
        result = self._http_utils.post("applications/dockercompose", data=data)
        _log_message(self._logger, DEBUG, "Docker Compose application created", result)
        return result
