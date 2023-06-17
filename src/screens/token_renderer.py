from __future__ import annotations

from typing import TYPE_CHECKING, List

from actions.move_type import MoveType
from board_model.piece import Piece
from board_model.position import Position
from screens.animated_piece import AnimatedPiece
from screens.animation_handler import AnimationHandler
from screens.outline import Outline

if TYPE_CHECKING:
    from game_manager import GameManager
    from screens.display import Display

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class TokenRenderer:
    def __init__(self, display: Display, game_manager: GameManager) -> None:
        """
        Render tokens

        Args:
            display (Display): Display to render token
            game_manager (GameManager): Game manager
        """
        self._display: Display = display
        self._game_manager: GameManager = game_manager
        self._animation_handler = AnimationHandler(self._game_manager.get_board())

    def render_token_elements(self, mills: List[List[int]] | None) -> None:
        """
        Render token elements

        Args:
            mills (List[List[int]] | None): List of mills
        """

        self._animation_handler.tick()  # update animations

        current_selection: Position = (
            self._game_manager._action_controller.get_current_selected_position()
        )

        self._render_mill_indicator_lines(
            self._animation_handler.get_static_mills(mills)
        )

        # Render orange lines
        if self._animation_handler.get_animating_mill_progress(mills) > 0.75:
            self._render_mill_indicator_lines(
                self._animation_handler.get_animating_mills(mills)
            )

        self._render_tokens(self._animation_handler.get_static_pieces())

        # Render outlines

        self._render_mill_token_outlines(
            self._animation_handler.get_static_mills(mills)
        )
        self._render_available_moves()

        self._render_tokens(self._animation_handler.get_animating_pieces())
        self._render_mill_token_outlines(
            self._animation_handler.get_animating_mills(mills)
        )

        self._render_selected_piece_outline(current_selection)

    def _render_mill_indicator_lines(self, mills: List[List[int]] | None) -> None:
        """
        Rendering UI for the line of a mill

        Args:
            mills (List[List[int]] | None): List of mills
        """

        if not mills:
            return

        for mill in mills:
            outline = Outline.ORANGE
            position: Position = self._game_manager._board.get_position_by_index(
                mill[0]
            )
            last_position: Position = self._game_manager._board.get_position_by_index(
                mill[-1]
            )
            self._display.draw_line(
                outline,
                (position.get_x_pos(), position.get_y_pos()),
                (last_position.get_x_pos(), last_position.get_y_pos()),
            )

    def _render_mill_token_outlines(self, mills: List[List[int]] | None) -> None:
        """
        Rendering the UI for mills

        Args:
            mills (List[List[int]] | None): List of mills
        """

        if not mills:
            return

        animating_pieces_in_mill: list[
            AnimatedPiece
        ] = self._animation_handler.get_animating_pieces_in_mills(mills)
        animated_piece_indexes = []

        # animate on the animated piece
        for animating_piece in animating_pieces_in_mill:
            animated_piece_indexes.append(animating_piece.get_destination_piece_index())
            self._display.draw_outline(
                animating_piece.get_x_pos(),
                animating_piece.get_y_pos(),
                animating_piece.get_radius(),
                Outline.ORANGE,
            )

        for mill in mills:
            outline = Outline.ORANGE
            for piece_index in mill:
                if piece_index not in animated_piece_indexes:
                    position: Position = (
                        self._game_manager._board.get_position_by_index(piece_index)
                    )
                    self._display.draw_outline(
                        position.get_x_pos(),
                        position.get_y_pos(),
                        position.get_radius(),
                        outline,
                    )

    def _render_tokens(self, tokens: list[Piece]) -> None:
        """
        Render tokens according to the state of the board
        """

        for position in tokens:
            self._display.draw_token(
                position.get_x_pos(),
                position.get_y_pos(),
                position.get_radius(),
                position.get_is_green(),
            )

    def _render_available_moves(self) -> None:
        """
        Rendering the available moves
        """

        if (
            self._game_manager._action_controller.get_current_action_handler().get_move_type()
            == MoveType.REMOVE
        ):
            outline = Outline.RED

        elif self._game_manager.get_is_player1_turn():
            outline = Outline.GREEN

        else:
            outline = Outline.BLUE

        for position in self._game_manager._board.get_positions():
            if (
                position.get_index()
                in self._game_manager._action_controller.get_current_action_handler().get_available_moves()
            ):
                # Draw outline if position in available moves
                self._display.draw_outline(
                    position.get_x_pos(),
                    position.get_y_pos(),
                    position.get_radius(),
                    outline,
                )

    def _render_selected_piece_outline(self, current_selection: Position) -> None:
        """
        Rendering the selected piece outline

        Args:
            current_selection (Position): Drawing border around current selected piece
        """
        if not current_selection:
            return

        outline = Outline.YELLOW
        self._display.draw_outline(
            current_selection.get_x_pos(),
            current_selection.get_y_pos(),
            current_selection.get_radius(),
            outline,
        )

    def get_animation_handler(self) -> AnimationHandler:
        """
        Get the animation handler

        Returns:
            AnimationHandler: Animation handler
        """
        return self._animation_handler
