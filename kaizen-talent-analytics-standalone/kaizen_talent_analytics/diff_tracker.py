import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DiffWatcher:
    """
    Stateful service to watch and log differences between outputs.
    """

    def __init__(self) -> None:
        self._diffs: List[Dict[str, Any]] = []

    def log_diff(self, prompt_id: str, old_output: str, new_output: str, session_id: str) -> None:
        """
        Log the difference between old and new outputs for a given prompt and session.

        Args:
            prompt_id (str): Identifier for the prompt.
            old_output (str): The previous output.
            new_output (str): The new output.
            session_id (str): Identifier for the session.

        Returns:
            None
        """
        try:
            diff_entry = {
                "prompt_id": prompt_id,
                "old_output": old_output,
                "new_output": new_output,
                "session_id": session_id
            }
            self._diffs.append(diff_entry)
            logger.info(f"Logged diff for prompt_id={prompt_id}, session_id={session_id}")
        except Exception as e:
            logger.error(f"Error logging diff for prompt_id={prompt_id}: {e}")

    def get_diffs(self) -> List[Dict[str, Any]]:
        """
        Retrieve all logged diffs.

        Returns:
            List[Dict[str, Any]]: List of diff entries.
        """
        return self._diffs
