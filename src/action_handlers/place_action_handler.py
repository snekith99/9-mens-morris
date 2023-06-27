from typing import List, Literal

from action_handlers.action_handler import ActionHandler
from actions.move_type import MoveType
from board_model.position import Position
from players.computer import Computer

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class PlaceActionHandler(ActionHandler):
    def handle_action(self, destination: Position) -> bool:
        """
        Responsible for handling the place action

        Args:
            position (Position): Position to place piece

        Returns:
            Literal[True]: If the place has been completed, return True
        """
        if destination.get_index() in self.get_available_moves():
            self._action_controller._game_manager.get_current_player().create_place_action(
                destination
            )
            self._action_controller._game_manager.toggle_move()
            return True
        return False

    def get_available_moves(self) -> List[int]:
        """
        Get available moves

        Returns:
            List[int]: List of available moves
        """
        available_moves: List[int] = []
        for (
            position
        ) in self._action_controller._game_manager._board.get_empty_positions():
            available_moves.append(position.get_index())
        return available_moves

    def get_move_type(self) -> Literal[MoveType.PLACE]:
        """
        Get move type

        Returns:
            Literal[MoveType.PLACE]: Move type
        """
        return MoveType.PLACE

    def handle_ai_action(self, computer: Computer) -> None:
        """
        Handles AI Action

        Args:
            computer (Computer): Computer's turn
        """
        computer.create_place_action()
        self._action_controller._game_manager.toggle_move()
