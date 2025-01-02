"""Filename: applications_create.py"""
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

from coolify_api._logging import _log_message
from coolify_api.url_utils import post
from coolify_api import utils


class CoolifyApplicationCreate:
    """
    Handles the creation of various types of applications using Coolify's API.

    Provides methods to create public applications, private applications through GitHub,
    private applications using deploy keys, Dockerfile applications, Docker image applications,
    and Docker Compose applications. Utilizes asynchronous HTTP calls to interact with Coolify's
    API, while offering a structured way to handle application creation with optional data input
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

################
# Public Repo:
    async def _public(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Initiates the creation of a public repository application.

        This asynchronous function interacts with the specified endpoint to create a
        public repository application using the provided input data. It logs debugging
        information before and after the request execution. The function relies on
        an async HTTP POST call to send the request and retrieve the result, which it
        subsequently returns.

        :param data: A dictionary containing the required information for creating
                     the public repository application.
        :type data: dict[str, Any]
        :return: Result of the HTTP POST request for creating the public repository
                 application.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, "Start to create a public repo app.", data)
        endpoint = "applications/public"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a public repo app")
        return results

    def public(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Asynchronously or synchronously processes the provided data and returns the result.

        This function adapts its behavior based on the availability of an active event loop.
        If an event loop is running, it executes the `_a_public` method asynchronously; otherwise,
        it runs the `_a_public` method using `asyncio.run`, blocking until the coroutine is complete.

        :param data: Optional dictionary containing input data to be processed.
        :type data: Optional[dict[str, Any]]
        :param kwargs: Additional keyword arguments passed to the `_a_public` method.
        :return: A dictionary containing the result of the processed operation.
        :rtype: dict[str, Any]
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._public(real_data)
        except RuntimeError:
            return asyncio.run(self._public(real_data))

###########
# Git Hub private repo using git-hub app:
    async def _private_github_app(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Asynchronously creates a private GitHub application using the provided data.

        This method interacts with a GitHub endpoint that facilitates the creation of
        private applications, utilizing the provided base URL and authentication
        headers. The input data defines the parameters necessary for the application
        creation. Logging is implemented to document the start and completion of the
        operation for debugging purposes.

        :param data: A dictionary containing the data required for creating the private
            GitHub application.
        :type data: dict[str, Any]
        :return: A dictionary containing the results of the operation, which includes
            information about the created private GitHub application.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, "Start to create a private app using GitHub.", data)
        endpoint = "applications/private-github-app"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a private GitHub app")
        return results

    def private_github_app(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Constructs the actual data object by combining given ``data`` and ``kwargs``,
        and invokes the asynchronous method ``_a_private_github_app`` for further
        processing. If the call is already in an asynchronous context, it awaits
        the asynchronous method directly; otherwise, it runs the asynchronous
        method in a new event loop synchronously.

        The method acts as an intermediary for handling data transformation
        and maintains compatibility between synchronous and asynchronous
        execution contexts.

        :param data: Optional dictionary containing the initial input data.
            If None, an empty data object is created.
        :param kwargs: Additional keyword arguments to be merged into the data.
        :return: A dictionary containing the result of the ``_a_private_github_app``
            asynchronous method execution.
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._private_github_app(real_data)
        except RuntimeError:
            return asyncio.run(self._private_github_app(real_data))

##############
# Private repo with a deploy-key:
    async def _private_deploy_key(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Initiates the process of creating a private application using a deploy key and performs
        asynchronous HTTP POST operation to the specified endpoint.

        This method logs the initiation and completion of the creation process, utilizing the provided
        deploy key details in the `data` parameter. The results of the operation are returned as a
        dictionary.

        :param data: A dictionary containing the deploy key details and additional parameters required
            for creating a private application.
        :type data: dict[str, Any]
        :return: A dictionary containing the results of the private application creation process.
        :rtype: dict[str, Any]
        """
        message = "Start to create a private app using deploy key"
        _log_message(self._logger, DEBUG, message, data)
        endpoint = "applications/private-deploy-key"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a private app using deploy key")
        return results

    def private_deploy_key(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Generates and manages a private deploy key for authentication. This method allows asynchronous
        execution if there is an existing running event loop; otherwise, it will handle the invocation
        of the asynchronous operation in a synchronous context by running the coroutine.

        :param data: The optional dictionary containing deployment-specific data used during the
                     creation or retrieval of the private deploy key.
        :type data: Optional[dict[str, Any]]
        :param kwargs: Additional key-value arguments that may be required for processing during
                       deployment.
        :return: A dictionary containing the details of the private deploy key or operation result.
        :rtype: dict[str, Any]
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._private_deploy_key(real_data)
        except RuntimeError:
            return asyncio.run(self._private_deploy_key(real_data))

##############
# Supplied dockerfile:
    async def _dockerfile(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Creates a Dockerfile-based application by sending the necessary data to a given
        endpoint asynchronously. The method logs the start and finish of the operation
        for debugging purposes.

        :param data: The dictionary containing the details required to create a
            Dockerfile-based application.
        :type data: dict[str, Any]
        :return: A dictionary containing the results of the operation.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, "Start to create a Dockerfile application.", data)
        endpoint = "applications/dockerfile"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Dockerfile application")
        return results

    def dockerfile(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Generate a Dockerfile representation based on provided data and keyword arguments.

        This method creates a Dockerfile configuration by combining user-provided
        data and additional keyword arguments. It supports both synchronous and
        asynchronous execution, depending on the presence of a running asyncio
        event loop.

        :param data: Optional dictionary containing initial data for the Dockerfile.
        :param kwargs: Additional parameters to extend or override the provided data.
        :return: A dictionary representation of the resulting Dockerfile configuration.
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._dockerfile(real_data)
        except RuntimeError:
            return asyncio.run(self._dockerfile(real_data))

###########
# Supplied docker image:
    async def _docker_image(self, data: Optional[dict[str, Any]], **kwargs) -> dict[str, Any]:
        """
        Asynchronously creates a Docker image application by sending data to a specified endpoint.
        This function combines the provided data and additional keyword arguments into a complete
        data payload, logs the creation process steps, and sends an HTTP POST request to create the
        application. Returns the result of the API call.

        :param data: Dictionary containing the main data for creating the Docker image
        application. This can be optional if additional data is provided via keyword
        arguments.
        :type data: Optional[dict[str, Any]]

        :param kwargs: Additional data to be included in the request payload.
        :type kwargs: Any

        :return: Results from the API call containing details of the created Docker image
        application.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, "Start to create a Docker image application.", data)
        endpoint = "applications/dockerimage"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Docker image application")
        return results

    def docker_image(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Generate or retrieve a Docker image asynchronously.

        This function handles the processing of input data and manages whether
        to execute the operation within an existing event loop or synchronously
        within a new one, depending on the runtime environment. It utilizes
        helper utilities to integrate additional keyword arguments into the
        input data and interacts with the asynchronous function (`_a_docker_image`)
        for the actual execution.

        :param data: Optional input data containing parameters for the image
            processing, provided as a dictionary. If `None`, an empty dictionary
            is used.
        :param kwargs: Additional keyword arguments to be incorporated into the
            `data` dictionary by the helper utility `create_data_with_kwargs`.
        :return: A dictionary representing the processed Docker image data or
            result following the execution of `_a_docker_image`.
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._docker_image(real_data)
        except RuntimeError:
            return asyncio.run(self._docker_image(real_data))

    async def _a_docker_compose(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Asynchronously creates a Docker Compose application.

        This function posts the provided application data to the specified Docker
        Compose endpoint to create a new application. The operation is logged at
        the DEBUG level both at the beginning and after the operation's completion.

        :param data: A dictionary containing the configuration and specifications
            required to create a Docker Compose application.
        :type data: dict[str, Any]
        :return: A dictionary containing the results of the API operation.
        :rtype: dict[str, Any]
        """
        _log_message(self._logger, DEBUG, "Start to create a Docker Compose application.", data)
        endpoint = "applications/dockercompose"
        results = post(self._base_url, endpoint, self._headers, data=data)
        _log_message(self._logger, DEBUG, "Finish creating a Docker Compose application")
        return results

    def docker_compose(self, data: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """
        Generates the appropriate data dictionary based on provided input parameters and executes
        Docker Compose functionality either synchronously or asynchronously depending on the
        current running event loop.

        If there is already an active asyncio event loop, the method ensures that the `_a_docker_compose`
        function is triggered asynchronously and its result is returned. Otherwise, it creates a new event loop
        by invoking `asyncio.run` to execute `_a_docker_compose`. This allows for flexible execution with or
        without an active asynchronous environment.

        :param data: A dictionary containing pre-generated data for configuring Docker Compose.
            If None, the method generates data based on keyword arguments.
        :param kwargs: Additional configuration parameters used to construct the data dictionary.
            These parameters are merged with `data` to create the final input.
        :return: A dictionary containing the result of the Docker Compose operation, either processed
            asynchronously or synchronously depending on the event loop state.
        """
        real_data = utils.create_data_with_kwargs(data, **kwargs)
        try:
            _ = asyncio.get_running_loop()
            return self._a_docker_compose(real_data)
        except RuntimeError:
            return asyncio.run(self._a_docker_compose(real_data))
