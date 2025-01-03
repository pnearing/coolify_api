"""Filename: coolify_api/databases_create.py"""
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
from .url_utils import post
import _utils


class CoolifyDatabasesCreate:
    """
    Handles the creation of various types of databases using Coolify's API.

    Provides methods to create PostgreSQL, MySQL, MongoDB, and Redis databases.
    Utilizes asynchronous HTTP calls to interact with Coolify's API and offers
    a structured way to handle database creation with optional data input
    and logging support.

    :ivar _base_url: Base URL used for API communication.
    :type _base_url: str
    :ivar _headers: Headers used for API requests.
    :type _headers: dict
    :ivar _logger: Logger instance for recording debug information.
    :type _logger: logging.Logger
    """
    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        """Base URL for the class."""
        self._headers = headers
        """Headers for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

    ###############
    # PostgreSQL Database
    async def _postgresql(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a PostgreSQL database.", data)
        endpoint = "databases/postgresql"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a PostgreSQL database")
        return results

    def postgresql(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._postgresql(real_data)
        except RuntimeError:
            return asyncio.run(self._postgresql(real_data))

    ###############
    # Clickhouse Database:
    async def _clickhouse(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a ClickHouse database.", data)
        endpoint = "databases/clickhouse"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a ClickHouse database")
        return results

    def clickhouse(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._clickhouse(real_data)
        except RuntimeError:
            return asyncio.run(self._clickhouse(real_data))

    ########################
    # DragonFly Database:
    async def _dragonfly(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a DragonFly database.", data)
        endpoint = "databases/dragonfly"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a DragonFly database")
        return results

    def dragonfly(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._dragonfly(real_data)
        except RuntimeError:
            return asyncio.run(self._dragonfly(real_data))

    ###############
    # Redis Database
    async def _redis(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a Redis database.", data)
        endpoint = "databases/redis"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Redis database")
        return results

    def redis(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._redis(real_data)
        except RuntimeError:
            return asyncio.run(self._redis(real_data))

    #################
    # KeyDB Database:
    async def _keydb(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a KeyDB database.", data)
        endpoint = "databases/keydb"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a KeyDB database")
        return results

    def keydb(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._keydb(real_data)
        except RuntimeError:
            return asyncio.run(self._keydb(real_data))

    #####################
    # MariaDB Database:
    async def _mariadb(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a MariaDB database.", data)
        endpoint = "databases/mariadb"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MariaDB database")
        return results

    def mariadb(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._mariadb(real_data)
        except RuntimeError:
            return asyncio.run(self._mariadb(real_data))

    ###############
    # MySQL Database
    async def _mysql(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a MySQL database.", data)
        endpoint = "databases/mysql"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MySQL database")
        return results

    def mysql(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._mysql(real_data)
        except RuntimeError:
            return asyncio.run(self._mysql(real_data))

    ###############
    # MongoDB Database
    async def _mongodb(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start to create a MongoDB database.", data)
        endpoint = "databases/mongodb"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a MongoDB database")
        return results

    def mongodb(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._mongodb(real_data)
        except RuntimeError:
            return asyncio.run(self._mongodb(real_data))
