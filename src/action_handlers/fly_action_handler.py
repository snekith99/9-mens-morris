from typing import Literal

from action_handlers.action_handler import ActionHandler
from actions.move_type import MoveType
from players.computer import Computer
from board_model.position import Position

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class FlyActionHandler(ActionHandler):
    def handle_action(self, destination: Position) -> bool | None:
        """
        Responsible for handling the move action

        Args:
            position (Position): Position to move piece
        """
        if destination.get_index() in self.get_available_moves():
            self._action_controller._game_manager.get_current_player().create_move_action(
                self._action_controller._current_selected_position, destination
            )
            self._action_controller._game_manager.toggle_move()
            return True

        elif (
            destination.is_occupied()
            and self._action_controller._game_manager.is_current_players_piece(
                destination
            )
        ):
            self._action_controller.set_current_selected_position(destination)
            return False

    def get_available_moves(self) -> list[int]:
        """
        Gets available moves

        Returns:
            list[int]: List of available moves
        """
        if self._action_controller._current_selected_position is None:
            return []
        return [
            position.get_index()
            for position in self._action_controller._game_manager._board.get_empty_positions()
        ]

    def get_move_type(self) -> Literal[MoveType.FLY]:
        """
        Gets the move type

        Returns:
            Literal[MoveType.FLY]: Gets the move type
        """
        return MoveType.FLY

    def handle_ai_action(self, computer: Computer) -> None:
        """
        Handles AI action

        Args:
            computer (Computer): Computer's turn
        """
        computer.create_fly_action()
        self._action_controller._game_manager.toggle_move()
