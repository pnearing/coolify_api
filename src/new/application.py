from typing import Any, Optional
from datetime import datetime
from logging import getLogger, DEBUG

from ..coolify_api._logging import _log_message
from coolify_api import CoolifyAPIClient



class CoolifyApplication:

    def __init__(self,
                 client: CoolifyAPIClient,
                 application_uuid: str,
                 do_load: bool = True,
                 application_data: dict[str, Any] = None,
                 ) -> None:
        
        self._client: CoolifyAPIClient = client
        """CoolifyAPIClient for the class."""
        self._application_uuid = application_uuid
        """Application UUID for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

        if application_data is not None and not isinstance(application_data, dict):
            raise TypeError("application_data must be a dictionary")

        if do_load: 
            data = client.applications.get(application_uuid)
        else:
            data = application_data

        if data is None:
            raise ValueError("application_data is None, and do_load is False")

        self.id: Optional[int] = data.get("id")
        """Unique identifier for the resource."""
        self.repository_project_id: Optional[int] = data.get("repository_project_id")
        """ID for the repository project associated with this resource."""
        self.description: Optional[str] = data.get("description")
        """Description of the resource."""
        self.uuid: Optional[str] = data.get("uuid")
        """Universally Unique Identifier (UUID) for the resource."""
        self.name: Optional[str] = data.get("name")
        """Name of the application or resource."""
        self.fqdn: Optional[str] = data.get("fqdn")
        """Fully Qualified Domain Name (FQDN) of the application."""
        self.config_hash: Optional[str] = data.get("config_hash")
        """Hash representing the configuration of the application."""
        self.git_repository: Optional[str] = data.get("git_repository")
        """URL of the associated Git repository."""
        self.git_branch: Optional[str] = data.get("git_branch")
        """Branch of the Git repository being used."""
        self.git_commit_sha: Optional[str] = data.get("git_commit_sha")
        """Commit SHA from the Git repository."""
        self.git_full_url: Optional[str] = data.get("git_full_url")
        """Complete URL of the Git repository."""
        self.docker_registry_image_name: Optional[str] = data.get("docker_registry_image_name")
        """Name of the Docker registry image."""
        self.docker_registry_image_tag: Optional[str] = data.get("docker_registry_image_tag")
        """Tag of the Docker registry image."""
        self.build_pack: Optional[str] = data.get("build_pack")
        """Build pack used for the application."""
        self.static_image: Optional[str] = data.get("static_image")
        """Static image related to the application."""
        self.install_command: Optional[str] = data.get("install_command")
        """Command used to install dependencies."""
        self.build_command: Optional[str] = data.get("build_command")
        """Command used to build the application."""
        self.start_command: Optional[str] = data.get("start_command")
        """Command used to start the application."""
        self.ports_exposes: Optional[str] = data.get("ports_exposes")
        """Ports exposed by the application."""
        self.ports_mappings: Optional[str] = data.get("ports_mappings")
        """Mapping of ports for the application."""
        self.base_directory: Optional[str] = data.get("base_directory")
        """Base directory for the application files."""
        self.publish_directory: Optional[str] = data.get("publish_directory")
        """Directory where the application will be published."""
        self.health_check_enabled: Optional[bool] = data.get("health_check_enabled")
        """Indicates whether health checks are enabled for the application."""
        self.health_check_path: Optional[str] = data.get("health_check_path")
        """Path used for health checking."""
        self.health_check_port: Optional[str] = data.get("health_check_port")
        """Port used for health checking."""
        self.health_check_host: Optional[str] = data.get("health_check_host")
        """Host used for health checking."""
        self.health_check_method: Optional[str] = data.get("health_check_method")
        """HTTP method used for health checking."""
        self.health_check_return_code: Optional[int] = data.get("health_check_return_code")
        """Expected HTTP return code for successful health checks."""
        self.health_check_scheme: Optional[str] = data.get("health_check_scheme")
        """Scheme (e.g., HTTP or HTTPS) used for health checks."""
        self.health_check_response_text: Optional[str] = data.get("health_check_response_text")
        """Expected response text for successful health checks."""
        self.health_check_interval: Optional[int] = data.get("health_check_interval")
        """Interval in seconds between health checks."""
        self.health_check_timeout: Optional[int] = data.get("health_check_timeout")
        """Timeout in seconds for health checks."""
        self.health_check_retries: Optional[int] = data.get("health_check_retries")
        """Number of retries for failed health checks."""
        self.health_check_start_period: Optional[int] = data.get("health_check_start_period")
        """Start period for health checks in seconds."""
        self.limits_memory: Optional[str] = data.get("limits_memory")
        """Memory limit for the application or container."""
        self.limits_memory_swap: Optional[str] = data.get("limits_memory_swap")
        """Memory swap limit for the application or container."""
        self.limits_memory_swappiness: Optional[int] = data.get("limits_memory_swappiness")
        """Swappiness value for application memory."""
        self.limits_memory_reservation: Optional[str] = data.get("limits_memory_reservation")
        """Memory reservation setting for the application."""
        self.limits_cpus: Optional[str] = data.get("limits_cpus")
        """Limits on CPU usage for the application."""
        self.limits_cpuset: Optional[str] = data.get("limits_cpuset")
        """CPU set used by the application."""
        self.limits_cpu_shares: Optional[int] = data.get("limits_cpu_shares")
        """CPU shares allotted to the application."""
        self.status: Optional[str] = data.get("status")
        """Current status of the application."""
        self.preview_url_template: Optional[str] = data.get("preview_url_template")
        """Template for application preview URLs."""
        self.destination_type: Optional[str] = data.get("destination_type")
        """Type of deployment destination, e.g., Kubernetes, Docker."""
        self.destination_id: Optional[int] = data.get("destination_id")
        """ID of the deployment destination."""
        self.source_id: Optional[int] = data.get("source_id")
        """ID of the source configuration."""
        self.private_key_id: Optional[int] = data.get("private_key_id")
        """ID of the private key used for deployment, if any."""
        self.environment_id: Optional[int] = data.get("environment_id")
        """Environment ID where the application is deployed."""
        self.dockerfile: Optional[str] = data.get("dockerfile")
        """Contents of the Dockerfile used for building the application."""
        self.dockerfile_location: Optional[str] = data.get("dockerfile_location")
        """Location of the Dockerfile if applicable."""
        self.dockerfile_target_build: Optional[str] = data.get("dockerfile_target_build")
        """Target build in the Dockerfile."""
        self.custom_labels: Optional[str] = data.get("custom_labels")
        """Custom labels attached to the application."""
        self.manual_webhook_secret_github: Optional[str] = data.get("manual_webhook_secret_github")
        """Manual GitHub webhook secret."""
        self.manual_webhook_secret_gitlab: Optional[str] = data.get("manual_webhook_secret_gitlab")
        """Manual GitLab webhook secret."""
        self.manual_webhook_secret_bitbucket: Optional[str] = data.get("manual_webhook_secret_bitbucket")
        """Manual Bitbucket webhook secret."""
        self.manual_webhook_secret_gitea: Optional[str] = data.get("manual_webhook_secret_gitea")
        """Manual Gitea webhook secret."""
        self.docker_compose_location: Optional[str] = data.get("docker_compose_location")
        """Location of the Docker Compose file."""
        self.docker_compose: Optional[str] = data.get("docker_compose")
        """Contents of the Docker Compose file."""
        self.docker_compose_raw: Optional[str] = data.get("docker_compose_raw")
        """Raw Docker Compose file contents."""
        self.docker_compose_domains: Optional[str] = data.get("docker_compose_domains")
        """Domains listed in the Docker Compose configuration."""
        self.docker_compose_custom_start_command: Optional[str] = data.get(
            "docker_compose_custom_start_command")
        """Custom start command for Docker Compose."""
        self.docker_compose_custom_build_command: Optional[str] = data.get(
            "docker_compose_custom_build_command")
        """Custom build command for Docker Compose."""
        self.swarm_replicas: Optional[int] = data.get("swarm_replicas")
        """Number of replicas in a Docker Swarm deployment."""
        self.swarm_placement_constraints: Optional[str] = data.get("swarm_placement_constraints")
        """Placement constraints for Swarm nodes."""
        self.custom_docker_run_options: Optional[str] = data.get("custom_docker_run_options")
        """Custom options for `docker run` command."""
        self.post_deployment_command: Optional[str] = data.get("post_deployment_command")
        """Command to be run after deployment."""
        self.post_deployment_command_container: Optional[str] = data.get(
            "post_deployment_command_container")
        """Container where the post-deployment command runs."""
        self.pre_deployment_command: Optional[str] = data.get("pre_deployment_command")
        """Command to be run before deployment."""
        self.pre_deployment_command_container: Optional[str] = data.get(
            "pre_deployment_command_container")
        """Container where the pre-deployment command runs."""
        self.watch_paths: Optional[str] = data.get("watch_paths")
        """Paths watched for changes."""
        self.custom_healthcheck_found: Optional[bool] = data.get("custom_healthcheck_found")
        """Indicates if a custom health check is defined."""
        self.redirect: Optional[str] = data.get("redirect")
        """Redirect URL settings."""
        self.created_at: Optional[datetime] = data.get("created_at")
        """Datetime when the resource was created."""
        self.updated_at: Optional[datetime] = data.get("updated_at")
        """Datetime when the resource was last updated."""
        self.deleted_at: Optional[datetime] = data.get("deleted_at")
        """Datetime when the resource was deleted."""
        self.compose_parsing_version: Optional[str] = data.get("compose_parsing_version")
        """Version of Docker Compose parsing being used."""
        self.custom_nginx_configuration: Optional[str] = data.get("custom_nginx_configuration")
        """Custom NGINX configuration file."""

