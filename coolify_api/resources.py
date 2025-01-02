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
#
import asyncio
from logging import getLogger, DEBUG

from coolify_api._logging import _log_message
from coolify_api.url_utils import get


class CoolifyResources:
    """Class to hold resources methods."""
    def __init__(self, base_url: str, headers: dict) -> None:
        self._base_url = base_url
        """Base URL for the class."""
        self._headers = headers
        """Headers for the class."""
        self._logger = getLogger(__name__)
        """Logger for the class."""

    def _list_all(self) -> list[dict]:
        _log_message(self._logger, DEBUG, "Listing all resources")
        endpoint = "resources"
        results = get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finished listing resources")
        return results

    def list_all(self) -> list[dict]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())
