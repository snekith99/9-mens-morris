from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from board_model.position import Position

if TYPE_CHECKING:
    from players.computer import Computer
    from actions.action_controller import ActionController

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class ActionHandler(ABC):
    def __init__(self, action_controller: ActionController) -> None:
        """
        Responsible for handling actions

        Args:
            action_controller (ActionController): Action controller
        """
        self._action_controller: ActionController = action_controller

    @abstractmethod
    def handle_ai_action(self, computer: Computer) -> None:
        """
        Handle AI action
        """
        raise NotImplementedError

    @abstractmethod
    def handle_action(self, destination: Position) -> Any:
        """
        Abstract method to handle action

        Args:
            destination (Position): Destination position
        """
        raise NotImplementedError

    @abstractmethod
    def get_available_moves(self) -> Any:
        """
        Gets available moves
        """
        raise NotImplementedError

    @abstractmethod
    def get_move_type(self) -> Any:
        """
        Gets move type
        """
        raise NotImplementedError
