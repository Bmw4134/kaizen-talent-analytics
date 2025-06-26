import logging
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Goal:
    """
    Dataclass representing a goal in the talent analytics system.
    """
    id: str
    description: str
    status: str  # e.g., "pending", "in_progress", "resolved"
    last_updated: Optional[str] = None  # ISO timestamp

class GoalTracker:
    """
    Stateful service to manage goals with in-memory storage.
    """

    def __init__(self) -> None:
        self._goals: Dict[str, Goal] = {}

    def add_goal(self, goal: Goal) -> None:
        """
        Add or update a goal.

        Args:
            goal (Goal): The goal object to add or update.

        Returns:
            None
        """
        try:
            self._goals[goal.id] = goal
            logger.info(f"Goal added/updated: {goal.id}")
        except Exception as e:
            logger.error(f"Error adding/updating goal {goal.id}: {e}")

    def resolve_goal(self, goal_id: str) -> None:
        """
        Mark a goal as resolved.

        Args:
            goal_id (str): The identifier of the goal to resolve.

        Returns:
            None
        """
        try:
            if goal_id in self._goals:
                goal = self._goals[goal_id]
                goal.status = "resolved"
                logger.info(f"Goal resolved: {goal_id}")
            else:
                logger.warning(f"Goal id {goal_id} not found to resolve.")
        except Exception as e:
            logger.error(f"Error resolving goal {goal_id}: {e}")

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """
        Retrieve a goal by its ID.

        Args:
            goal_id (str): The identifier of the goal.

        Returns:
            Optional[Goal]: The goal if found, else None.
        """
        try:
            return self._goals.get(goal_id)
        except Exception as e:
            logger.error(f"Error retrieving goal {goal_id}: {e}")
            return None
