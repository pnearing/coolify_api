"""File: coolify_api/teams.py"""
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

from _logging import _log_message
from url_utils import get


class CoolifyTeams:
    _logger = getLogger(__name__)

    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self._base_url: str = base_url
        self._headers: dict[str, str] = headers

    async def _list_all(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start listing all teams")
        endpoint = "teams"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish listing all teams")
        return results

    def list_all(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._list_all()
        except RuntimeError:
            return asyncio.run(self._list_all())

    async def _get(self, team_id: str) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, f"Start getting team with id: {team_id}")
        endpoint = f"teams/{team_id}"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting team with id: {team_id}")
        return results

    def get(self, team_id: str) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get(team_id)
        except RuntimeError:
            return asyncio.run(self._get(team_id))

    async def _get_team_members(self, team_id: str) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, f"Start getting members for team with id: {team_id}")
        endpoint = f"teams/{team_id}/members"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, f"Finish getting members for team with id: {team_id}")
        return results

    def get_team_members(self, team_id: str) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._get_team_members(team_id)
        except RuntimeError:
            return asyncio.run(self._get_team_members(team_id))

    async def _get_current_team(self) -> dict[str, Any]:
        _log_message(self._logger, DEBUG, "Start getting current team")
        endpoint = "teams/current"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish getting current team")
        return results

    def get_current_team(self) -> dict[str, Any]:
        try:
            _ = asyncio.get_running_loop()
            return self._get_current_team()
        except RuntimeError:
            return asyncio.run(self._get_current_team())

    async def _get_current_team_members(self) -> list[dict[str, Any]]:
        _log_message(self._logger, DEBUG, "Start getting members of the current team")
        endpoint = "teams/current/members"
        results = await get(self._base_url, endpoint, self._headers)
        _log_message(self._logger, DEBUG, "Finish getting members of the current team")
        return results

    def get_current_team_members(self) -> list[dict[str, Any]]:
        try:
            _ = asyncio.get_running_loop()
            return self._get_current_team_members()
        except RuntimeError:
            return asyncio.run(self._get_current_team_members())