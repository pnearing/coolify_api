"""File: coolify_api/servers.py"""
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

import _utils as utils
from ._logging import _log_message
from .url_utils import get, post, patch, delete


class CoolifyServers:

    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        self._headers = headers
        self._logger = getLogger(__name__)

    #################
    # LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start to list all servers")
        endpoint = "servers"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all servers")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    # GET:
    async def _get(self, server_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to get server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting server with id: {server_uuid}")
        return results

    def get(self, server_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(server_uuid)
        except RuntimeError:
            return asyncio.run(self._get(server_uuid))

    # CREATE:
    async def _create(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to create a new server")
        endpoint = "servers"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating a new server")
        return results

    def create(self, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._create(real_data)
        except RuntimeError:
            return asyncio.run(self._create(real_data))

    # UPDATE:
    async def _update(self, server_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating server with id: {server_uuid}")
        return results

    def update(self, server_uuid: str, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(server_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(server_uuid, real_data))

    # DELETE:
    async def _delete(self, server_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to delete server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}"
        results = delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish deleting server with id: {server_uuid}")
        return results

    def delete(self, server_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(server_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(server_uuid))

    # GET resources:
    async def _resources(self, server_uuid: str) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, f"Start to get resources of a server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}/resources"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG,
                     f"Finish getting resources of a server with id: {server_uuid}")
        return results

    def resources(self, server_uuid: str) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._resources(server_uuid)
        except RuntimeError:
            return asyncio.run(self._resources(server_uuid))

    # GET domains:
    async def _domains(self, server_uuid: str) -> list[dict[str, Any]]:
        """Retrieving domains of a server asynchronously."""
        _log_message(self._logger, DEBUG, f"Start to get domains of a server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}/domains"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting domains of a server with id: {server_uuid}")
        return results


    def domains(self, server_uuid: str) -> list[dict[str, Any]]:
        """
            Execute the _domains function asynchronously or synchronously
            depending on the environment.
            """
        try:
            _ = asyncio.get_running_loop()
            return self._domains(server_uuid)
        except RuntimeError:
            return asyncio.run(self._domains(server_uuid))

    # VALIDATE server:
    async def _validate(self, server_uuid: str) -> dict[str, Any]:
        """Perform server validation asynchronously."""
        _log_message(self._logger, DEBUG, f"Start to validate a server with id: {server_uuid}")
        endpoint = f"servers/{server_uuid}/validate"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish validating server with id: {server_uuid}")
        return results

    def validate(self, server_uuid: str) -> dict[str, Any]:
        """
        Execute the _validate function asynchronously or synchronously
        depending on the environment.
        """
        try:
            _ = asyncio.get_running_loop()
            return self._validate(server_uuid)
        except RuntimeError:
            return asyncio.run(self._validate(server_uuid))
