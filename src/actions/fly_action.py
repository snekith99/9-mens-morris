from __future__ import annotations

from actions.action import Action
from board_model.position import Position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class FlyAction(Action):
    def __init__(
        self, origin: Position, destination: Position, game_manager: GameManager
    ) -> None:
        """
        Initialising the FlyAction class with the origin, destination and gamemanager

        Args:
            origin (Position): The start location of the piece
            game_manager (GameManager): Game Manager that will be performing this fly action
        """
        super().__init__(game_manager)
        self._origin: Position = origin
        self._destination: Position = destination

    def execute(self) -> None:
        """
        Moves the piece from the origin to the destination. The origin is reassigned if the user clicks another one of their pieces.
        """
        self._game_manager.get_display().get_sound_controller().piece_move_sound()
        self._game_manager.get_display().get_token_renderer().get_animation_handler().add_animation(
            self._origin,
            self._origin.get_is_green(),
            end_position=self._destination,
            duration=0.75,
        )  # spawn animation between origin and destination

        self._board.move_piece(self._origin, self._destination)
