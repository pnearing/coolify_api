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
"""coolify_api/services.py"""
import asyncio
from logging import getLogger, DEBUG
from typing import Optional, Any

import _utils as utils
from ._logging import _log_message
from .url_utils import get, post, patch, delete
from .services_environment import CoolifyServicesEnvVars


class CoolifyServices:

    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        """The base url for the Coolify API."""
        self._headers = headers
        """The headers for the Coolify API, contain auth data."""
        self._logger = getLogger(__name__)
        """The logger for the Coolify API."""
        self.environment: CoolifyServicesEnvVars = CoolifyServicesEnvVars(self._base_url, self._headers)
        """The environment for the services."""

    # LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start to list all services")
        endpoint = "services"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all services")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    # GET:
    async def _get(self, service_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to get service with id: {service_uuid}")
        endpoint = f"services/{service_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting service with id: {service_uuid}")
        return results

    def get(self, service_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(service_uuid)
        except RuntimeError:
            return asyncio.run(self._get(service_uuid))

    # CREATE:
    async def _create(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to create a new service")
        endpoint = "services"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating a new service")
        return results

    def create(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._create(real_data)
        except RuntimeError:
            return asyncio.run(self._create(real_data))

    # UPDATE:
    async def _update(self, service_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update service with id: {service_uuid}")
        endpoint = f"services/{service_uuid}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating service with id: {service_uuid}")
        return results

    def update(self, service_uuid: str, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(service_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(service_uuid, real_data))

    # DELETE:
    async def _delete(self, service_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to delete service with id: {service_uuid}")
        endpoint = f"services/{service_uuid}"
        results = delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish deleting service with id: {service_uuid}")
        return results

    def delete(self, service_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(service_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(service_uuid))

    # START:
    async def _start(self, service_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Starting service with service_id: {service_uuid}")
        endpoint = f"services/{service_uuid}/start"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG,
                     f"Finish starting service with service_id: {service_uuid}")
        return results

    def start(self, service_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._start(service_uuid)
        except RuntimeError:
            return asyncio.run(self._start(service_uuid))

    # STOP:
    async def _stop(self, service_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Stopping service with service_id: {service_uuid}")
        endpoint = f"services/{service_uuid}/stop"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG,
                     f"Finish stopping service with service_id: {service_uuid}")
        return results

    def stop(self, service_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._stop(service_uuid)
        except RuntimeError:
            return asyncio.run(self._stop(service_uuid))

    # RESTART:
    async def _restart(self, service_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Restarting service with service_id: {service_uuid}")
        endpoint = f"services/{service_uuid}/restart"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG,
                     f"Finish restarting service with service_id: {service_uuid}")
        return results

    def restart(self, service_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._restart(service_uuid)
        except RuntimeError:
            return asyncio.run(self._restart(service_uuid))
