import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SessionRecord:
    """
    Dataclass representing a session record.
    """
    start_time: str
    duration: int
    files_touched: List[str]
    active_modules: List[str]

class SessionLogger:
    """
    Stateful service to log session activities with in-memory storage.
    """

    def __init__(self) -> None:
        self._sessions: List[SessionRecord] = []

    def log_session(self, start_time: str, duration: int, files_touched: List[str], active_modules: List[str]) -> None:
        """
        Log details about a session.

        Args:
            start_time (str): The start time of the session (ISO format).
            duration (int): Duration of the session in seconds.
            files_touched (List[str]): List of file paths touched during the session.
            active_modules (List[str]): List of active module names during the session.

        Returns:
            None
        """
        try:
            if duration < 0:
                raise ValueError("Duration cannot be negative")
            record = SessionRecord(
                start_time=start_time,
                duration=duration,
                files_touched=files_touched,
                active_modules=active_modules
            )
            self._sessions.append(record)
            logger.info(f"Session logged: start_time={start_time}, duration={duration}")
        except Exception as e:
            logger.error(f"Error logging session: {e}")

    def get_sessions(self) -> List[SessionRecord]:
        """
        Retrieve all logged sessions.

        Returns:
            List[SessionRecord]: List of session records.
        """
        return self._sessions
