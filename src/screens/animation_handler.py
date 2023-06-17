import CONSTANTS
from board_model.board import Board
from board_model.position import Position
from screens.animated_piece import AnimatedPiece

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class AnimationHandler:
    def __init__(self, board: Board) -> None:
        """
        Initialises animation handler. Handle the locations of each *animated* piece.
        Change the rendering of the from get occupied locations to get piece animated locations
        """
        self._current_animations: list[AnimatedPiece] = []
        self._board: Board = board

    def tick(self) -> None:
        """
        Updates the animation
        """
        for animation in self._current_animations:
            is_completed: bool = animation.tick()
            if is_completed:
                self.terminate_animation(animation)

    def add_animation(self, start_position: Position, is_green: bool, **kwargs) -> None:
        """
        Adds an animation to the animation handler

        Args:
            animation (Animation): Animation to be added
        """
        defaultKwargs = {
            "end_radius": CONSTANTS.BOARD_TOKEN_RADIUS,
            "start_radius": CONSTANTS.BOARD_TOKEN_RADIUS,
            "end_position": start_position,
            "duration": 1,
        }
        kwargs = {**defaultKwargs, **kwargs}

        animating_piece = AnimatedPiece(
            start_position.get_x_pos(),
            start_position.get_y_pos(),
            kwargs["end_position"].get_x_pos(),
            kwargs["end_position"].get_y_pos(),
            kwargs["start_radius"],
            kwargs["end_radius"],
            kwargs["end_position"].get_index(),
            is_green,
            kwargs["duration"],
        )
        self._current_animations.append(animating_piece)

    def terminate_animation(self, animation: AnimatedPiece) -> None:
        """
        Terminates an animation

        Args:
            animation (Animation): Animation to be terminated
        """
        self._current_animations.remove(animation)

    def get_current_animations(self) -> list[AnimatedPiece]:
        """
        Gets the current animations

        Returns:
            list[Animation]: List of current animations
        """
        return self._current_animations

    def clear_animations(self) -> None:
        """
        Clears all animations
        """
        self._current_animations = []

    def get_animating_pieces(self) -> list[AnimatedPiece]:
        """
        Gets animating pieces

        Returns:
            list[AnimatedPiece]: List of animated pieces
        """
        return [animation for animation in self._current_animations]

    def get_static_pieces(self) -> list:
        """
        Gets static pieces

        Returns:
            list: List of static pieces
        """
        return [
            piece
            for piece in self._board.get_occupied_positions()
            if piece.get_index()
            not in [
                animation.get_destination_piece_index()
                for animation in self._current_animations
            ]
        ]

    def is_animating(self) -> bool:
        """
        Checks if animating

        Returns:
            bool: True if animating
        """
        return len(self._current_animations) > 0

    def get_animating_pieces_in_mills(self, mills: list) -> list[AnimatedPiece]:
        """
        Gets animating pieces in mills

        Args:
            mills (list): List of mills

        Returns:
            list[AnimatedPiece]: List of animated pieces
        """
        flattened_mills: list = [mill for mill in mills for mill in mill]
        return [
            animation
            for animation in self._current_animations
            if animation.get_destination_piece_index() in flattened_mills
        ]

    def get_animating_mills(self, mills: list) -> list:
        """
        Gets animating mills

        Args:
            mills (list): List of mills

        Returns:
            list: Animating mills
        """
        animating_mills: list = []
        for mill in mills:
            for index in mill:
                if index in [
                    animation.get_destination_piece_index()
                    for animation in self._current_animations
                ]:
                    animating_mills.append(mill)
                    break
        return animating_mills

    def get_static_mills(self, mills: list) -> list:
        """
        Gets static mills

        Args:
            mills (list): List of mills

        Returns:
            list: Static mills
        """
        static_mills: list = []
        animating_mills: list = self.get_animating_mills(mills)
        for mill in mills:
            if mill not in animating_mills:
                static_mills.append(mill)
        return static_mills

    def get_animating_mill_progress(self, mills: list) -> int:
        """
        Gets progress of animating mills

        Args:
            mills (list): List of mills

        Returns:
            int: 1 if in progress
        """
        animating_pieces_in_mills: list[
            AnimatedPiece
        ] = self.get_animating_pieces_in_mills(mills)
        if len(animating_pieces_in_mills) == 0:
            return 1

        return min(
            [animation.get_progress() for animation in animating_pieces_in_mills]
        )
