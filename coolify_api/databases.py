"""File: coolify_api/databases.py"""
#   Copyright (c) 2024.
#
#   Proprietary License
#
#   management-tool License Agreement
#
#   Permission is hereby granted, to any person contracted with Rapid Dev Group to
#   use this software and associated documentation files (the "Software"), to use
#   the Software for personal and commercial purposes, subject to the following
#   conditions:
#
#   1. Redistribution and use in source and binary forms, with or without
#      modification, are not permitted.
#   2. The Software shall be used for Good, not Evil.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#
#   Contact: pn@goldeverywhere.com
#
import asyncio
from typing import Any, Optional
from logging import getLogger, DEBUG

import coolify_api.utils as utils
from coolify_api.url_utils import get, patch, delete
from coolify_api._logging import _log_message
from coolify_api.databases_create import CoolifyDatabasesCreate


class CoolifyDatabases:
    """
    Manages Coolify databases, providing methods to perform synchronous and
    asynchronous operations such as listing, retrieving, updating, and deleting
    databases with Coolify backend API.

    :ivar create: Provides methods for creating Coolify databases.
    :type create: CoolifyDatabasesCreate
    """

    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        self._headers = headers
        self.create: CoolifyDatabasesCreate = CoolifyDatabasesCreate(base_url, headers)
        self._logger = getLogger(__name__)

    # Asynchronous version of list_all
    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start to list all databases")
        endpoint = "databases"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all databases")
        return results

    # Synchronous wrapper for list_all
    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    async def _get(self, database_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to get database with id: {database_id}")
        endpoint = f"databases/{database_id}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting database with id: {database_id}")
        return results

    def get(self, database_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(database_id)
        except RuntimeError:
            return asyncio.run(self._get(database_id))

    async def _delete(self, database_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to delete database with id: {database_id}")
        endpoint = f"databases/{database_id}"
        results = delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish deleting database with id: {database_id}")
        return results

    def delete(self, database_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(database_id)
        except RuntimeError:
            return asyncio.run(self._delete(database_id))

    async def _update(self, database_id: str, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update database with id: {database_id}")
        endpoint = f"databases/{database_id}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating database with id: {database_id}")
        return results

    def update(self, database_id: str, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(database_id, real_data)
        except RuntimeError:
            return asyncio.run(self._update(database_id, real_data))

    async def _start(self, database_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start database with id: {database_id}")
        endpoint = f"databases/{database_id}/start"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish starting database with id: {database_id}")
        return results

    def start(self, database_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._start(database_id)
        except RuntimeError:
            return asyncio.run(self._start(database_id))

    async def _stop(self, database_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Stop database with id: {database_id}")
        endpoint = f"databases/{database_id}/stop"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish stopping database with id: {database_id}")
        return results

    def stop(self, database_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._stop(database_id)
        except RuntimeError:
            return asyncio.run(self._stop(database_id))

    async def _restart(self, database_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Restart database with id: {database_id}")
        endpoint = f"databases/{database_id}/restart"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish restarting database with id: {database_id}")
        return results

    def restart(self, database_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._restart(database_id)
        except RuntimeError:
            return asyncio.run(self._restart(database_id))
