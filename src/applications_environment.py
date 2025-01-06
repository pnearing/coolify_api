"""File: coolify_api/applications_environment.py"""
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
from logging import getLogger, DEBUG
from typing import Any, Optional, Coroutine

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyApplicationEnvVars:
    def __init__(self, http_utils: HTTPUtils) -> None:
        self._http_utils: HTTPUtils = http_utils
        """HTTP client for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

    ###############
    # List:
    def list_all(self, application_uuid: str
                 ) -> list[dict[str, Any]] | Coroutine[Any, Any, list[dict[str, Any]]]:
        message = f"Start to list vars for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"applications/{application_uuid}/envs")
        message = f"Finish listing vars for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    #################
    # Create:
    def create(self, application_uuid: str, data: dict[str, Any], **kwargs
               ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to create var for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post(f"applications/{application_uuid}/envs", data=data)
        message = f"Finish creating var for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ################
    # Update singe:
    def update(self, application_uuid: str, data: dict[str, Any], **kwargs
               ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update var for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"applications/{application_uuid}/envs", data=data)
        message = f"Finish updating var for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    #############
    # Update Multiple:
    def update_bulk(self, application_uuid: str, data: list[dict[str, Any]]
                    ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        message = f"Start to bulk update vars for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"applications/{application_uuid}/envs", data=data)
        message = f"Finish bulk updating vars for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ############
    # Delete:
    def delete(self, application_uuid: str, variable_uuid: str) -> dict | Coroutine[Any, Any, dict]:
        message = f"Start delete var {variable_uuid} for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(f"applications/{application_uuid}/envs/{variable_uuid}")
        message = f"Finish delete var {variable_uuid} for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
