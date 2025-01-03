"""File: coolify_api/operations.py"""
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
from typing import Any
from ._logging import _log_message
from .url_utils import get


class CoolifyOperations:
    _logger = getLogger(__name__)

    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self._base_url: str = base_url
        self._headers: dict[str, str] = headers

    async def _get_version(self) -> str:
        _log_message(self._logger, DEBUG, "Start getting version")
        endpoint = "version"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish getting version")
        return results

    def get_version(self) -> str:
        try:
            _ = asyncio.get_running_loop()
            return self._get_version()
        except RuntimeError:
            return asyncio.run(self._get_version())

    async def _enable_api(self) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start enabling API")
        endpoint = "operations/enable-api"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish enabling API")
        return results

    def enable_api(self) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._enable_api()
        except RuntimeError:
            return asyncio.run(self._enable_api())

    async def _disable_api(self) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start disabling API")
        endpoint = "operations/disable-api"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish disabling API")
        return results

    def disable_api(self) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._disable_api()
        except RuntimeError:
            return asyncio.run(self._disable_api())

    async def _health_check(self) -> str:
        _log_message(self._logger, DEBUG, "Start health check")
        endpoint = "operations/healthcheck"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish health check")
        return results

    def health_check(self) -> str:
        try:
            _ = asyncio.get_running_loop()
            return self._health_check()
        except RuntimeError:
            return asyncio.run(self._health_check())
