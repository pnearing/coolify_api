"""File: coolify_api/projects.py"""
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
from logging import getLogger, DEBUG
from typing import Optional, Any

import _utils as utils
from ._logging import _log_message
from .url_utils import get, post, patch, delete


class CoolifyProjects:

    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        self._headers = headers
        self._logger = getLogger(__name__)

    # LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start to list all projects")
        endpoint = "projects"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all projects")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    # GET:
    async def _get(self, project_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to get project with id: {project_uuid}")
        endpoint = f"projects/{project_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting project with id: {project_uuid}")
        return results

    def get(self, project_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(project_uuid)
        except RuntimeError:
            return asyncio.run(self._get(project_uuid))

    # CREATE:
    async def _create(self, data: dict[str, Any]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to create a new project")
        endpoint = "projects"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating a new project")
        return results

    def create(self, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._create(real_data)
        except RuntimeError:
            return asyncio.run(self._create(real_data))

    # UPDATE:
    async def _update(self, project_uuid: str, data: Optional[dict[str, Any]]) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to update project with id: {project_uuid}")
        endpoint = f"projects/{project_uuid}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating project with id: {project_uuid}")
        return results

    def update(self, project_uuid: str, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(project_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(project_uuid, real_data))

    # DELETE:
    async def _delete(self, project_uuid: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start to delete project with id: {project_uuid}")
        endpoint = f"projects/{project_uuid}"
        results = delete(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish deleting project with id: {project_uuid}")
        return results

    def delete(self, project_uuid: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._delete(project_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(project_uuid))
