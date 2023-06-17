from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from board_model.board import Board

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Action(ABC):
    def __init__(self, game_manager: GameManager) -> None:
        """
        Action Abstract class for all actions

        Args:
            game_manager (GameManager): Action will manipulate GameManager
        """
        self._game_manager: GameManager = game_manager
        self._board: Board = self._game_manager.get_board()

    @abstractmethod
    def execute(self) -> None:
        """
        Abstract method to perform specific Action
        """
        pass
