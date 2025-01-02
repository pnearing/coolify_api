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
#

from logging import getLogger, DEBUG
from coolify_api._logging import _log_message
from coolify_api.url_utils import _get, _post, _delete, _patch


class CoolifyEnvironmentVariables:

    def __init__(self, base_url: str, headers: dict, base_endpoint: str) -> None:
        self._base_url = base_url
        """Base URL for the class."""
        self._headers = headers
        """Headers for the class."""
        self._base_endpoint = base_endpoint
        """Base endpoint for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

    async def list_all(self) -> list[dict]:
        _log_message(self._logger, DEBUG, "Listing all environment variables")
        endpoint = f"{self._base_endpoint}/envs"
        results = await _get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finished listing environment variables")
        return results

    async def get(self, variable_uuid: str) -> dict:
        _log_message(self._logger, DEBUG, f"Getting environment variable: {variable_uuid}")
        endpoint = f"{self._base_endpoint}/envs/{variable_uuid}"
        results = await _get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finished getting environment variable: {variable_uuid}")
        return results

    async def create(self, data: dict = {}, **kwargs) -> dict:
        _log_message(self._logger, DEBUG, f"Creating environment variable", data)
        endpoint = f"{self._base_endpoint}/envs"
        if kwargs:
            data.update(kwargs)
        results = await _post(self._base_url, endpoint, self._headers, data)
        _log_message(self._logger)
        return results

    async def update(self, variable_uuid: str, data: dict = {}, **kwargs) -> dict:
        _log_message(self._logger, DEBUG, f"Updating environment variable: {variable_uuid}", data)
        endpoint = f"{self._base_endpoint}/envs/{variable_uuid}"
        if kwargs:
            data.update(kwargs)
        results = await _patch(self._base_url, endpoint, self._headers, data)
        _log_message(self._logger, DEBUG, f"Finished updating environment variable: {variable_uuid}")
        return results

    async def delete(self, variable_uuid: str) -> dict:
        _log_message(self._logger, DEBUG, f"Deleting environment variable: {variable_uuid}")
        endpoint = f"{self._base_endpoint}/envs/{variable_uuid}"
        results = await _delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finished deleting environment variable: {variable_uuid}")
        return results
