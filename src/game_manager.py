"""
Responsible for managing the game. The main code in regards to the actions of the game and movements.
"""

from typing import List, Tuple

import pygame
import pygame_widgets
from pygame.event import Event
from pygame.time import Clock

import CONSTANTS
from actions.action_controller import ActionController
from board_model.board import Board
from board_model.game_over_controller import GameOverController
from board_model.position import Position
from players.computer import Computer
from players.human import Human
from players.player import Player
from screens.display import Display

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class GameManager:
    def __init__(self) -> None:
        """
        Initialises GameManager Class
        """
        self._is_vs_computer = False
        self._board = Board(self)
        self._action_controller = ActionController(self)
        self._display = Display(self)
        self._game_over_controller = GameOverController(
            self, self._board, self._display
        )
        self._ai_move_time = None

        self._display.go_to_menu()
        self._render_game()

    def initialise_game(self) -> None:
        """
        Initialise game.

        This function prints a message and resets the game state to the initial values.
        """
        self.get_display().get_sound_controller().play_start_game_sound()
        self._display.get_token_renderer().get_animation_handler().clear_animations()

        self._game_over_controller.hide_restart_button()

        self._board.reset()  # Reset board
        self.player1 = Human(self, "Player 1")
        self.current_player: Player = self.player1

        # Handle conditional whether it is a computer or not
        if not self._is_vs_computer:
            self.player2 = Human(self, "Player 2")
        else:
            self.player2 = Computer(self, "CPU")
        self._action_controller.reset()

    def toggle_move(self) -> bool:
        """
        Toggles the move of the players.

        This function switches the turn of the players by flipping a boolean flag. It returns the updated flag value.

        Returns:
           bool: True if it is player 1's turn, False otherwise.
        """
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def get_is_player1_turn(self) -> bool:
        """
        Checks if it is player 1's turn.

        This function returns the value of the boolean flag that indicates whose turn it is.

        Returns:
            bool: True if it is player 1's turn, False otherwise.
        """

        return self.current_player == self.player1

    def get_green_token_count(self) -> int:
        """
        Gets green token count

        Returns:
            int: Green token count
        """

        return self.player1.get_pieces_left()

    def get_blue_token_count(self) -> int:
        """
        Gets blue token count

        Returns:
            int: Blue token count
        """

        return self.player2.get_pieces_left()

    def get_green_pieces_on_board(self) -> int:
        """
        Gets green token count on board

        Returns:
            int: Green token count on board
        """

        return self.player1.get_pieces_on_board()

    def get_blue_pieces_on_board(self) -> int:
        """
        Gets blue token count on board

        Returns:
            int: Blue token count on board
        """

        return self.player2.get_pieces_on_board()

    def decrement_token_count(self) -> None:
        """
        Decrement current player token count
        """
        self.current_player.decrement_piece_count()

    def increment_token_board(self) -> None:
        """
        Increments current player piece on board
        """
        self.current_player.increment_piece_on_board()

    def decrement_green_board(self) -> None:
        """
        Decrement green piece on board
        """

        return self.player1.decrement_piece_on_board()

    def decrement_blue_board(self) -> None:
        """
        Decrement blue piece on board
        """

        return self.player2.decrement_piece_on_board()

    def get_board(self) -> Board:
        """
        Gets Board instance

        Returns:
            Board: Board instance created by GameManager
        """

        return self._board

    def get_display(self) -> Display:
        """
        Gets Display instance

        Returns:
            Display: Display instance created by GameManager
        """

        return self._display

    def is_current_players_piece(self, position: Position) -> bool:
        """
        Check if current player's piece

        Args:
            position (Position): Position that has been clicked

        Returns:
            bool: If current player's piece, return True, else False
        """
        return position.get_piece().get_is_green() == self.get_is_player1_turn()

    def check_click(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Checking if the mouse click has been clicked on a position

        Args:
            mouse_pos : Mouse position of click by user
        """

        # Checking the position of click and performing action based on this

        for position in self._board.get_positions():
            position_rect: pygame.Rect = position.get_rect()

            if position_rect.collidepoint(
                mouse_pos
            ):  # getting the position you clicked on
                self._action_controller.handle_action(position)

    def set_is_vs_computer(self, is_vs_computer: bool) -> None:
        """
        Sets if playing vs computer

        Args:
            is_vs_computer (bool): New boolean to change to if playing vs computer
        """

        self._is_vs_computer: bool = is_vs_computer

    def get_is_vs_computer(self) -> bool:
        """
        Gets the boolean if it is playing vs computer

        Returns:
            bool: Boolean to see if playing vs computer
        """
        return self._is_vs_computer

    def get_action_controller(self) -> ActionController:
        """
        Gets ActionController instance

        Returns:
            ActionController: ActionController instance created by GameManager
        """

        return self._action_controller

    def get_player1(self) -> Player:
        """
        Gets player 1

        Returns:
            Player: Player 1
        """
        return self.player1

    def get_player2(self) -> Player:
        """
        Gets player 2

        Returns:
            Player: Player 2
        """
        return self.player2

    def get_current_player(self) -> Player:
        """
        Gets current player

        Returns:
            Player: Current player
        """

        return self.current_player

    def get_other_player(self) -> Player:
        """Gets other player

        Returns:
            Player: Player who is not the current player
        """
        return self.player1 if self.current_player == self.player2 else self.player2

    def get_mover_name(self) -> str:
        """
        Gets mover's name

        Returns:
            str: Mover's name
        """

        return self.current_player.get_name()

    def get_move_type(self) -> str:
        """
        Gets move type

        Returns:
            str: Move type
        """

        return self._action_controller.get_move_type()

    def is_ai_turn(self) -> bool:
        """
        Checks if AI' turn

        Returns:
            bool: True if AI's turn, else false
        """
        return self._is_vs_computer and self.get_current_player() == self.get_player2()

    def _render_game(self) -> None:
        """
        Renders the game on the screen.

        This function handles the main game loop and renders the game on the screen.
        It checks for user input events and updates the screen accordingly.
        It also limits the frame rate to 60 FPS using a clock object.
        It uses pygame_widgets to create and update widgets on the screen.
        """

        running = True
        is_game_over = False

        while running:
            clock: Clock = Clock()

            # Poll for events
            # pygame.QUIT event means the user clicked X to close your window
            events: List[Event] = pygame.event.get()
            if pygame.QUIT in [event.type for event in events]:
                running = False
                continue

            if not is_game_over:
                if self.is_ai_turn():
                    ai_player: Computer = self.get_current_player()
                    ai_player.set_move_time()

                    if ai_player.is_time_to_move():
                        self._action_controller.handle_ai_action(
                            self.get_current_player()
                        )

                else:
                    for event in events:
                        if (
                            event.type == pygame.MOUSEBUTTONDOWN
                        ):  # don't respond to clicks if the game is over
                            self.check_click(pygame.mouse.get_pos())

            # check if mills exist
            if self._board.get_mill_manager().get_new_mill():
                self._action_controller.initiate_remove()

            # Fill the screen with a color to wipe away anything from last frame
            self._display.clear_screen()

            self._display.get_token_renderer().render_token_elements(
                self._board.get_mill_manager().get_mills()
            )

            is_game_over: bool = self._game_over_controller.is_game_over()

            pygame_widgets.update(events)
            pygame.display.flip()

            # Limits FPS
            clock.tick(CONSTANTS.FPS)

        pygame.quit()
