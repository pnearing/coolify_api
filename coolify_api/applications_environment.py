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
import asyncio
from logging import getLogger, DEBUG
from typing import Any, Optional

import coolify_api.utils as utils
from coolify_api._logging import _log_message
from coolify_api.url_utils import _get, _post, _patch, _delete


class CoolifyApplicationEnvVars:
    """
    Manages environment variables for applications in a Coolify instance.

    The class provides methods for asynchronous and synchronous management of
    environment variables related to applications in the Coolify platform. It
    supports CRUD (Create, Read, Update, and Delete) operations with both single
    and bulk updates for environment variables. This class uses asynchronous HTTP
    requests internally to interact with the Coolify backend API.

    :ivar _logger: Logger instance used for internal logging.
    :type _logger: logging.Logger
    :ivar _base_url: Base URL for the Coolify API.
    :type _base_url: str
    :ivar _headers: Headers to include in API requests, typically containing
        authentication or content type information.
    :type _headers: dict[str, str]
    """
    _logger = getLogger(__name__)
    """Logger for the class."""

    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self._base_url: str = base_url
        """Base URL for the class."""
        self._headers: dict[str, str] = headers
        """Headers for the class."""

    ###############
    # List:
    async def _list_all(self, application_uuid: str) -> list[dict[str, Any]]:
        """
        List environment variables for the specified application.

        This asynchronous method retrieves all environment variables associated with
        a particular application identified by its UUID. It sends an HTTP GET request
        to the constructed endpoint and returns the resulting data as a list of
        dictionaries.

        :param application_uuid: The unique identifier (UUID) of the application
            for which to retrieve environment variables.
        :type application_uuid: str
        :return: A list of dictionaries containing the environment variables
            associated with the application.
        :rtype: list[dict[str, Any]]
        """
        _log_message(self._logger, DEBUG, f"Start to list vars for app_id: {application_uuid}")
        endpoint = f"applications/{application_uuid}/envs"
        results = await _get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish listing vars for app_id: {application_uuid}")
        return results

    def list_all(self, application_uuid: str) -> list[dict[str, Any]]:
        """
        Lists all records associated with the specified application UUID.

        This method retrieves and returns a list of dictionaries containing the records
        related to the supplied application UUID. It determines whether to run an
        asynchronous function in an existing event loop or outside one, depending on
        runtime.

        :param application_uuid: Unique identifier for the application whose records
            are to be listed.
        :type application_uuid: str
        :return: A list of dictionaries where each dictionary represents a record.
        :rtype: list[dict[str, Any]]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._list_all(application_uuid)
        except RuntimeError:
            return asyncio.run(self._list_all(application_uuid))

    #################
    # Create:
    async def _create(self, application_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Asynchronous method for creating an environment variable for a given application.

        This method handles the creation of an environment variable under a specific application
        using its unique identifier. It sends a POST request to the provided endpoint with the
        necessary data. Logging messages are generated before and after the operation to help
        in tracking the process.

        :param application_uuid: Unique identifier for the application.
        :type application_uuid: str
        :param data: Key-value pairs containing the details of the environment variable to create.
        :type data: dict[str, Any]
        :return: A dictionary containing the server response for the POST request.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, f"Start to create var for app_id: {application_uuid}", data)
        endpoint = f"applications/{application_uuid}/envs"
        results = await _post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish creating var for app_id: {application_uuid}")
        return results

    def create(self, application_uuid: str,
               data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Creates a new application data object associated with the given application UUID.
        This function is capable of both synchronous and asynchronous execution. It attempts
        to leverage the current running asynchronous event loop if present; otherwise, it
        falls back to running its asynchronous counterpart in a synchronous context.

        The function utilizes additional keyword arguments to dynamically generate a portion
        of the data structure using a utility function.

        :param application_uuid: The unique identifier of the application.
        :type application_uuid: str
        :param data: Optional dictionary containing additional application data. If not provided,
            the function initializes this parameter as None.
        :type data: Optional[dict[str, Any]]
        :param kwargs: Any additional keyword arguments used to build or extend the data dictionary.

        :return: A dictionary representing the created application data object.
        :rtype: dict[str, Any]
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._create(application_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._create(application_uuid, real_data))

    ################
    # Update singe:
    async def _update(self, application_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Asynchronous method to update environment variables for a specific application.

        This method sends a PATCH request to the specified endpoint to update the
        environment variables of the application identified by the given UUID. It
        logs the start and end of the operation for debugging purposes. The updated
        environment data is provided as a dictionary.

        :param application_uuid: Unique identifier of the application.
        :type application_uuid: str
        :param data: Dictionary containing the environment variables to be updated.
        :type data: dict[str, Any]
        :return: The result of the PATCH request containing the response data.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, f"Start to update var for app_id: {application_uuid}", data)
        endpoint = f"applications/{application_uuid}/envs"
        results = await _patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating var for app_id: {application_uuid}")
        return results

    def update(self, application_uuid: str,
               data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Updates an application resource identified by the provided UUID with the given
        data and optional keyword arguments. If there's an active asyncio event loop,
        the asynchronous update method is invoked. Otherwise, the asynchronous update
        method is run in a new event loop.

        :param application_uuid: The unique identifier of the application to update.
        :type application_uuid: str
        :param data: The data to update the application with. Defaults to None.
        :type data: Optional[dict[str, Any]]
        :param kwargs: Additional keyword arguments to customize the update operation.
        :type kwargs: dict
        :return: A dictionary containing the updated application data.
        :rtype: dict[str, Any]
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(application_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(application_uuid, real_data))

    #############
    # Update Multiple:
    async def _update_bulk(self, application_uuid: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Updates environment variables for a given application in bulk.

        This asynchronous method performs a bulk update of environment variables for
        the specified application using the provided data. It logs the start and
        completion of the operation at the debug level. The actual update is
        performed by sending a PATCH request to the corresponding endpoint.

        :param application_uuid: Unique identifier of the application.
        :type application_uuid: str
        :param data: A list of dictionaries, where each dictionary represents the
            environment variable to be updated and its associated data.
        :type data: list[dict[str, Any]]
        :return: A dictionary containing the result of the bulk update operation.
        :rtype: dict[str, Any]
        """
        message = f"Start to bulk update vars for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        endpoint = f"applications/{application_uuid}/envs/bulk"
        results = await _patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish bulk updating vars for app_id: {application_uuid}")
        return results

    def update_bulk(self, application_uuid: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Updates a bulk operation for a given application UUID with the provided data. This
        method ensures compatibility with both synchronous and asynchronous execution
        contexts. If called from within an active event loop, it delegates the operation
        to an asynchronous method. If no event loop is running, it creates one and runs
        the asynchronous method.

        :param application_uuid: The unique identifier for the application to which the
                                 bulk operation corresponds.
        :type application_uuid: str
        :param data: A list of dictionaries containing the bulk operation data. Each
                     dictionary should represent an individual operation with its
                     respective details.
        :type data: list[dict[str, Any]]
        :return: A dictionary containing the status or result of the bulk update operation.
        :rtype: dict[str, Any]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._update_bulk(application_uuid, data)
        except RuntimeError:
            return asyncio.run(self._update_bulk(application_uuid, data))

    ############
    # Delete:
    async def _delete(self, application_uuid: str, variable_uuid: str) -> dict:
        """
        Perform an asynchronous operation to delete a variable within a specified application.

        This method logs messages indicating the start and end of the delete operation. It
        constructs the endpoint URL for the delete request and uses an asynchronous method
        to send the delete request. The result of the request is then returned.

        :param application_uuid: The unique identifier of the target application.
        :type application_uuid: str
        :param variable_uuid: The unique identifier of the target variable to be deleted.
        :type variable_uuid: str
        :return: The results of the asynchronous delete operation as a dictionary.
        :rtype: dict
        """
        message = f"Start delete var {variable_uuid} for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        endpoint = f"applications/{application_uuid}/envs/{variable_uuid}"
        results = await _delete(self._base_url, endpoint, self._headers)
        message = f"Finish delete var {variable_uuid} for app_id: {application_uuid}"
        _log_message(self._logger, DEBUG, message)
        return results

    def delete(self, application_uuid: str, variable_uuid: str) -> dict:
        """
        Deletes a specified variable for a given application. The method handles both
        synchronous and asynchronous execution environments to ensure seamless
        operation. If called from within an async event loop, it executes the delete
        operation asynchronously. Otherwise, it manages the operation using asyncio.run,
        allowing blocking-style execution.

        :param application_uuid: The unique identifier of the application.
        :type application_uuid: str
        :param variable_uuid: The unique identifier of the variable to be deleted.
        :type variable_uuid: str
        :return: A dictionary representing the result of the variable deletion
            operation.
        :rtype: dict
        """
        try:
            _ = asyncio.get_running_loop()
            return self._delete(application_uuid, variable_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(application_uuid, variable_uuid))

