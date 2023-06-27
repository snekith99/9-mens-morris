from __future__ import annotations

import random
import time

from actions.fly_action import FlyAction
from actions.move_action import MoveAction
from actions.place_action import PlaceAction
from actions.remove_action import RemoveAction
from board_model.position import Position
from players.player import Player

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Computer(Player):
    def __init__(self, game_manager: GameManager, name: str) -> None:
        """
        Initialising computer class

        Args:
            game_manager (GameManager): Player to execute action using gamemanager
        """
        super().__init__(game_manager, name)
        self._move_time = None

    def get_random_available_position(self, current_selected_piece=None) -> Position:
        """
        Getting random available position

        Args:
            current_selected_piece (Piece, optional): Current selected piece. Defaults to None.

        Returns:
            Position: Randomly selected position
        """
        available_positions: list = self.get_positions_from_origin(
            current_selected_piece
        )
        random_position: Position = random.choice(available_positions)
        return self.game_manager.get_board().get_position_by_index(random_position)

    def get_positions_from_origin(self, origin: Position) -> list:
        """
        Gets positions from origin

        Args:
            origin (Position): Origin position

        Returns:
            list: List of available positions
        """
        self.game_manager.get_action_controller().set_current_selected_position(origin)
        available_positions: list = (
            self.game_manager.get_action_controller()
            .get_current_action_handler()
            .get_available_moves()
        )
        return available_positions

    def create_place_action(self) -> bool:
        """
         Computer creating a place action

        Returns:
            bool: Returns true if placed successfully
        """
        position: Position = self.get_random_available_position()
        place_action = PlaceAction(position, self.game_manager)
        return place_action.execute()

    def create_fly_action(self) -> bool:
        """
        Computer creating a fly action
        """
        origin: Position = self.get_random_origin()
        destination: Position = self.get_random_available_position(origin)
        fly_action = FlyAction(origin, destination, self.game_manager)
        return fly_action.execute()

    def create_remove_action(self) -> bool:
        """
        Computer creating a remove action
        """
        position: Position = self.get_random_available_position()
        remove_action = RemoveAction(position, self.game_manager)
        return remove_action.execute()

    def create_move_action(self) -> bool:
        """
        Computer creating a move action
        """
        # set highlighted piece randomly, then get available positions
        origin: Position = self.get_random_origin()
        destination: Position = self.get_random_available_position(origin)
        move_action = MoveAction(origin, destination, self.game_manager)
        return move_action.execute()

    def get_random_origin(self) -> Position:
        """
        Gets random position

        Raises:
            Exception: No available moves

        Returns:
            Position: Position of random origin
        """
        is_green: bool = self.game_manager.get_is_player1_turn()
        possible_origins: list[
            Position
        ] = self.game_manager.get_board().get_positions_from_colour(is_green)
        random.shuffle(possible_origins)

        for origin in possible_origins:
            available_positions: list = self.get_positions_from_origin(origin)
            if len(available_positions) > 0:
                return origin

        raise Exception("No available moves. Game should already be over")

    def get_move_time(self) -> float | None:
        """
        Gets move time

        Returns:
            float | None: move time or none if no move time
        """
        return self._move_time

    def set_move_time(self) -> None:
        """
        Sets move time
        """
        if self._move_time is None:
            self._move_time: float = time.time() + random.random() * 2 + 1

    def is_time_to_move(self) -> bool:
        """
        If time to move

        Returns:
            bool: True if time to move
        """
        if time.time() >= self._move_time:
            self._move_time = None
            return True
        return False
