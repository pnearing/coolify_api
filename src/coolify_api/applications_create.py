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


    def public(self, project_uuid: str, server_uuid: str, git_repository: str, 
               git_branch: str, ports_exposes: str, environment_name: str = None, environment_uuid: str = None,
               **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a public Git repository.

        Args:
            # Required
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid. *Required
            git_repository - string - The git repository URL. *Required
            git_branch - string - The git branch. *Required
            ports_exposes - string - The ports to expose. *Required

            # Optional
            build_pack - string - The build pack type. (Valid values: nixpacks, static, dockerfile, dockercompose)
            destination_uuid - string - The destination UUID.
            name - string - The application name.
            description - string - The application description.
            domains - string - The application domains.
            git_commit_sha - string - The git commit SHA.
            docker_registry_image_name - string - The docker registry image name.
            docker_registry_image_tag - string - The docker registry image tag.
            is_static - boolean - The flag to indicate if the application is static.
            static_image - string - The static image. (Valid values: nginx:alpine)
            install_command - string - The install command.
            build_command - string - The build command.
            start_command - string - The start command.
            ports_mappings - string - The ports mappings.
            base_directory - string - The base directory for all commands.
            publish_directory - string - The publish directory.
            health_check_enabled - boolean - Health check enabled.
            health_check_path - string - Health check path.
            health_check_port - string - Health check port.
            health_check_host - string - Health check host.
            health_check_method - string - Health check method.
            health_check_return_code - integer - Health check return code.
            health_check_scheme - string - Health check scheme.
            health_check_response_text - string - Health check response text.
            health_check_interval - integer - Health check interval in seconds.
            health_check_timeout - integer - Health check timeout in seconds.
            health_check_retries - integer - Health check retries count.
            health_check_start_period - integer - Health check start period in seconds.
            limits_memory - string - Memory limit.
            limits_memory_swap - string - Memory swap limit.
            limits_memory_swappiness - integer - Memory swappiness.
            limits_memory_reservation - string - Memory reservation.
            limits_cpus - string - CPU limit.
            limits_cpuset - string - CPU set.
            limits_cpu_shares - integer - CPU shares.
            custom_labels - string - Custom labels.
            custom_docker_run_options - string - Custom docker run options.
            post_deployment_command - string - Post deployment command.
            post_deployment_command_container - string - Post deployment command container.
            pre_deployment_command - string - Pre deployment command.
            pre_deployment_command_container - string - Pre deployment command container.
            manual_webhook_secret_github - string - Manual webhook secret for Github.
            manual_webhook_secret_gitlab - string - Manual webhook secret for Gitlab.
            manual_webhook_secret_bitbucket - string - Manual webhook secret for Bitbucket.
            manual_webhook_secret_gitea - string - Manual webhook secret for Gitea.
            redirect - string - How to set redirect with Traefik / Caddy. www<->non-www. Valid values: www, non-www, both.
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            dockerfile - string - The Dockerfile content.
            docker_compose_location - string - The Docker Compose location.
            docker_compose_raw - string - The Docker Compose raw content.
            docker_compose_custom_start_command - string - The Docker Compose custom start command.
            docker_compose_custom_build_command - string - The Docker Compose custom build command.
            docker_compose_domains - array - The Docker Compose domains.
            watch_paths - string - The watch paths.
            use_build_server - boolean - Use build server.
        
        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "ports_exposes": ports_exposes,
        }, **kwargs)

        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        _log_message(self._logger, DEBUG, "Creating public application", data)
        result = self._http_utils.post("applications/public", data=data)
        _log_message(self._logger, DEBUG, "Public application created", result)
        return result


    def private_github_app(self, project_uuid: str, server_uuid: str, github_app_uuid: str, git_repository: str,
                           git_branch: str, ports_exposes: str, environment_name: str = None, environment_uuid: str = None,
                           **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a private repository using GitHub App authentication.

        Args:
            # Required
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid. *Required
            github_app_uuid - string - The Github App UUID. *Required
            git_repository - string - The git repository URL. *Required
            git_branch - string - The git branch. *Required
            ports_exposes - string - The ports to expose. *Required

            # Optional
            destination_uuid - string - The destination UUID.
            build_pack - string - The build pack type. Valid values: nixpacks, static, dockerfile, dockercompose
            name - string - The application name.
            description - string - The application description.
            domains - string - The application domains.
            git_commit_sha - string - The git commit SHA.
            docker_registry_image_name - string - The docker registry image name.
            docker_registry_image_tag - string - The docker registry image tag.
            is_static - boolean - The flag to indicate if the application is static.
            static_image - string - The static image. Valid values: nginx:alpine
            install_command - string - The install command.
            build_command - string - The build command.
            start_command - string - The start command.
            ports_mappings - string - The ports mappings.
            base_directory - string - The base directory for all commands.
            publish_directory - string - The publish directory.
            health_check_enabled - boolean - Health check enabled.
            health_check_path - string - Health check path.
            health_check_port - string - Health check port.
            health_check_host - string - Health check host.
            health_check_method - string - Health check method.
            health_check_return_code - integer - Health check return code.
            health_check_scheme - string - Health check scheme.
            health_check_response_text - string - Health check response text.
            health_check_interval - integer - Health check interval in seconds.
            health_check_timeout - integer - Health check timeout in seconds.
            health_check_retries - integer - Health check retries count.
            health_check_start_period - integer - Health check start period in seconds.
            limits_memory - string - Memory limit.
            limits_memory_swap - string - Memory swap limit.
            limits_memory_swappiness - integer - Memory swappiness.
            limits_memory_reservation - string - Memory reservation.
            limits_cpus - string - CPU limit.
            limits_cpuset - string - CPU set.
            limits_cpu_shares - integer - CPU shares.
            custom_labels - string - Custom labels.
            custom_docker_run_options - string - Custom docker run options.
            post_deployment_command - string - Post deployment command.
            post_deployment_command_container - string - Post deployment command container.
            pre_deployment_command - string - Pre deployment command.
            pre_deployment_command_container - string - Pre deployment command container.
            manual_webhook_secret_github - string - Manual webhook secret for Github.
            manual_webhook_secret_gitlab - string - Manual webhook secret for Gitlab.
            manual_webhook_secret_bitbucket - string - Manual webhook secret for Bitbucket.
            manual_webhook_secret_gitea - string - Manual webhook secret for Gitea.
            redirect - string - How to set redirect with Traefik / Caddy. www<->non-www. Valid values: www, non-www, both.
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            dockerfile - string - The Dockerfile content.
            docker_compose_location - string - The Docker Compose location.
            docker_compose_raw - string - The Docker Compose raw content.
            docker_compose_custom_start_command - string - The Docker Compose custom start command.
            docker_compose_custom_build_command - string - The Docker Compose custom build command.
            docker_compose_domains - array - The Docker Compose domains.
            watch_paths - string - The watch paths.
            use_build_server - boolean - Use build server.


        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "github_app_uuid": github_app_uuid,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "ports_exposes": ports_exposes,
        }, **kwargs)

        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        _log_message(self._logger, DEBUG, "Creating private GitHub App application", data)
        result = self._http_utils.post("applications/private-github-app", data=data)
        _log_message(self._logger, DEBUG, "Private GitHub App application created", result)
        return result


    def private_deploy_key(self, project_uuid: str, server_uuid: str, private_key_uuid: str, git_repository: str,
                            git_branch: str, ports_exposes: str, environment_name: str = None, environment_uuid: str = None,
                            **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a private repository using deploy key authentication.

        Args:
            # Required
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid. *Required
            private_key_uuid - string - The private key UUID. *Required
            git_repository - string - The git repository URL. *Required
            git_branch - string - The git branch. *Required
            ports_exposes - string - The ports to expose. *Required

            # Optional
            destination_uuid - string - The destination UUID.
            build_pack - string - The build pack type. Valid values: nixpacks, static, dockerfile, dockercompose
            name - string - The application name.
            description - string - The application description.
            domains - string - The application domains.
            git_commit_sha - string - The git commit SHA.
            docker_registry_image_name - string - The docker registry image name.
            docker_registry_image_tag - string - The docker registry image tag.
            is_static - boolean - The flag to indicate if the application is static.
            static_image - string - The static image. Valid values: nginx:alpine
            install_command - string - The install command.
            build_command - string - The build command.
            start_command - string - The start command.
            ports_mappings - string - The ports mappings.
            base_directory - string - The base directory for all commands.
            publish_directory - string - The publish directory.
            health_check_enabled - boolean - Health check enabled.
            health_check_path - string - Health check path.
            health_check_port - string - Health check port.
            health_check_host - string - Health check host.
            health_check_method - string - Health check method.
            health_check_return_code - integer - Health check return code.
            health_check_scheme - string - Health check scheme.
            health_check_response_text - string - Health check response text.
            health_check_interval - integer - Health check interval in seconds.
            health_check_timeout - integer - Health check timeout in seconds.
            health_check_retries - integer - Health check retries count.
            health_check_start_period - integer - Health check start period in seconds.
            limits_memory - string - Memory limit.
            limits_memory_swap - string - Memory swap limit.
            limits_memory_swappiness - integer - Memory swappiness.
            limits_memory_reservation - string - Memory reservation.
            limits_cpus - string - CPU limit.
            limits_cpuset - string - CPU set.
            limits_cpu_shares - integer - CPU shares.
            custom_labels - string - Custom labels.
            custom_docker_run_options - string - Custom docker run options.
            post_deployment_command - string - Post deployment command.
            post_deployment_command_container - string - Post deployment command container.
            pre_deployment_command - string - Pre deployment command.
            pre_deployment_command_container - string - Pre deployment command container.
            manual_webhook_secret_github - string - Manual webhook secret for Github.
            manual_webhook_secret_gitlab - string - Manual webhook secret for Gitlab.
            manual_webhook_secret_bitbucket - string - Manual webhook secret for Bitbucket.
            manual_webhook_secret_gitea - string - Manual webhook secret for Gitea.
            redirect - string - How to set redirect with Traefik / Caddy. www<->non-www. Valid values: www, non-www, both
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            dockerfile - string - The Dockerfile content.
            docker_compose_location - string - The Docker Compose location.
            docker_compose_raw - string - The Docker Compose raw content.
            docker_compose_custom_start_command - string - The Docker Compose custom start command.
            docker_compose_custom_build_command - string - The Docker Compose custom build command.
            docker_compose_domains - array - The Docker Compose domains.
            watch_paths - string - The watch paths.
            use_build_server - boolean - Use build server.

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "private_key_uuid": private_key_uuid,
            "git_repository": git_repository,
            "git_branch": git_branch,
            "ports_exposes": ports_exposes,
        }, **kwargs)

        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        _log_message(self._logger, DEBUG, "Creating private deploy key application", data)
        result = self._http_utils.post("applications/private-deploy-key", data=data)
        _log_message(self._logger, DEBUG, "Private deploy key application created", result)
        return result


    def dockerfile(self, project_uuid: str, server_uuid: str, dockerfile: str, 
                    environment_name: str = None, environment_uuid: str = None, 
                    **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """
        Create an application from a Dockerfile.

        Args:
            # Required
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid. *Required
            dockerfile - string - The Dockerfile content. *Required

            # Optional
            build_pack - string - The build pack type. *Valid values: nixpacks, static, dockerfile, dockercompose
            ports_exposes - string - The ports to expose.
            destination_uuid - string - The destination UUID.
            name - string - The application name.
            description - string - The application description.
            domains - string - The application domains.
            docker_registry_image_name - string - The docker registry image name.
            docker_registry_image_tag - string - The docker registry image tag.
            ports_mappings - string - The ports mappings.
            base_directory - string - The base directory for all commands.
            health_check_enabled - boolean - Health check enabled.
            health_check_path - string - Health check path.
            health_check_port - string - Health check port.
            health_check_host - string - Health check host.
            health_check_method - string - Health check method.
            health_check_return_code - integer - Health check return code.
            health_check_scheme - string - Health check scheme.
            health_check_response_text - string - Health check response text.
            health_check_interval - integer - Health check interval in seconds.
            health_check_timeout - integer - Health check timeout in seconds.
            health_check_retries - integer - Health check retries count.
            health_check_start_period - integer - Health check start period in seconds.
            limits_memory - string - Memory limit.
            limits_memory_swap - string - Memory swap limit.
            limits_memory_swappiness - integer - Memory swappiness.
            limits_memory_reservation - string - Memory reservation.
            limits_cpus - string - CPU limit.
            limits_cpuset - string - CPU set.
            limits_cpu_shares - integer - CPU shares.
            custom_labels - string - Custom labels.
            custom_docker_run_options - string - Custom docker run options.
            post_deployment_command - string - Post deployment command.
            post_deployment_command_container - string - Post deployment command container.
            pre_deployment_command - string - Pre deployment command.
            pre_deployment_command_container - string - Pre deployment command container.
            manual_webhook_secret_github - string - Manual webhook secret for Github.
            manual_webhook_secret_gitlab - string - Manual webhook secret for Gitlab.
            manual_webhook_secret_bitbucket - string - Manual webhook secret for Bitbucket.
            manual_webhook_secret_gitea - string - Manual webhook secret for Gitea.
            redirect - string - How to set redirect with Traefik / Caddy. www<->non-www. *Valid values - www, non-www, both
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            docker_compose_location - string - The Docker Compose location.
            docker_compose_raw - string - The Docker Compose raw content.
            docker_compose_custom_start_command - string - The Docker Compose custom start command.
            docker_compose_custom_build_command - string - The Docker Compose custom build command.
            docker_compose_domains - array - The Docker Compose domains.
            watch_paths - string - The watch paths.
            use_build_server - boolean - Use build server.

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "dockerfile": dockerfile,
        }, **kwargs)

        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        _log_message(self._logger, DEBUG, "Creating Dockerfile application", data)
        result = self._http_utils.post("applications/dockerfile", data=data)
        _log_message(self._logger, DEBUG, "Dockerfile application created", result)
        return result

    def docker_image(self, project_uuid: str, server_uuid: str, docker_registry_image_name: str, 
                     ports_exposes: str, environment_name: str = None, environment_uuid: str = None, 
                     **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker image.

        Args:
            # Required
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            docker_registry_image_name - string - The docker registry image name.*Required
            ports_exposes - string - The ports to expose.*Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid.*Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid.*Required

            # Optional
            docker_registry_image_tag - string - The docker registry image tag.
            destination_uuid - string - The destination UUID.
            name - string - The application name.
            description - string - The application description.
            domains - string - The application domains.
            ports_mappings - string - The ports mappings.
            health_check_enabled - boolean - Health check enabled.
            health_check_path - string - Health check path.
            health_check_port - string - Health check port.
            health_check_host - string - Health check host.
            health_check_method - string - Health check method.
            health_check_return_code - integer - Health check return code.
            health_check_scheme - string - Health check scheme.
            health_check_response_text - string - Health check response text.
            health_check_interval - integer - Health check interval in seconds.
            health_check_timeout - integer - Health check timeout in seconds.
            health_check_retries - integer - Health check retries count.
            health_check_start_period - integer - Health check start period in seconds.
            limits_memory - string - Memory limit.
            limits_memory_swap - string - Memory swap limit.
            limits_memory_swappiness - integer - Memory swappiness.
            limits_memory_reservation - string - Memory reservation.
            limits_cpus - string - CPU limit.
            limits_cpuset - string - CPU set.
            limits_cpu_shares - integer - CPU shares.
            custom_labels - string - Custom labels.
            custom_docker_run_options - string - Custom docker run options.
            post_deployment_command - string - Post deployment command.
            post_deployment_command_container - string - Post deployment command container.
            pre_deployment_command - string - Pre deployment command.
            pre_deployment_command_container - string - Pre deployment command container.
            manual_webhook_secret_github - string - Manual webhook secret for Github.
            manual_webhook_secret_gitlab - string - Manual webhook secret for Gitlab.
            manual_webhook_secret_bitbucket - string - Manual webhook secret for Bitbucket.
            manual_webhook_secret_gitea - string - Manual webhook secret for Gitea.
            redirect - string - How to set redirect with Traefik / Caddy. www<->non-www. Valid values: www, non-www, both
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            use_build_server - boolean - Use build server.

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "docker_registry_image_name": docker_registry_image_name,
            "ports_exposes": ports_exposes,
        }, **kwargs)

        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")

        _log_message(self._logger, DEBUG, "Creating Docker image application", data)
        result = self._http_utils.post("applications/dockerimage", data=data)
        _log_message(self._logger, DEBUG, "Docker image application created", result)
        return result

    def docker_compose(self, project_uuid: str, server_uuid: str, docker_compose_raw: str, 
                       environment_name: str = None, environment_uuid: str = None,
                        **kwargs) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        """Create an application from a Docker Compose configuration.

        Args:
            project_uuid - string - The project UUID. *Required
            server_uuid - string - The server UUID. *Required
            docker_compose_raw - string - The Docker Compose raw content. *Required
            environment_name - string - The environment name. You need to provide at least one of environment_name or environment_uuid. *Required
            environment_uuid - string - The environment UUID. You need to provide at least one of environment_name or environment_uuid. *Required
            
            destination_uuid - string - The destination UUID if the server has more than one destinations.
            name - string - The application name.
            description - string - The application description.
            instant_deploy - boolean - The flag to indicate if the application should be deployed instantly.
            use_build_server - boolean - Use build server.

        Returns:
            Dictionary containing the created application UUID:
            {
                "uuid": "string"
            }

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        data = create_data_with_kwargs({
            "project_uuid": project_uuid,
            "server_uuid": server_uuid,
            "docker_compose_raw": docker_compose_raw,
        }, **kwargs)
        
        if environment_name:
            data["environment_name"] = environment_name
        elif environment_uuid:
            data["environment_uuid"] = environment_uuid
        else:
            _log_message(self._logger, ERROR, "You need to provide at least one of environment_name or environment_uuid")
            raise ValueError("You need to provide at least one of environment_name or environment_uuid")
        
        _log_message(self._logger, DEBUG, "Creating Docker Compose application", data)
        result = self._http_utils.post("applications/dockercompose", data=data)
        _log_message(self._logger, DEBUG, "Docker Compose application created", result)
        return result
