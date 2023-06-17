from typing import List, Literal

from action_handlers.action_handler import ActionHandler
from actions.move_type import MoveType
from board_model.position import Position
from players.computer import Computer

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class MoveActionHandler(ActionHandler):
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
        Get available moves

        Returns:
            List[int]: List of available moves
        """
        if self._action_controller._current_selected_position is None:
            return []

        available_moves: List[int] = []
        adjacent_pieces: List[
            int
        ] = (
            self._action_controller._current_selected_position.get_adjacent_piece_indexes()
        )
        for position_index in adjacent_pieces:
            position: Position = (
                self._action_controller._game_manager._board.get_position_by_index(
                    position_index
                )
            )
            if not position.is_occupied():
                available_moves.append(position_index)
        return available_moves

    def get_move_type(self) -> Literal[MoveType.MOVE]:
        """
        Get move type

        Returns:
            Literal[MoveType.MOVE]: Move type
        """
        return MoveType.MOVE

    def handle_ai_action(self, computer: Computer) -> None:
        """
        Handles AI action

        Args:
            computer (Computer): Computer's turn
        """
        computer.create_move_action()
        self._action_controller._game_manager.toggle_move()
