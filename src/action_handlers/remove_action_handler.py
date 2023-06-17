from typing import List, Literal

from action_handlers.action_handler import ActionHandler
from actions.move_type import MoveType
from board_model.position import Position
from players.computer import Computer

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class RemoveActionHandler(ActionHandler):
    def handle_action(self, position: Position) -> bool:
        """
        Responsible for handling the remove action

        Args:
            position (Position): Removing piece at position

        Returns:
            Literal[True]: If remove has been completed, return True
        """
        if position.get_index() in self.get_available_moves():
            self._action_controller._game_manager.get_current_player().create_remove_action(
                position
            )
            self._action_controller._game_manager.toggle_move()
            return True
        return False

    def get_available_moves(self) -> List[int]:
        """
        Gets available moves

        Returns:
            List[int]: List of available moves
        """

        available_moves: List[int] = []
        mills = (
            self._action_controller.get_game_manager()
            .get_board()
            .get_mill_manager()
            .get_mills()
        )
        flattened_mills = [mill_index for mill in mills for mill_index in mill]
        for (
            position
        ) in self._action_controller.get_game_manager()._board.get_occupied_positions():
            if not self._action_controller._game_manager.is_current_players_piece(
                position
            ):
                if position.get_index() not in flattened_mills:
                    available_moves.append(position.get_index())

        if (
            len(available_moves) != 0
        ):  # if there are no available moves then you can take from a mill
            return available_moves
        else:
            return [
                position.get_index()
                for position in self._action_controller.get_game_manager()
                .get_board()
                .get_occupied_positions()
                if not self._action_controller.get_game_manager().is_current_players_piece(
                    position
                )
            ]

    def get_move_type(self) -> Literal[MoveType.REMOVE]:
        """
        Gets move type

        Returns:
            Literal[MoveType.REMOVE]: Move type
        """
        return MoveType.REMOVE

    def handle_ai_action(self, computer: Computer) -> None:
        """
        Handles AI action

        Args:
            computer (Computer): Computer's turn
        """
        computer.create_remove_action()
        self._action_controller._game_manager.toggle_move()
