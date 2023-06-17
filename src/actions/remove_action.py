from __future__ import annotations

from typing import TYPE_CHECKING

from actions.action import Action

if TYPE_CHECKING:
    from board_model.position import Position
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class RemoveAction(Action):
    def __init__(self, position: Position, game_manager: GameManager) -> None:
        """
        Initialising the RemoveAction class with game manager and board

        Args:
            origin (Position): The start location of the piece
            game_manager (GameManager): Game Manager that will be performing this move
        """
        super().__init__(game_manager)
        self._position: Position = position

    def execute(self) -> None:
        """
        Moves the piece from the origin to the destination. The origin is reassigned if the user clicks another one of their pieces.
        """
        self._game_manager.get_display().get_sound_controller().remove_piece_sound()

        self._game_manager.get_display().get_token_renderer().get_animation_handler().add_animation(
            self._position, self._position.get_is_green(), end_radius=0, duration=0.1
        )  # spawn animation between origin and destination
        self._board.remove_piece(self._position)
