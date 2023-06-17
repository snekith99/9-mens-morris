from __future__ import annotations

from abc import ABC, abstractmethod
from board_model.position import Position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Player(ABC):
    def __init__(self, game_manager: GameManager, name: str) -> None:
        """
        Initialising player class

        Args:
            game_manager (GameManager): Player to execute action using gamemanager
            name (str): Name of player
        """
        self.game_manager: GameManager = game_manager
        self.name: str = name
        self.pieces = 9
        self.pieces_on_board = 0

    def get_name(self) -> str:
        """
        Gets player name

        Returns:
            str: Player name
        """
        return self.name

    def get_pieces_left(self) -> int:
        """
        Get pieces left to place

        Returns:
            int: Pieces left to place
        """
        return self.pieces

    def get_pieces_on_board(self) -> int:
        """
        Gets pieces on board for player

        Returns:
            int: Pieces on board for player
        """
        return self.pieces_on_board

    def decrement_piece_count(self) -> None:
        """
        Decrements piece count: When player places a piece
        """
        self.pieces -= 1

    def decrement_piece_on_board(self) -> None:
        """
        Decrements piece count on board
        """
        self.pieces_on_board -= 1

    def increment_piece_on_board(self) -> None:
        """
        Increments piece count on board
        """
        self.pieces_on_board += 1

    @abstractmethod
    def create_place_action() -> bool:
        """
        Abstract method for creating a place action

        Args:
            position (Position): Position to create piece
        """
        raise NotImplementedError

    @abstractmethod
    def create_move_action() -> bool:
        """
        Abstract method for moving a piece

        Args:
            origin (Position): Source position
            destination (Position): Destination position
        """
        raise NotImplementedError

    @abstractmethod
    def create_remove_action() -> bool:
        """
        Abstract method for removing a piece

        Args:
            position (Position): Position to remove the piece
        """
        raise NotImplementedError

    @abstractmethod
    def create_fly_action() -> bool:
        """
        Abstract method for flying a piece

        Args:
            origin (Position): Source position
            destination (Position): Destination position
        """
        raise NotImplementedError
