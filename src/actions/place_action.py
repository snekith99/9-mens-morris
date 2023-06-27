from __future__ import annotations

from typing import TYPE_CHECKING

from actions.action import Action
from board_model.piece import Piece
from board_model.position import Position

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class PlaceAction(Action):
    def __init__(self, destination: Position, game_manager: GameManager) -> None:
        """
        Initialising PlaceAction class

        Args:
            position (Position): Position to place piece
            game_manager (GameManager): GameManager to modify board
        """
        super().__init__(game_manager)
        self._destination: Position = destination

    def execute(self) -> None:
        """
        Creates a piece and adds it to the board
        """

        self._game_manager.get_display().get_sound_controller().place_piece_sound()

        is_player1_to_move: bool = self._game_manager.get_is_player1_turn()
        self._game_manager.get_display().get_token_renderer().get_animation_handler().add_animation(
            self._destination, is_player1_to_move, start_radius=0, duration=1
        )  # spawn animation between origin and destination
        self._board.add_piece(self._destination, Piece(is_player1_to_move))
