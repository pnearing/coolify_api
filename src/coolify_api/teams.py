"""Coolify Teams API client.

This module provides methods to manage Coolify teams, including:
- Listing all teams
- Getting team details
- Managing team members
- Getting current team information

Example:
    ```python
    from coolify_api import CoolifyAPIClient

    client = CoolifyAPIClient()

    # List all teams
    teams = client.teams.list_all()

    # Get team details
    team = client.teams.get("team-id")

    # Get team members
    members = client.teams.team_members("team-id")

    # Get current team
    current = client.teams.current_team()
    current_members = client.teams.current_team_members()
    ```
"""

from logging import getLogger, DEBUG
from typing import Any, Coroutine, Dict, List

from ._logging import _log_message
from ._http_utils import HTTPUtils


class CoolifyTeams:
    """Manages Coolify teams.

    This class provides methods to interact with teams in Coolify, including
    team management and member operations.
    """

    def __init__(self, http_utils: HTTPUtils) -> None:
        """Initialize the teams manager.

        Args:
            http_utils: HTTP client for making API requests
        """
        self._http_utils = http_utils
        self._logger = getLogger(__name__)

    def list_all(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """List all teams.

        Returns:
            List of team objects containing:
            - id (int): Team ID
            - name (str): Team name
            - description (str): Team description
            - personal_team (bool): Whether team is personal
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp
            - smtp_enabled (bool): SMTP notification status
            - discord_enabled (bool): Discord notification status
            - telegram_enabled (bool): Telegram notification status
            And many other notification configuration fields

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to list all teams"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("teams")
        message = "Finish listing all teams"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def get(self, team_id: str) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get team details by ID.

        Args:
            team_id: ID of the team to retrieve

        Returns:
            Team object containing same fields as list_all()

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If team ID not found
        """
        message = f"Start to get team with id: {team_id}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"teams/{team_id}")
        message = f"Finish getting team with id: {team_id}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def team_members(self, team_id: str
                    ) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """Get team members by team ID.

        Args:
            team_id: ID of the team

        Returns:
            List of user objects containing:
            - id (int): User ID
            - name (str): User name
            - email (str): User email
            - email_verified_at (str): Email verification timestamp
            - created_at (str): Creation timestamp
            - updated_at (str): Last update timestamp
            - two_factor_confirmed_at (str): 2FA confirmation timestamp
            - force_password_reset (bool): Password reset flag
            - marketing_emails (bool): Marketing email preference

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
            CoolifyNotFoundError: If team ID not found
        """
        message = f"Start getting members for team with id: {team_id}"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get(f"teams/{team_id}/members")
        message = f"Finish getting members for team with id: {team_id}"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def current_team(self) -> Dict[str, Any] | Coroutine[Any, Any, Dict[str, Any]]:
        """Get currently authenticated team.

        Returns:
            Team object containing same fields as list_all()

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start to get current team"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("teams/current")
        message = "Finish getting current team"
        _log_message(self._logger, DEBUG, message, results)
        return results

    def current_members(self) -> List[Dict[str, Any]] | Coroutine[Any, Any, List[Dict[str, Any]]]:
        """Get members of currently authenticated team.

        Returns:
            List of user objects containing same fields as team_members()

        Raises:
            CoolifyError: For general API errors
            CoolifyAuthenticationError: If authentication fails
        """
        message = "Start getting members of the current team"
        _log_message(self._logger, DEBUG, message)
        results = self._http_utils.get("teams/current/members")
        message = "Finish getting members of the current team"
        _log_message(self._logger, DEBUG, message, results)
        return results
