"""File: coolify_api/services_environment.py"""
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

import coolify_api.utils as utils
from coolify_api._logging import _log_message
from coolify_api.url_utils import get, post, patch, delete


class CoolifyServicesEnvVars:
    _logger = getLogger(__name__)

    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self._base_url: str = base_url
        self._headers: dict[str, str] = headers

    async def _list_all(self, service_uuid: str) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, f"Start to list vars for service_id: {service_uuid}")
        endpoint = f"services/{service_uuid}/envs"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish listing vars for service_id: {service_uuid}")
        return results

    def list_all(self, service_uuid: str) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all(service_uuid)
        except RuntimeError:
            return asyncio.run(self._list_all(service_uuid))

    async def _create(self, service_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to create var for service_id: {service_uuid}",
                     data)
        endpoint = f"services/{service_uuid}/envs"
        results = await post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating var for service_id: {service_uuid}")
        return results

    def create(self, service_uuid: str,
               data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._create(service_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._create(service_uuid, real_data))

    async def _update(self, service_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update var for service_id: {service_uuid}",
                     data)
        endpoint = f"services/{service_uuid}/envs"
        results = await patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating var for service_id: {service_uuid}")
        return results

    def update(self, service_uuid: str,
               data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(service_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(service_uuid, real_data))

    async def _update_bulk(self, service_uuid: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        message = f"Start to bulk update vars for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        endpoint = f"services/{service_uuid}/envs/bulk"
        results = await patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG,
                     f"Finish bulk updating vars for service_id: {service_uuid}")
        return results

    def update_bulk(self, service_uuid: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._update_bulk(service_uuid, data)
        except RuntimeError:
            return asyncio.run(self._update_bulk(service_uuid, data))

    async def _delete(self, service_uuid: str, variable_uuid: str) -> dict:
        message = f"Start delete var {variable_uuid} for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        endpoint = f"services/{service_uuid}/envs/{variable_uuid}"
        results = await delete(self._base_url, endpoint, self._headers)
        message = f"Finish delete var {variable_uuid} for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        return results

    def delete(self, service_uuid: str, variable_uuid: str) -> dict:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(service_uuid, variable_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(service_uuid, variable_uuid))#   Copyright (c) 2024.
