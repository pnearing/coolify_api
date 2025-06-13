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

    def public(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a public Git repository.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "git_repository": "string",
            "git_branch": "string",
            "build_pack": "string",
            "ports_exposes": "string",
            "destination_uuid": "string",
            "name": "string",
            "description": "string",
            "domains": "string",
            "git_commit_sha": "string",
            "docker_registry_image_name": "string",
            "docker_registry_image_tag": "string",
            "is_static": true,
            "static_image": "string",
            "install_command": "string",
            "build_command": "string",
            "start_command": "string",
            "ports_mappings": "string",
            "base_directory": "string",
            "publish_directory": "string",
            "health_check_enabled": true,
            "health_check_path": "string",
            "health_check_port": "string",
            "health_check_host": "string",
            "health_check_method": "string",
            "health_check_return_code": 0,
            "health_check_scheme": "string",
            "health_check_response_text": "string",
            "health_check_interval": 0,
            "health_check_timeout": 0,
            "health_check_retries": 0,
            "health_check_start_period": 0,
            "limits_memory": "string",
            "limits_memory_swap": "string",
            "limits_memory_swappiness": 0,
            "limits_memory_reservation": "string",
            "limits_cpus": "string",
            "limits_cpuset": "string",
            "limits_cpu_shares": 0,
            "custom_labels": "string",
            "custom_docker_run_options": "string",
            "post_deployment_command": "string",
            "post_deployment_command_container": "string",
            "pre_deployment_command": "string",
            "pre_deployment_command_container": "string",
            "manual_webhook_secret_github": "string",
            "manual_webhook_secret_gitlab": "string",
            "manual_webhook_secret_bitbucket": "string",
            "manual_webhook_secret_gitea": "string",
            "redirect": "string",
            "instant_deploy": true,
            "dockerfile": "string",
            "docker_compose_location": "string",
            "docker_compose_raw": "string",
            "docker_compose_custom_start_command": "string",
            "docker_compose_custom_build_command": "string",
            "docker_compose_domains": [...],
            "watch_paths": "string",
            "use_build_server": true
        
        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating public application", kwargs)
        result = self._http_utils.post("applications/public", data=kwargs)
        _log_message(self._logger, DEBUG, "Public application created", result)
        return result


    def private_github_app(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a private repository using GitHub App authentication.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "github_app_uuid": "string",
            "git_repository": "string",
            "git_branch": "string",
            "ports_exposes": "string",
            "destination_uuid": "string",
            "build_pack": "string",
            "name": "string",
            "description": "string",
            "domains": "string",
            "git_commit_sha": "string",
            "docker_registry_image_name": "string",
            "docker_registry_image_tag": "string",
            "is_static": true,
            "static_image": "string",
            "install_command": "string",
            "build_command": "string",
            "start_command": "string",
            "ports_mappings": "string",
            "base_directory": "string",
            "publish_directory": "string",
            "health_check_enabled": true,
            "health_check_path": "string",
            "health_check_port": "string",
            "health_check_host": "string",
            "health_check_method": "string",
            "health_check_return_code": 0,
            "health_check_scheme": "string",
            "health_check_response_text": "string",
            "health_check_interval": 0,
            "health_check_timeout": 0,
            "health_check_retries": 0,
            "health_check_start_period": 0,
            "limits_memory": "string",
            "limits_memory_swap": "string",
            "limits_memory_swappiness": 0,
            "limits_memory_reservation": "string",
            "limits_cpus": "string",
            "limits_cpuset": "string",
            "limits_cpu_shares": 0,
            "custom_labels": "string",
            "custom_docker_run_options": "string",
            "post_deployment_command": "string",
            "post_deployment_command_container": "string",
            "pre_deployment_command": "string",
            "pre_deployment_command_container": "string",
            "manual_webhook_secret_github": "string",
            "manual_webhook_secret_gitlab": "string",
            "manual_webhook_secret_bitbucket": "string",
            "manual_webhook_secret_gitea": "string",
            "redirect": "string",
            "instant_deploy": true,
            "dockerfile": "string",
            "docker_compose_location": "string",
            "docker_compose_raw": "string",
            "docker_compose_custom_start_command": "string",
            "docker_compose_custom_build_command": "string",
            "docker_compose_domains": [],
            "watch_paths": "string",
            "use_build_server": true

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating private GitHub App application", kwargs)
        result = self._http_utils.post("applications/private-github-app", data=kwargs)
        _log_message(self._logger, DEBUG, "Private GitHub App application created", result)
        return result


    def private_deploy_key(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a private repository using deploy key authentication.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "private_key_uuid": "string",
            "git_repository": "string",
            "git_branch": "string",
            "ports_exposes": "string",
            "destination_uuid": "string",
            "build_pack": "string",
            "name": "string",
            "description": "string",
            "domains": "string",
            "git_commit_sha": "string",
            "docker_registry_image_name": "string",
            "docker_registry_image_tag": "string",
            "is_static": true,
            "static_image": "string",
            "install_command": "string",
            "build_command": "string",
            "start_command": "string",
            "ports_mappings": "string",
            "base_directory": "string",
            "publish_directory": "string",
            "health_check_enabled": true,
            "health_check_path": "string",
            "health_check_port": "string",
            "health_check_host": "string",
            "health_check_method": "string",
            "health_check_return_code": 0,
            "health_check_scheme": "string",
            "health_check_response_text": "string",
            "health_check_interval": 0,
            "health_check_timeout": 0,
            "health_check_retries": 0,
            "health_check_start_period": 0,
            "limits_memory": "string",
            "limits_memory_swap": "string",
            "limits_memory_swappiness": 0,
            "limits_memory_reservation": "string",
            "limits_cpus": "string",
            "limits_cpuset": "string",
            "limits_cpu_shares": 0,
            "custom_labels": "string",
            "custom_docker_run_options": "string",
            "post_deployment_command": "string",
            "post_deployment_command_container": "string",
            "pre_deployment_command": "string",
            "pre_deployment_command_container": "string",
            "manual_webhook_secret_github": "string",
            "manual_webhook_secret_gitlab": "string",
            "manual_webhook_secret_bitbucket": "string",
            "manual_webhook_secret_gitea": "string",
            "redirect": "string",
            "instant_deploy": true,
            "dockerfile": "string",
            "docker_compose_location": "string",
            "docker_compose_raw": "string",
            "docker_compose_custom_start_command": "string",
            "docker_compose_custom_build_command": "string",
            "docker_compose_domains": [],
            "watch_paths": "string",
            "use_build_server": true
        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating private deploy key application", kwargs)
        result = self._http_utils.post("applications/private-deploy-key", data=kwargs)
        _log_message(self._logger, DEBUG, "Private deploy key application created", result)
        return result


    def dockerfile(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Dockerfile.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "dockerfile": "string",
            "build_pack": "string",
            "ports_exposes": "string",
            "destination_uuid": "string",
            "name": "string",
            "description": "string",
            "domains": "string",
            "docker_registry_image_name": "string",
            "docker_registry_image_tag": "string",
            "ports_mappings": "string",
            "base_directory": "string",
            "health_check_enabled": true,
            "health_check_path": "string",
            "health_check_port": "string",
            "health_check_host": "string",
            "health_check_method": "string",
            "health_check_return_code": 0,
            "health_check_scheme": "string",
            "health_check_response_text": "string",
            "health_check_interval": 0,
            "health_check_timeout": 0,
            "health_check_retries": 0,
            "health_check_start_period": 0,
            "limits_memory": "string",
            "limits_memory_swap": "string",
            "limits_memory_swappiness": 0,
            "limits_memory_reservation": "string",
            "limits_cpus": "string",
            "limits_cpuset": "string",
            "limits_cpu_shares": 0,
            "custom_labels": "string",
            "custom_docker_run_options": "string",
            "post_deployment_command": "string",
            "post_deployment_command_container": "string",
            "pre_deployment_command": "string",
            "pre_deployment_command_container": "string",
            "manual_webhook_secret_github": "string",
            "manual_webhook_secret_gitlab": "string",
            "manual_webhook_secret_bitbucket": "string",
            "manual_webhook_secret_gitea": "string",
            "redirect": "string",
            "instant_deploy": true,
            "use_build_server": true

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating Dockerfile application", kwargs)
        result = self._http_utils.post("applications/dockerfile", data=kwargs)
        _log_message(self._logger, DEBUG, "Dockerfile application created", result)
        return result

    def docker_image(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker image.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "docker_registry_image_name": "string",
            "docker_registry_image_tag": "string",
            "ports_exposes": "string",
            "destination_uuid": "string",
            "name": "string",
            "description": "string",
            "domains": "string",
            "ports_mappings": "string",
            "health_check_enabled": true,
            "health_check_path": "string",
            "health_check_port": "string",
            "health_check_host": "string",
            "health_check_method": "string",
            "health_check_return_code": 0,
            "health_check_scheme": "string",
            "health_check_response_text": "string",
            "health_check_interval": 0,
            "health_check_timeout": 0,
            "health_check_retries": 0,
            "health_check_start_period": 0,
            "limits_memory": "string",
            "limits_memory_swap": "string",
            "limits_memory_swappiness": 0,
            "limits_memory_reservation": "string",
            "limits_cpus": "string",
            "limits_cpuset": "string",
            "limits_cpu_shares": 0,
            "custom_labels": "string",
            "custom_docker_run_options": "string",
            "post_deployment_command": "string",
            "post_deployment_command_container": "string",
            "pre_deployment_command": "string",
            "pre_deployment_command_container": "string",
            "manual_webhook_secret_github": "string",
            "manual_webhook_secret_gitlab": "string",
            "manual_webhook_secret_bitbucket": "string",
            "manual_webhook_secret_gitea": "string",
            "redirect": "string",
            "instant_deploy": true,
            "use_build_server": true

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating Docker image application", kwargs)
        result = self._http_utils.post("applications/dockerimage", data=kwargs)
        _log_message(self._logger, DEBUG, "Docker image application created", result)
        return result

    def docker_compose(self, **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker Compose configuration.

        Args:
            "project_uuid": "string",
            "server_uuid": "string",
            "environment_name": "string",
            "environment_uuid": "string",
            "docker_compose_raw": "string",
            "destination_uuid": "string",
            "name": "string",
            "description": "string",
            "instant_deploy": true,
            "use_build_server": true

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        _log_message(self._logger, DEBUG, "Creating Docker Compose application", kwargs)
        result = self._http_utils.post("applications/dockercompose", data=kwargs)
        _log_message(self._logger, DEBUG, "Docker Compose application created", result)
        return result
