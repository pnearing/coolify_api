"""coolify_api/applications.py"""
import asyncio
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
from typing import Optional, Any

import _utils
from ._logging import _log_message
from .url_utils import get, patch, delete
from .applications_create import CoolifyApplicationCreate
from .applications_environment import CoolifyApplicationEnvVars


class CoolifyApplications:
    """
    Manages Coolify applications, providing methods to perform synchronous and
    asynchronous operations such as listing, retrieving, updating, and deleting
    applications. Designed to interface with a Coolify backend API. The class
    also provides separate control, creation, and environment variable handling
    functionalities through related modules.

    :ivar create: Provides methods for creating Coolify applications.
    :type create: CoolifyApplicationCreate
    :ivar envs: Manages environment variables for Coolify applications.
    :type envs: CoolifyApplicationEnvVars
    """
    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        """Base URL for the class."""
        self._headers = headers
        """Headers for the class."""
        self.create: CoolifyApplicationCreate = CoolifyApplicationCreate(base_url, headers)
        """Create methods for applications."""
        self.envs: CoolifyApplicationEnvVars = CoolifyApplicationEnvVars(base_url, headers)
        """Env Vars methods for applications."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

#################
# LIST:
    async def _list_all(self) -> list[dict[str, Any]]:
        """
        Asynchronously retrieves a list of all applications from the specified endpoint.

        This function sends a GET request to the given endpoint and retrieves the list
        of applications in the form of a list of dictionaries. The process is logged
        at both the start and end of the operation for debugging purposes.

        :return: A list of dictionaries, each representing an application.
        :rtype: list[dict[str, Any]]
        """
        _log_message(self._logger, DEBUG, "Start to list all applications")
        endpoint = "applications"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all applications")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        """
        Lists all elements asynchronously or synchronously based on the running environment.

        This method checks if the code is being executed in an asynchronous loop. If the code
        is inside an asynchronous environment, it will execute the asynchronous function
        directly. If not, it runs the asynchronous function in a newly created event loop.

        :return: A list of dictionaries, each representing an application.
        :rtype: list[dict[str, Any]]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

#############
# GET:
    async def _get(self, application_uuid: str) -> dict[str, Any]:
        """
        Fetches application information asynchronously based on the provided UUID.

        This method sends a GET request to retrieve the details
        of an application specified by its unique identifier. The process is
        logged at the DEBUG level both when starting and finishing the data
        retrieval.

        :param application_uuid: A string that uniquely identifies the
            application to be retrieved.
        :return: A dictionary containing the application details retrieved
            from the specified endpoint.
        """
        _log_message(self._logger, DEBUG, f"Start to get application with id: {application_uuid}")
        endpoint = f"applications/{application_uuid}"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting application with id: {application_uuid}")
        return results

    def get(self, application_uuid: str) -> dict[str, Any]:
        """
        This method retrieves application details based on the UUID provided. The function
        checks if there is an active asyncio event loop. If present, it proceeds with the
        asynchronous version of the fetch operation. Otherwise, it blocks and runs the
        asynchronous fetch function in a new event loop context. The return value is a
        dictionary containing the application's details.

        :param application_uuid: Unique identifier of the application whose details need
                                 to be fetched.
        :type application_uuid: str
        :return: A dictionary containing the application details retrieved
            from the specified endpoint.
        :rtype: dict[str, Any]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._get(application_uuid)
        except RuntimeError:
            return asyncio.run(self._get(application_uuid))

#######################
# DELETE:
    async def _delete(self, application_uuid: str) -> dict[str, Any]:
        """
        Deletes an application with the specified UUID. The function makes an asynchronous
        DELETE request to the application's specific endpoint and logs the start and
        completion of the operation.

        :param application_uuid: A string representing the UUID of the application to delete.
        :return: A dictionary containing the results of the DELETE operation.
        """
        _log_message(self._logger, DEBUG, f"Start to delete application with id: {application_uuid}")
        endpoint = f"applications/{application_uuid}"
        results = delete(self._base_url, endpoint, self._headers)
        # TODO: CHECK IF ^^THIS^^ MIGHT RETURN NONE.
        _log_message(self._logger, DEBUG, f"Finish deleting application with id: {application_uuid}")
        return results

    def delete(self, application_uuid: str) -> dict[str, Any]:
        """
        Deletes an application identified by its UUID. This method ensures that the deletion
        is compatible with both synchronous and asynchronous contexts. If an event loop is
        already running, it delegates to an asynchronous delete method. Otherwise, it executes
        the asynchronous delete method in a new event loop.

        :param application_uuid: The unique identifier for the application to be deleted.
        :type application_uuid: str
        :return: A dictionary containing the result of the delete operation.
        :rtype: dict[str, Any]
        """

        try:
            _ = asyncio.get_running_loop()
            return self._delete(application_uuid)
        except RuntimeError:
            return asyncio.run(self._delete(application_uuid))

###############
# UPDATE:
    async def _update(self, application_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Performs an asynchronous update for an application using its unique identifier and the provided data.
        This method sends a PATCH request to update the application and logs debug messages before and
        after the operation is performed.

        :param application_uuid: The universally unique identifier of the application to be updated.
        :type application_uuid: str
        :param data: A dictionary containing the fields and their new values to be updated in the application.
        :type data: dict[str, Any]
        :return: A dictionary containing the results of the update operation.
        :rtype: dict[str, Any]
        """
        message = f"Start to update application with id: {application_uuid}"
        _log_message(self._logger, DEBUG, message, data)
        endpoint = f"applications/{application_uuid}"
        results = patch(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, f"Finish updating application with id: {application_uuid}")
        return results

    def update(self, application_uuid: str,
               data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        """
        Updates an application with provided data, handling different execution environments
        for asyncio. Supports both synchronous and asynchronous contexts.

        The function processes the data dictionary and merges it with additional keyword arguments
        before invoking the update process. If an existing asyncio event loop is running,
        the asynchronous update method is leveraged. If no loop exists, the method will run
        the asynchronous update method in a blocking manner using `asyncio.run`.

        :param application_uuid: The unique identifier for the application to be updated.
        :type application_uuid: str
        :param data: A dictionary containing the data for the update, or None.
        :type data: Optional[dict[str, Any]]
        :param kwargs: Additional key-value pairs to merge with the input data.
        :return: A dictionary representing the updated application data returned by the
            update process.
        :rtype: dict[str, Any]
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._update(application_uuid, real_data)
        except RuntimeError:
            return asyncio.run(self._update(application_uuid, real_data))

#############
# Start:
    async def _start(self, application_id: str) -> dict[str, Any]:
        """
        Starts an application asynchronously using its application ID.

        This method communicates with an API endpoint to initiate the starting
        process of the application specified by the `application_id`. It logs
        debug messages before and after the process, and it returns the results
        as a dictionary.

        :param application_id: The unique identifier of the application to
            start.
        :type application_id: str
        :return: A dictionary containing the response from the operation,
            which includes details about the started application.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, f"Starting app with app_id: {application_id}")
        endpoint = f"applications/{application_id}/start"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish starting app with app_id: {application_id}")
        return results

    def start(self, application_id: str) -> dict[str, Any]:
        """
        Starts the application process by either invoking the asynchronous
        method directly if an event loop is running, or by running the
        asynchronous method in a new event loop if no event loop is detected.

        This method identifies the current asyncio context and ensures that
        the appropriate asynchronous process is triggered based on the
        context's state.

        :param application_id: A string that uniquely identifies the
            application to be started.
        :return: A dictionary containing the result of the application start
            process. The keys and values of the dictionary vary depending on
            the implementation of `self._a_start`.
        """
        try:
            _ = asyncio.get_running_loop()
            return self._start(application_id)
        except RuntimeError:
            return asyncio.run(self._start(application_id))

###############
# Stop:
    async def _stop(self, application_id: str) -> dict[str, Any]:
        """
        Stops a running application asynchronously.

        The method sends a request to stop the application identified by the provided
        application ID. Upon successfully stopping the application, the results are
        returned as a dictionary containing details of the operation.

        :param application_id: A string representing the unique identifier of the
            application to stop.
        :return: A dictionary containing the result of the stop operation.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, f"Stopping app with app_id: {application_id}")
        endpoint = f"applications/{application_id}/stop"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish stopping app with app_id: {application_id}")
        return results

    def stop(self, application_id: str) -> dict[str, Any]:
        """
        Stops the specified application based on its unique identifier. This method aims
        to interact with an asynchronous implementation and falls back to synchronous
        execution when no running event loop is detected.

        :param application_id: The unique identifier of the application to be stopped.
        :type application_id: str
        :return: A dictionary containing the result of the stopping operation.
        :rtype: dict[str, Any]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._stop(application_id)
        except RuntimeError:
            return asyncio.run(self._stop(application_id))

############
# Restart:
    async def _restart(self, application_id: str) -> dict[str, Any]:
        """
        Restart an application asynchronously using its application ID. This function
        logs debug messages before and after restarting the application, sends a GET
        request to the appropriate endpoint, and returns the results.

        :param application_id: The unique identifier of the application to restart
        :type application_id: str
        :return: The response data from the restart operation
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, f"Restarting app with app_id: {application_id}")
        endpoint = f"applications/{application_id}/restart"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish restarting app with app_id: {application_id}")
        return results

    def restart(self, application_id: str) -> dict[str, Any]:
        """
        Restarts the application identified by the given application ID. This method
        checks if an asyncio event loop is running in the current context. If an
        event loop is running, it calls the asynchronous `_a_restart` method using
        the running loop; otherwise, it blocks and invokes the asynchronous method
        using `asyncio.run`. This ensures safe operation in both synchronous and
        asynchronous execution contexts.

        :param application_id: Identifier of the application to be restarted
        :type application_id: str
        :return: A dictionary containing the status and result of the restart operation
        :rtype: dict[str, Any]
        """
        try:
            _ = asyncio.get_running_loop()
            return self._restart(application_id)
        except RuntimeError:
            return asyncio.run(self._restart(application_id))
