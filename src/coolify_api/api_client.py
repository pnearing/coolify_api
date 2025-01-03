"""File: coolify_api/api_client.py"""
#  Copyright (c) 2024.
#
#  Proprietary License
#
#  management-tool License Agreement
#
#  Permission is hereby granted, to any person contracted with Rapid Dev Group to
#  use this software and associated documentation files (the "Software"), to use
#  the Software for personal and commercial purposes, subject to the following
#  conditions:
#
#  1. Redistribution and use in source and binary forms, with or without
#     modification, are not permitted.
#  2. The Software shall be used for Good, not Evil.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Contact: pn@goldeverywhere.com
import os
import logging

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
    """Main class for interacting with the Coolify API."""
    _logger = logging.getLogger(__name__)
    COOLIFY_BASE_URL = os.getenv("COOLIFY_BASE_URL")
    COOLIFY_API_KEY = os.getenv("COOLIFY_API_KEY")

    def __init__(self, base_url: str = COOLIFY_BASE_URL, api_key: str = COOLIFY_API_KEY):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.applications: CoolifyApplications = CoolifyApplications(base_url, headers)
        """Work with the applications API."""
        self.databases: CoolifyDatabases = CoolifyDatabases(base_url, headers)
        """Work with the databases API."""
        self.deployments: CoolifyDeployments = CoolifyDeployments(base_url, headers)
        """Work with the deployments API."""
        self.operations: CoolifyOperations = CoolifyOperations(base_url, headers)
        """Work with the operations API."""
        self.private_keys: CoolifyPrivateKeys = CoolifyPrivateKeys(base_url, headers)
        """Work with the private keys API."""
        self.projects: CoolifyProjects = CoolifyProjects(base_url, headers)
        """Work with the projects API."""
        self.resources: CoolifyResources = CoolifyResources(base_url, headers)
        """Work with the resources API."""
        self.servers: CoolifyServers = CoolifyServers(base_url, headers)
        """Work with the servers API."""
        self.services: CoolifyServices = CoolifyServices(base_url, headers)
        """Work with the services API."""
        self.teams: CoolifyTeams = CoolifyTeams(base_url, headers)
        """Work with the teams API."""
