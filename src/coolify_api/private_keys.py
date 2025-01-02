"""File: coolify_api/private_keys.py"""
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

import coolify_api.utils as utils
from coolify_api._logging import _log_message
from coolify_api.url_utils import get, post, patch, delete


class CoolifyPrivateKeys:
    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        self._headers = headers
        self._logger = getLogger(__name__)

    # LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start to list all private keys")
        endpoint = "security/keys"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all private keys")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    #############
    # GET:
    async def _get(self, key_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to get private key with id: {key_uuid}")
        endpoint = f"security/keys/{key_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting private key with id: {key_uuid}")
        return results

    def get(self, private_key_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(private_key_uuid)
        except RuntimeError:
            return asyncio.run(self._get(private_key_uuid))

    #################
    # CREATE:
    async def _create(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to create a new private key")
        endpoint = "security/keys"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating a new private key")
        return results

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._create(data)
        except RuntimeError:
            return asyncio.run(self._create(data))

    #################
    # UPDATE:
    async def _update(self, key_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update key with id: {key_uuid}")
        endpoint = f"security/keys/{key_uuid}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating key with id: {key_uuid}")
        return results

    def update(self, key_uuid: str, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(key_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(key_uuid, real_data))

    #####################
    # DELETE:
    async def _delete(self, key_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to delete key with id: {key_uuid}")
        endpoint = f"security/keys/{key_uuid}"
        results = delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish deleting key with id: {key_uuid}")
        return results


    def delete(self, key_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(key_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(key_uuid))