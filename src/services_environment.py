"""File: coolify_api/services_environment.py"""
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
from typing import Optional, Any, Coroutine

from ._utils import create_data_with_kwargs
from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyServicesEnvVars:
    def __init__(self, http_utils: HTTPUtils) -> None:
        self._http_utils: HTTPUtils = http_utils
        """HTTPUtils instance for making HTTP requests."""
        self._logger = getLogger(__name__)
        """The logger for the class."""

    ##################
    # List:
    def list_all(self, service_uuid: str
                 ) -> list[dict[str, Any]] | Coroutine[Any, Any, list[dict[str, Any]]]:
        message = f"Start to list vars for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"services/{service_uuid}/envs")
        message = f"Finish listing vars for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ####################
    # Create:
    def create(self, service_uuid: str, data: dict[str, Any], **kwargs
               ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to create var for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.post(f"services/{service_uuid}/envs", data=data)
        message = f"Finish creating var for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ##################
    # Update:
    def update(self, service_uuid: str, data: dict[str, Any], **kwargs
               ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        data = create_data_with_kwargs(data, **kwargs)
        message = f"Start to update var for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"services/{service_uuid}/envs", data=data)
        message = f"Finish updating var for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ###############
    # Update Bulk:
    def update_bulk(self, service_uuid: str, data: list[dict[str, Any]]
                    ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        message = f"Start to bulk update vars for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        results = self._http_utils.patch(f"services/{service_uuid}/envs", data=data)
        message = f"Finish bulk updating vars for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    ###################
    # Delete:
    def delete(self, service_uuid: str, variable_uuid: str
               ) -> dict[str, Any] | Coroutine[Any, Any, dict[str, Any]]:
        message = f"Start delete var {variable_uuid} for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.delete(f"services/{service_uuid}/envs/{variable_uuid}")
        message = f"Finish delete var {variable_uuid} for service_id: {service_uuid}"
        _log_message(self._logger, DEBUG, message, results)
        return results
