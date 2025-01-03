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
import asyncio
from logging import getLogger, DEBUG
from typing import Optional, Any

from ._logging import _log_message
from .url_utils import get, post


class CoolifyDeployments:
    """
    Manages Coolify deployments, providing methods to perform operations such
    as listing, retrieving, and deploying deployments.
    """

    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        self._headers = headers
        self._logger = getLogger(__name__)

    # LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        """ Asynchronously retrieves a list of all deployments from the specified endpoint. """

        _log_message(self._logger, DEBUG, "Start to list all deployments")
        endpoint = "deployments"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all deployments")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        """ Lists all elements asynchronously or synchronously based on the running environment. """

        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    # GET:
    async def _get(self, deployment_uuid: str) -> dict[str, Any]:
        """ Fetches deployment information asynchronously based on the provided UUID. """

        _log_message(self._logger, DEBUG, f"Start to get deployment with id: {deployment_uuid}")
        endpoint = f"deployments/{deployment_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting deployment with id: {deployment_uuid}")
        return results

    def get(self, deployment_uuid: str) -> dict[str, Any]:
        """ Retrieve deployment details based on the UUID provided. """

        try:
            _ = asyncio.get_running_loop()
            return self._get(deployment_uuid)
        except RuntimeError:
            return asyncio.run(self._get(deployment_uuid))

    ###################
    # DEPLOY:
    async def _deploy(self,
                      deployment_uuid: Optional[str] = None,
                      tag: Optional[str] = None,
                      ) -> dict[str, Any]:
        """ Deploy a current deployment asynchronously using its deployment UUID. """
        if deployment_uuid is None and tag is None:
            raise AttributeError("Either deployment_uuid or tag must be specified")
        params = {}
        if deployment_uuid:
            params["uuid"] = deployment_uuid
        if tag:
            params["tag"] = tag
        _log_message(self._logger, DEBUG, f"Start to deploy deployment with params: {params}")
        endpoint = "deployments"
        results = post(self._base_url, endpoint, headers=self._headers, params=params)
        _log_message(self._logger, DEBUG, f"Finish deploying deployment.")
        return results

    def deploy(self, deployment_uuid: str) -> dict[str, Any]:
        """ Deploys deployment using deployment UUID. """
        try:
            _ = asyncio.get_running_loop()
            return self._deploy(deployment_uuid)
        except RuntimeError:
            return asyncio.run(self._deploy(deployment_uuid))