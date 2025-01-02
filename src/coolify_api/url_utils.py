"""Module to store all url handling methods."""
import asyncio
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
import os
from datetime import timedelta
from typing import Any, NoReturn, Optional
import time
import requests
from requests.models import Response
import logging

from coolify_api._logging import OUTPUT_IS_SHY
from coolify_api.exceptions import *

LOGGER = logging.getLogger(__name__)

REQUESTS_PER_SECOND = os.getenv("REQUESTS_PER_SECOND", 4)
REQUESTS_TIMEOUT = os.getenv("REQUESTS_TIMEOUT", 10)

INITIAL_OFFSET_TIME = timedelta(seconds=30)
LAST_REQUEST_TIME = time.time() - INITIAL_OFFSET_TIME.total_seconds()


@staticmethod
def _build_v1_url(base_url, endpoint):
    return f"{base_url}/api/v1/{endpoint}"


@staticmethod
def _handle_response(data: Optional[Any], response: Response) -> Any | NoReturn:
    status_code = response.status_code
    url = response.url
    if 200 <= response.status_code < 300:
        LOGGER.info("Coolify Api URL: '%s', responded with Status Code: '%i'", url, status_code)
        return response.json()
    if 300 <= response.status_code < 400:
        LOGGER.warning("Coolify Api URL: '%s', responded with Status Code: '%i'", url, status_code)
        try:
            return response.json()
        except ValueError:
            if not OUTPUT_IS_SHY:
                message = (f"Coolify Api URL: '{url}', responded with Status Code: '{status_code}',"
                           f" and the following JSON data was returned: \n{response.text}")
                LOGGER.warning(message)
            return response.text
    if 400 <= response.status_code < 500:
        if response.status_code == 401:
            raise CoolifyAuthenticationError(url=url, headers=headers, data=data, response=response)
        if response.status_code == 422:
            raise CoolifyAPIValidationError(response)
        # Default Error:
        raise CoolifyAPIResponseError(url=url, headers=headers, data=data, response=response)
    if response.status_code >= 500:
        raise CoolifyAPIError(url=url, headers=headers, data=data, response=response)


# RATE LIMITING: 1 request a second.
@staticmethod
def _rate_limit() -> bool:
    global LAST_REQUEST_TIME
    current_time = time.time()
    interval = 1 / REQUESTS_PER_SECOND
    limited = False
    if current_time - LAST_REQUEST_TIME < interval:
        sleep_time = interval - (current_time - LAST_REQUEST_TIME)
        LOGGER.debug("Rate limiting applied. Sleeping for %s seconds.", sleep_time)
        time.sleep(sleep_time)
        limited = True
    LAST_REQUEST_TIME = time.time()
    return limited


##############
# GET:
@staticmethod
async def _get(url: str,
               headers: dict[str, str],
               params: Optional[dict[str, str]] = None,
               ) -> Any | NoReturn:
    LOGGER.debug("Starting GET request to %s", url)
    try:
        _rate_limit()
        response = await requests.get(url, headers=headers, timeout=REQUESTS_TIMEOUT, params=params)
    except requests.RequestException as e:
        LOGGER.error("Error sending GET request to %s", url)
        raise RequestsError(url, headers=headers, data=None, exception=e) from e
    LOGGER.debug("Finished GET request to %s", url)
    return _handle_response(data=None, response=response)


@staticmethod
def get(base_url: str,
        endpoint: str,
        headers: dict,
        params: Optional[dict] = None
        ) -> Any | NoReturn:
    url = _build_v1_url(base_url, endpoint)
    try:
        _ = asyncio.get_running_loop()
        return _get(url=url, headers=headers, params=params)
    except RuntimeError:
        return asyncio.run(_get(url=url, headers=headers, params=params))


#####################
# POST:
@staticmethod
async def _post(url: str,
                headers: dict,
                params: Optional[dict] = None,
                data: Any = None
                ) -> Any | NoReturn:
    LOGGER.debug("Starting POST request to %s", url)
    try:
        _rate_limit()
        response = await requests.post(url,
                                       headers=headers,
                                       params=params,
                                       json=data,
                                       timeout=REQUESTS_TIMEOUT)
    except requests.RequestException as e:
        LOGGER.error("Error sending POST request to %s", url)
        raise RequestsError(url, headers=headers, data=data, exception=e) from e
    LOGGER.debug("Finished POST request to %s", url)
    return _handle_response(url=url, headers=headers, data=data, response=response)


@staticmethod
def post(base_url: str,
         endpoint: str,
         headers: dict,
         params: Optional[dict] = None,
         data: Any = None
         ) -> Any:
    url = _build_v1_url(base_url, endpoint)
    try:
        _ = asyncio.get_running_loop()
        return _post(url, headers=headers, params=params, data=data)
    except RuntimeError:
        return asyncio.run(_post(url, headers=headers, params=params, data=data))


###############
# PATCH:
@staticmethod
async def _patch(url: str,
                 headers: dict,
                 params: Optional[dict] = None,
                 data: Any = None
                 ) -> Any | NoReturn:
    LOGGER.debug("Starting PATCH request to %s", url)
    try:
        _rate_limit()
        response = await requests.patch(url,
                                  headers=headers,
                                  params=params,
                                  json=data,
                                  timeout=REQUESTS_TIMEOUT,
                                  )
    except requests.RequestException as e:
        LOGGER.error("Error sending PATCH request to %s", url)
        raise RequestsError(url, headers=headers, data=data, exception=e) from e
    LOGGER.debug("Finished PATCH request to %s", url)
    return _handle_response(url=url, headers=headers, data=data, response=response)


@staticmethod
def patch(base_url: str,
          endpoint: str,
          headers: dict,
          params: Optional[dict] = None,
          data: Any = None
          ) -> Any:
    url = _build_v1_url(base_url, endpoint)
    try:
        _ = asyncio.get_running_loop()
        return asyncio.run(_patch(url, headers=headers, params=params, data=data))
    except RuntimeError:
        return asyncio.run(_patch(url, headers=headers, params=params, data=data))


#############
# DELETE:
@staticmethod
async def _delete(url: str,
                  headers: dict,
                  params: Optional[dict] = None
                  ) -> Any | NoReturn:
    LOGGER.debug("Starting DELETE request to %s", url)
    try:
        _rate_limit()
        response = await requests.delete(url, headers=headers, timeout=REQUESTS_TIMEOUT,
                                         params=params)
    except requests.RequestException as e:
        LOGGER.error("Error sending DELETE request to %s", url)
        raise RequestsError(url, headers=headers, data=None, exception=e) from e
    LOGGER.debug("Finished DELETE request to %s", url)
    return _handle_response(url=url, headers=headers, data=None, response=response)


@staticmethod
def delete(base_url: str,
           endpoint: str,
           headers: dict,
           params: Optional[dict] = None,
           ) -> Any:
    url = _build_v1_url(base_url, endpoint)
    try:
        _ = asyncio.get_running_loop()
        return _delete(url, headers=headers, params=params)
    except RuntimeError:
        return asyncio.run(_delete(url, headers=headers, params=params))
