#   Copyright (c) 2024.
#  #
#   Proprietary License
#  #
#   management-tool License Agreement
#  #
#   Permission is hereby granted, to any person contracted with Rapid Dev Group to
#   use this software and associated documentation files (the "Software"), to use
#   the Software for personal and commercial purposes, subject to the following
#   conditions:
#  #
#   1. Redistribution and use in source and binary forms, with or without
#      modification, are not permitted.
#   2. The Software shall be used for Good, not Evil.
#  #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#  #
#   Contact: pn@goldeverywhere.com
#
from typing import Optional
from datetime import datetime
from logging import getLogger, DEBUG

from coolify_api import CoolifyAPIClient

from coolify_api._logging import _log_message
from coolify_api.url_utils import delete, get, patch, post


class CoolifyApplication:
    """
     Initialize an Application object.

     Parameters:
     - api_client (CoolifyApiClient): An instance of CoolifyApiClient to interact with the API.
     - application_uuid (str): The UUID of the application.
     """

    async def populate(self, data: dict) -> None:
        data = await self._client.applications.get(self._application_uuid)
        self.__dict__.update(data)
        return

    def __init__(self,
                 client: CoolifyAPIClient,
                 application_uuid: str,
                 do_load: bool = True,
                 ) -> None:
        self._client: CoolifyAPIClient = client
        """CoolifyAPIClient for the class."""
        self._application_uuid = application_uuid
        """Application UUID for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

        data = {}
        if do_load:
            data = client.applications.get(application_uuid)

        self.id: Optional[int] = data.get("id", None)
        """Unique identifier for the resource."""
        self.repository_project_id: Optional[int] = data.get("repository_project_id", None)
        """ID for the repository project associated with this resource."""
        self.description: Optional[str] = data.get("description", None)
        """Description of the resource."""
        self.uuid: Optional[str] = data.get("uuid", None)
        """Universally Unique Identifier (UUID) for the resource."""
        self.name: Optional[str] = data.get("name", None)
        """Name of the application or resource."""
        self.fqdn: Optional[str] = data.get("fqdn", None)
        """Fully Qualified Domain Name (FQDN) of the application."""
        self.config_hash: Optional[str] = data.get("config_hash", None)
        """Hash representing the configuration of the application."""
        self.git_repository: Optional[str] = data.get("git_repository", None)
        """URL of the associated Git repository."""
        self.git_branch: Optional[str] = data.get("git_branch", None)
        """Branch of the Git repository being used."""
        self.git_commit_sha: Optional[str] = data.get("git_commit_sha", None)
        """Commit SHA from the Git repository."""
        self.git_full_url: Optional[str] = data.get("git_full_url", None)
        """Complete URL of the Git repository."""
        self.docker_registry_image_name: Optional[str] = data.get("docker_registry_image_name", None)
        """Name of the Docker registry image."""
        self.docker_registry_image_tag: Optional[str] = data.get("docker_registry_image_tag", None)
        """Tag of the Docker registry image."""
        self.build_pack: Optional[str] = data.get("build_pack", None)
        """Build pack used for the application."""
        self.static_image: Optional[str] = data.get("static_image", None)
        """Static image related to the application."""
        self.install_command: Optional[str] = data.get("install_command", None)
        """Command used to install dependencies."""
        self.build_command: Optional[str] = data.get("build_command", None)
        """Command used to build the application."""
        self.start_command: Optional[str] = data.get("start_command", None)
        """Command used to start the application."""
        self.ports_exposes: Optional[str] = data.get("ports_exposes", None)
        """Ports exposed by the application."""
        self.ports_mappings: Optional[str] = data.get("ports_mappings", None)
        """Mapping of ports for the application."""
        self.base_directory: Optional[str] = data.get("base_directory", None)
        """Base directory for the application files."""
        self.publish_directory: Optional[str] = data.get("publish_directory", None)
        """Directory where the application will be published."""
        self.health_check_enabled: Optional[bool] = data.get("health_check_enabled", None)
        """Indicates whether health checks are enabled for the application."""
        self.health_check_path: Optional[str] = data.get("health_check_path", None)
        """Path used for health checking."""
        self.health_check_port: Optional[str] = data.get("health_check_port", None)
        """Port used for health checking."""
        self.health_check_host: Optional[str] = data.get("health_check_host", None)
        """Host used for health checking."""
        self.health_check_method: Optional[str] = data.get("health_check_method", None)
        """HTTP method used for health checking."""
        self.health_check_return_code: Optional[int] = data.get("health_check_return_code", None)
        """Expected HTTP return code for successful health checks."""
        self.health_check_scheme: Optional[str] = data.get("health_check_scheme", None)
        """Scheme (e.g., HTTP or HTTPS) used for health checks."""
        self.health_check_response_text: Optional[str] = data.get("health_check_response_text", None)
        """Expected response text for successful health checks."""
        self.health_check_interval: Optional[int] = data.get("health_check_interval", None)
        """Interval in seconds between health checks."""
        self.health_check_timeout: Optional[int] = data.get("health_check_timeout", None)
        """Timeout in seconds for health checks."""
        self.health_check_retries: Optional[int] = data.get("health_check_retries", None)
        """Number of retries for failed health checks."""
        self.health_check_start_period: Optional[int] = data.get("health_check_start_period", None)
        """Start period for health checks in seconds."""
        self.limits_memory: Optional[str] = data.get("limits_memory", None)
        """Memory limit for the application or container."""
        self.limits_memory_swap: Optional[str] = data.get("limits_memory_swap", None)
        """Memory swap limit for the application or container."""
        self.limits_memory_swappiness: Optional[int] = data.get("limits_memory_swappiness", None)
        """Swappiness value for application memory."""
        self.limits_memory_reservation: Optional[str] = data.get("limits_memory_reservation", None)
        """Memory reservation setting for the application."""
        self.limits_cpus: Optional[str] = data.get("limits_cpus", None)
        """Limits on CPU usage for the application."""
        self.limits_cpuset: Optional[str] = data.get("limits_cpuset", None)
        """CPU set used by the application."""
        self.limits_cpu_shares: Optional[int] = data.get("limits_cpu_shares", None)
        """CPU shares allotted to the application."""
        self.status: Optional[str] = data.get("status", None)
        """Current status of the application."""
        self.preview_url_template: Optional[str] = data.get("preview_url_template", None)
        """Template for application preview URLs."""
        self.destination_type: Optional[str] = data.get("destination_type", None)
        """Type of deployment destination, e.g., Kubernetes, Docker."""
        self.destination_id: Optional[int] = data.get("destination_id", None)
        """ID of the deployment destination."""
        self.source_id: Optional[int] = data.get("source_id", None)
        """ID of the source configuration."""
        self.private_key_id: Optional[int] = data.get("private_key_id", None)
        """ID of the private key used for deployment, if any."""
        self.environment_id: Optional[int] = data.get("environment_id", None)
        """Environment ID where the application is deployed."""
        self.dockerfile: Optional[str] = data.get("dockerfile", None)
        """Contents of the Dockerfile used for building the application."""
        self.dockerfile_location: Optional[str] = data.get("dockerfile_location", None)
        """Location of the Dockerfile if applicable."""
        self.dockerfile_target_build: Optional[str] = data.get("dockerfile_target_build", None)
        """Target build in the Dockerfile."""
        self.custom_labels: Optional[str] = data.get("custom_labels", None)
        """Custom labels attached to the application."""
        self.manual_webhook_secret_github: Optional[str] = data.get("manual_webhook_secret_github", None)
        """Manual GitHub webhook secret."""
        self.manual_webhook_secret_gitlab: Optional[str] = data.get("manual_webhook_secret_gitlab", None)
        """Manual GitLab webhook secret."""
        self.manual_webhook_secret_bitbucket: Optional[str] = data.get("manual_webhook_secret_bitbucket",
                                                                       None)
        """Manual Bitbucket webhook secret."""
        self.manual_webhook_secret_gitea: Optional[str] = data.get("manual_webhook_secret_gitea", None)
        """Manual Gitea webhook secret."""
        self.docker_compose_location: Optional[str] = data.get("docker_compose_location", None)
        """Location of the Docker Compose file."""
        self.docker_compose: Optional[str] = data.get("docker_compose", None)
        """Contents of the Docker Compose file."""
        self.docker_compose_raw: Optional[str] = data.get("docker_compose_raw", None)
        """Raw Docker Compose file contents."""
        self.docker_compose_domains: Optional[str] = data.get("docker_compose_domains", None)
        """Domains listed in the Docker Compose configuration."""
        self.docker_compose_custom_start_command: Optional[str] = data.get(
            "docker_compose_custom_start_command", None)
        """Custom start command for Docker Compose."""
        self.docker_compose_custom_build_command: Optional[str] = data.get(
            "docker_compose_custom_build_command", None)
        """Custom build command for Docker Compose."""
        self.swarm_replicas: Optional[int] = data.get("swarm_replicas", None)
        """Number of replicas in a Docker Swarm deployment."""
        self.swarm_placement_constraints: Optional[str] = data.get("swarm_placement_constraints", None)
        """Placement constraints for Swarm nodes."""
        self.custom_docker_run_options: Optional[str] = data.get("custom_docker_run_options", None)
        """Custom options for `docker run` command."""
        self.post_deployment_command: Optional[str] = data.get("post_deployment_command", None)
        """Command to be run after deployment."""
        self.post_deployment_command_container: Optional[str] = data.get(
            "post_deployment_command_container", None)
        """Container where the post-deployment command runs."""
        self.pre_deployment_command: Optional[str] = data.get("pre_deployment_command", None)
        """Command to be run before deployment."""
        self.pre_deployment_command_container: Optional[str] = data.get("pre_deployment_command_container",
                                                                        None)
        """Container where the pre-deployment command runs."""
        self.watch_paths: Optional[str] = data.get("watch_paths", None)
        """Paths watched for changes."""
        self.custom_healthcheck_found: Optional[bool] = data.get("custom_healthcheck_found", None)
        """Indicates if a custom health check is defined."""
        self.redirect: Optional[str] = data.get("redirect", None)
        """Redirect URL settings."""
        self.created_at: Optional[datetime] = data.get("created_at", None)
        """Datetime when the resource was created."""
        self.updated_at: Optional[datetime] = data.get("updated_at", None)
        """Datetime when the resource was last updated."""
        self.deleted_at: Optional[datetime] = data.get("deleted_at", None)
        """Datetime when the resource was deleted."""
        self.compose_parsing_version: Optional[str] = data.get("compose_parsing_version", None)
        """Version of Docker Compose parsing being used."""
        self.custom_nginx_configuration: Optional[str] = data.get("custom_nginx_configuration", None)
        """Custom NGINX configuration file."""

