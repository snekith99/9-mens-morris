from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Literal

from board_model.mill_manager import MillManager
from board_model.piece import Piece
from board_model.position import Position

if TYPE_CHECKING:
    from game_manager import GameManager

    from .piece import Piece

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Board:
    def __init__(self, game_manager: GameManager) -> None:
        """
        Initialising Board class

        Args:
            game_manager (GameManager): GameManager to make changes to board
        """
        self._positions: List[Position] = []
        self._game_manager: GameManager = game_manager
        self._mill_manager = MillManager(self)
        self._create_positions()

    def reset(self) -> None:
        """
        Resetting board
        """
        self.__init__(self._game_manager)

    def get_positions(self) -> List[Position]:
        """
        Get position list

        Returns:
            list: Position list
        """

        return self._positions

    def get_occupied_positions(self) -> list:
        """
        Get occupied positions

        Returns:
            list: List of occupied positions
        """
        return [position for position in self._positions if position.is_occupied()]

    def get_positions_from_colour(self, is_green=True) -> list:
        """
        Get coloured pieces

        Args:
            is_green (bool, optional): Whether to get green or blue pieces. Defaults to True.

        Returns:
            list: List of coloured pieces
        """
        return [
            position
            for position in self._positions
            if position.get_piece() is not None
            and position.get_piece().get_is_green() == is_green
        ]

    def get_empty_positions(self) -> list:
        """
        Get empty positions

        Returns:
            list: List of empty positions
        """
        return [position for position in self._positions if not position.is_occupied()]

    def get_mill_manager(self) -> MillManager:
        """
        Get mill manager

        Returns:
            MillManager: Mill manager
        """
        return self._mill_manager

    def add_piece(self, position: Position, piece: Piece) -> None:
        """
        Adding piece to piece_list and decrementing token count

        Args:
            piece (Piece): Piece to be added
        """

        position.set_piece(piece)
        self._game_manager.increment_token_board()
        self._game_manager.decrement_token_count()

    def get_piece_from_position(self, position: Position) -> Piece | None:
        """
        Gets piece from the position

        Args:
            position (Position): Position where piece is located

        Returns:
            Piece | None: Either returns the piece or None if there's no piece on that position
        """
        return position.get_piece()

    def move_piece(self, source: Position, destination: Position) -> None:
        """
        Moving piece to destination position

        Args:
            piece (Piece): Piece to be moved
            destination (Position): Destination position to move the piece
        """
        piece: Piece = source.get_piece()
        source.set_piece(None)
        destination.set_piece(piece)

    def remove_piece(self, position: Position) -> None:
        """
        Removing piece from the position

        Args:
            position (Position): Position to remove piece from
        """
        position.set_piece(None)

        if (
            self._game_manager.get_mover_name()
            == self._game_manager.get_player1().get_name()
        ):
            self._game_manager.decrement_blue_board()
        else:
            self._game_manager.decrement_green_board()

    def get_piece_list(self) -> list[Piece]:
        """
        Get piece list

        Returns:
            list: Piece list
        """
        piece_list = []
        for position in self._positions:
            if position.get_piece() is not None:
                piece_list.append(position.get_piece())
        return piece_list

    def _create_positions(self) -> None:
        """
        Creating positions on board and adding neighbours
        """
        # list of coordinates for each position in the game board
        piece_locations = (
            (458, 297),
            (641, 297),
            (822, 297),
            (514, 354),
            (640, 354),
            (765, 354),
            (569, 408),
            (640, 408),
            (711, 408),
            (458, 479),
            (514, 479),
            (569, 479),
            (711, 479),
            (765, 479),
            (822, 479),
            (569, 551),
            (640, 551),
            (711, 551),
            (514, 605),
            (641, 605),
            (766, 605),
            (458, 662),
            (640, 662),
            (822, 662),
        )

        # List of neighbours for each position in the game board (ordered by each piece's index)
        neighbours = [
            {"top": None, "bottom": 9, "left": None, "right": 1},
            {"top": None, "bottom": 4, "left": 0, "right": 2},
            {"top": None, "bottom": 14, "left": 1, "right": None},
            {"top": None, "bottom": 10, "left": None, "right": 4},
            {"top": 1, "bottom": 7, "left": 3, "right": 5},
            {"top": None, "bottom": 13, "left": 4, "right": None},
            {"top": None, "bottom": 11, "left": None, "right": 7},
            {"top": 4, "bottom": None, "left": 6, "right": 8},
            {"top": None, "bottom": 12, "left": 7, "right": None},
            {"top": 0, "bottom": 21, "left": None, "right": 10},
            {"top": 3, "bottom": 18, "left": 9, "right": 11},
            {"top": 6, "bottom": 15, "left": 10, "right": None},
            {"top": 8, "bottom": 17, "left": None, "right": 13},
            {"top": 5, "bottom": 20, "left": 12, "right": 14},
            {"top": 2, "bottom": 23, "left": 13, "right": None},
            {"top": 11, "bottom": None, "left": None, "right": 16},
            {"top": None, "bottom": 19, "left": 15, "right": 17},
            {"top": 12, "bottom": None, "left": 16, "right": None},
            {"top": 10, "bottom": None, "left": None, "right": 19},
            {"top": 16, "bottom": 22, "left": 18, "right": 20},
            {"top": 13, "bottom": None, "left": 19, "right": None},
            {"top": 9, "bottom": None, "left": None, "right": 22},
            {"top": 19, "bottom": None, "left": 21, "right": 23},
            {"top": 14, "bottom": None, "left": 22, "right": None},
        ]

        for i in range(len(piece_locations)):
            self._positions.append(Position(piece_locations[i], neighbours[i], i))

    def is_pieces_placed(self) -> bool:
        """
        Checking if all pieces have been placed

        Returns:
            bool: True if all pieces have been placed
        """
        return (
            self._game_manager.get_blue_token_count() == 0
            and self._game_manager.get_green_token_count() == 0
        )

    def get_mills(self) -> list:
        """
        Checks the board for the presence of mills
        """
        mills = []
        for position in self._positions:
            if position.is_occupied():
                neighbours = position.get_neighbours()
                # Checks if the position has neighbours on both sides of the position
                for direction in (("top", "bottom"), ("left", "right")):
                    if (
                        neighbours[direction[0]] is not None
                        and neighbours[direction[1]] is not None
                    ):
                        top_piece: Piece = self.get_position_by_index(
                            neighbours[direction[0]]
                        ).get_piece()
                        middle_piece: Piece = position.get_piece()
                        bottom_piece: Piece = self.get_position_by_index(
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

    def compare_mills(self, mills: list) -> Any | None:
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

    def get_new_mill(self) -> Any | None:
        """
        Gets the new mill

        Returns:
            Any | None: New mill if present, otherwise None
        """

        mills: list = self.get_mills()
        return self.compare_mills(mills)

    def get_position_by_index(self, index: int) -> Position:
        """
        Gets position at index

        Args:
            index (int): Index with position

        Raises:
            Exception: If incorrect index is given, no position present at index

        Returns:
            Position: Position at index
        """
        for position in self._positions:
            if position.get_index() == index:
                return position

        raise Exception(f"Incorrect index given {index}")

    def get_all_available_moves(self) -> List[int]:
        """
        Returns all available moves

        Returns:
            List[int]: List of available moves
        """
        origin = self._game_manager._action_controller.get_current_selected_position()
        all_available_moves = []
        for position in self._positions:
            if position.is_occupied() and self._game_manager.is_current_players_piece(
                position
            ):
                self._game_manager._action_controller.set_current_selected_position(
                    position
                )
            all_available_moves += (
                self._game_manager._action_controller.get_current_action_handler().get_available_moves()
            )

        self._game_manager._action_controller.set_current_selected_position(origin)
        return list(set(all_available_moves))

    def is_game_over(self) -> str | Literal[False]:
        """
        Checks if game is over

        Returns:
            str | Literal[False]: Game over or not signal
        """
        if self._game_manager._board.is_pieces_placed():
            if self._game_manager.get_blue_pieces_on_board() <= 2:
                return self._game_manager.get_player1().get_name()
            elif self._game_manager.get_green_pieces_on_board() <= 2:
                return self._game_manager.get_player2().get_name()
            elif self.get_all_available_moves() == []:
                return self._game_manager.get_other_player().get_name()
        return False
