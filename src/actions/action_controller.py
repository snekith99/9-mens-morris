from __future__ import annotations

from typing import TYPE_CHECKING

from action_handlers.action_handler import ActionHandler
from action_handlers.fly_action_handler import FlyActionHandler
from action_handlers.move_action_handler import MoveActionHandler
from action_handlers.place_action_handler import PlaceActionHandler
from action_handlers.remove_action_handler import RemoveActionHandler
from actions.move_type import MoveType
from board_model.position import Position
from players.computer import Computer

if TYPE_CHECKING:
    from game_manager import GameManager

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class ActionController:
    def __init__(self, game_manager: GameManager) -> None:
        """
        Initialises action controller

        Args:
            game_manager (GameManager): Game manager the action controller will be manipulating
        """
        self._current_selected_position: Position = None
        self._move_type: MoveType = MoveType.PLACE
        self._game_manager: GameManager = game_manager
        self._current_action_handler = PlaceActionHandler(self)

    def get_current_action_handler(self) -> ActionHandler:
        """
        Gets current action handler

        Returns:
            ActionHandler: Current action handler
        """
        return self._current_action_handler

    def set_current_action_handler(self, action_handler: ActionHandler) -> None:
        """
        Set current action handler

        Args:
            action_handler (ActionHandler): New action handler
        """
        self._current_action_handler: ActionHandler = action_handler

    def get_game_manager(self) -> GameManager:
        """
        Gets game manager

        Returns:
            GameManager: Game Manager
        """
        return self._game_manager

    def get_move_type(self) -> MoveType:
        """
        Gets current move type

        Returns:
            MoveType: Current move type
        """
        return self._current_action_handler.get_move_type()

    def get_current_selected_position(self) -> Position:
        """
        Gets current selected position

        Returns:
            Position: Current selected position
        """
        return self._current_selected_position

    def set_current_selected_position(self, position: Position) -> None:
        """
        Sets current selected position

        Args:
            position (Position): Position to be set
        """
        self._current_selected_position: Position = position

    def update_action_handler(self) -> None:
        """
        Updating the move type
        """
        self._current_selected_position = None

        if (
            # checks if the player's pieces are less than 3, if so, give them the ability to fly
            self._game_manager.get_current_player().get_pieces_on_board() <= 3
            and self._game_manager.get_board().is_pieces_placed()
        ):
            self._current_action_handler = FlyActionHandler(self)
            # if the player has more than 3 pieces on the board, they can do a normal move
        elif self._game_manager.get_board().is_pieces_placed():
            self._current_action_handler = MoveActionHandler(self)

        else:
            # if the player has not placed all their pieces, they can only place
            self._current_action_handler = PlaceActionHandler(self)

    def handle_action(self, position: Position) -> bool:
        """
        Handling action

        Args:
            position (Position): Position to do action

        Returns:
            bool: True if updates
        """
        if self._current_action_handler.handle_action(position):
            self.update_action_handler()

    def handle_ai_action(self, computer: Computer):
        """
        Handling AI action
        """
        self._current_action_handler.handle_ai_action(computer)
        self.update_action_handler()

    def initiate_remove(self) -> None:
        """
        Initiating a remove action
        """
        self._game_manager.toggle_move()
        self._current_action_handler = RemoveActionHandler(self)

    def reset(self) -> None:
        """
        Resetting game
        """
        self.__init__(self._game_manager)
