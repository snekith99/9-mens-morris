from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from board_model.board import Board

from board_model.piece import Piece
from board_model.position import Neighbours

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class MillManager:
    def __init__(self, board: Board) -> None:
        """
        Initialises mill manager

        Args:
            board (Board): Board
        """
        self.mills: list = []
        self._board: Board = board

    def get_mills(self) -> list:
        """
        Checks the board for the presence of mills
        """
        mills: list = []
        for position in self._board.get_occupied_positions():
            neighbours: Neighbours = position.get_neighbours()
            # Checks if the position has neighbours on both sides of the position
            for direction in (("top", "bottom"), ("left", "right")):
                if (
                    neighbours[direction[0]] is not None
                    and neighbours[direction[1]] is not None
                ):
                    top_piece: Piece = self._board.get_position_by_index(
                        neighbours[direction[0]]
                    ).get_piece()
                    middle_piece: Piece = position.get_piece()
                    bottom_piece: Piece = self._board.get_position_by_index(
                        neighbours[direction[1]]
                    ).get_piece()

                    if top_piece is None or bottom_piece is None:
                        continue

                    if (
                        top_piece.get_is_green() == bottom_piece.get_is_green()
                        and top_piece.get_is_green() == middle_piece.get_is_green()
                    ):  # check if there are pieces of the same colour on either side of the piece
                        mills.append(
                            [
                                neighbours[direction[0]],
                                position.get_index(),
                                neighbours[direction[1]],
                            ]
                        )
        return mills

    def compare_mills(self, mills: list) -> List[int] | None:
        """
        Returns new mill if present

        Args:
            mills (list): List of mills

        Returns:
            Any | None: New mill if present, otherwise None
        """

        new_mill = None

        for mill in mills:
            if mill not in self.mills:
                new_mill = mill
                break

        self.mills = mills

        return new_mill

    def get_new_mill(self) -> List[int] | None:
        """
        Gets the new mill

        Returns:
            Any | None: New mill if present, otherwise None
        """

        mills = self.get_mills()
        return self.compare_mills(mills)
