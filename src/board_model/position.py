from __future__ import annotations

import CONSTANTS
from screens.renderable_token import RenderableToken

from typing import TYPE_CHECKING, List, Tuple, TypedDict

import pygame
from pygame import Rect

if TYPE_CHECKING:
    from .piece import Piece

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Neighbours(TypedDict):
    """
    Responsible for the neighbours of a position

    Args:
        TypedDict (TypedDict): A typed dictionary containing the index of the neighbours in the position list at either left, right, top or bottom else None
    """

    top: int | None
    bottom: int | None
    left: int | None
    right: int | None


class Position(RenderableToken):
    def __init__(
        self,
        center: Tuple[int, int],
        neighbours: Neighbours,
        index: int,
        piece: Piece = None,
    ) -> None:
        """
        Initialising Position class

        Args:
            center (Tuple[int, int]): Centre of position in the form [x, y]
            neighbours (Neighbours): Neighbours of a position. Contains the index of the neighbours in the position list at either left, right, top or bottom else None
            index (int): Index of position in position list
            is_occupied (bool, optional): Boolean to see if position is occupied by another piece. Defaults to False.
            piece (Piece): Piece at position
        """

        self.index: int = index
        self.radius = CONSTANTS.BOARD_TOKEN_RADIUS
        self.x_pos: int = center[0]
        self.y_pos: int = center[1]
        self._piece = piece
        self.neighbours: Neighbours = neighbours
        self.rect = pygame.Rect(
            self.x_pos - self.radius,
            self.y_pos - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def get_x_pos(self) -> int:
        """
        Gets x coordinate of position

        Returns:
            float: X coordinate of position
        """

        return self.x_pos

    def get_y_pos(self) -> int:
        """
        Gets y coordinate of position

        Returns:
            float: Y coordinate of position
        """

        return self.y_pos

    def get_neighbours(self) -> Neighbours:
        """
        Gets list of all neighbours

        Returns:
            Neighbours: A typed dictionary containing the index of the neighbours in the position list at either left, right, top or bottom else None
        """

        return self.neighbours

    def get_rect(self) -> Rect:
        """
        Gets pygame Rectangle

        Returns:
            Rect: pygame Rectangle for position
        """

        return self.rect

    def get_radius(self) -> int:
        """
        Gets radius

        Returns:
            int: Returns radius as an int
        """
        return self.radius

    def is_occupied(self) -> bool:
        """
        Gets boolean if occupied

        Returns:
            bool: if position is occupied by another piece
        """

        return self._piece is not None

    def get_piece(self) -> Piece:
        """
        Gets piece at position

        Returns:
            Piece: Piece at position
        """

        return self._piece

    def set_piece(self, piece: Piece) -> None:
        """
        Sets piece at current position

        Args:
            piece (Piece): New piece to be assigned at position
        """
        self._piece: Piece = piece

    def get_index(self) -> int:
        """
        Returns index of position

        Returns:
            int: Index of position
        """
        return self.index

    def get_adjacent_piece_indexes(self) -> List[int]:
        """
        Gets indexes of adjacent pieces

        Returns:
            List[int]: List of adjancent pieces' index
        """
        return [
            neighbour
            for neighbour in self.get_neighbours().values()
            if neighbour is not None
        ]

    def get_is_green(self) -> bool:
        """
        Checks if green position

        Returns:
            bool: True if green
        """
        return self._piece.get_is_green()
