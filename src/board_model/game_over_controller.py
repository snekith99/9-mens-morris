from __future__ import annotations

from typing import TYPE_CHECKING

from pygame_widgets.button import Button

from board_model.board import Board
from screens.display import Display

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class GameOverController:
    def __init__(
        self, game_manager: GameManager, board: Board, display: Display
    ) -> None:
        """
        Initialising game over controller

        Args:
            game_manager (GameManager): Game manager
            board (Board): Board that is currently being played on
            display (Display): Display that pygame is using
        """
        self._board: Board = board
        self._display: Display = display
        self._game_manager: GameManager = game_manager

        self._restart_button: Button = self._display.create_end_of_game_restart_button(
            self.button_callback
        )
        self.hide_restart_button()

    def is_game_over(self) -> bool:
        """
        Checks if game is over

        Returns:
            bool: True if the game is over, otherwise false
        """
        if winner_name := self._board.is_game_over():
            if not self._restart_button.isVisible():
                self._display.get_sound_controller().play_winner_sound()
                self._restart_button.show()

            self._display.draw_winner_dialogue(winner_name)
            return True
        return False

    def button_callback(self) -> None:
        """
        Initialises game
        """
        self._game_manager.initialise_game()

    def get_restart_button(self) -> Button:
        """
        Returns restart button

        Returns:
            Button: Restart button
        """
        return self._restart_button

    def hide_restart_button(self) -> None:
        """
        Hides restart button
        """
        if self._restart_button:
            self._restart_button.hide()
