"""Coolify API Client module for interacting with the Coolify API.

This module provides the main client class for interacting with various Coolify API endpoints.
It handles authentication and provides access to different API resources through dedicated classes.

Environment Variables:
    COOLIFY_BASE_URL: Base URL for the Coolify API (default: https://app.coolify.io)
    COOLIFY_API_KEY: API key for authentication
"""
import os
import logging

from ._http_utils import HTTPUtils
from .applications import CoolifyApplications
from .databases import CoolifyDatabases
from .deployments import CoolifyDeployments
from .operations import CoolifyOperations
from .private_keys import CoolifyPrivateKeys
from .projects import CoolifyProjects
from .resources import CoolifyResources
from .servers import CoolifyServers
from .services import CoolifyServices
from .teams import CoolifyTeams


class CoolifyAPIClient:
    """Main client class for interacting with the Coolify API.
    
    This class serves as the main entry point for interacting with various Coolify API endpoints.
    It initializes all the specialized API clients for different resources (applications, databases,
    etc.) and handles authentication.

    Attributes:
        applications (CoolifyApplications): Client for applications API endpoints
        databases (CoolifyDatabases): Client for databases API endpoints
        deployments (CoolifyDeployments): Client for deployments API endpoints
        operations (CoolifyOperations): Client for operations API endpoints
        private_keys (CoolifyPrivateKeys): Client for private keys API endpoints
        projects (CoolifyProjects): Client for projects API endpoints
        resources (CoolifyResources): Client for resources API endpoints
        servers (CoolifyServers): Client for servers API endpoints
        services (CoolifyServices): Client for services API endpoints
        teams (CoolifyTeams): Client for teams API endpoints

    Args:
        base_url (str, optional): Base URL for the Coolify API. 
            Defaults to COOLIFY_API_URL env var or https://app.coolify.io
        api_key (str, optional): API key for authentication. 
            Defaults to COOLIFY_API_KEY env var
    """

    _logger = logging.getLogger(__name__)
    COOLIFY_API_URL = os.getenv("COOLIFY_API_URL", "https://app.coolify.io")
    COOLIFY_API_KEY = os.getenv("COOLIFY_API_KEY")

    def __init__(self, api_url: str = COOLIFY_API_URL, api_key: str = COOLIFY_API_KEY):
        """Initialize the Coolify API client.

        Args:
            api_url: Base URL for the Coolify API
            api_key: API key for authentication

        Raises:
            ValueError: If api_key is not provided either as argument or environment variable
        """
        if not api_key:
            raise ValueError("API key must be provided either as argument or COOLIFY_API_KEY env var")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        http_tools: HTTPUtils = HTTPUtils(api_url, headers)

        self.applications: CoolifyApplications = CoolifyApplications(http_tools)
        """Client for working with the applications API."""
        self.databases: CoolifyDatabases = CoolifyDatabases(http_tools)
        """Client for working with the databases API."""
        self.deployments: CoolifyDeployments = CoolifyDeployments(http_tools)
        """Client for working with the deployments API."""
        self.operations: CoolifyOperations = CoolifyOperations(http_tools)
        """Client for working with the operations API."""
        self.private_keys: CoolifyPrivateKeys = CoolifyPrivateKeys(http_tools)
        """Client for working with the private keys API."""
        self.projects: CoolifyProjects = CoolifyProjects(http_tools)
        """Client for working with the projects API."""
        self.resources: CoolifyResources = CoolifyResources(http_tools)
        """Client for working with the resources API."""
        self.servers: CoolifyServers = CoolifyServers(http_tools)
        """Client for working with the servers API."""
        self.services: CoolifyServices = CoolifyServices(http_tools)
        """Client for working with the services API."""
        self.teams: CoolifyTeams = CoolifyTeams(http_tools)
        """Client for working with the teams API."""
