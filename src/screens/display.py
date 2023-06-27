from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import pygame
from pygame import Rect, Surface
from pygame_widgets.button import Button
from screens.outline import Outline

import CONSTANTS
from actions.move_type import MoveType
from screens.sound_controller import SoundController
from screens.token_renderer import TokenRenderer

if TYPE_CHECKING:
    from game_manager import GameManager

from .menu import Menu

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Display:
    def __init__(self, game_manager: GameManager) -> None:
        """
        Initialise display class

        Args:
            game_manager (GameManager): Need to communicate to game_manager when clicking on screen
        """

        pygame.init()
        self._game_manager: GameManager = game_manager
        self._token_renderer: TokenRenderer = TokenRenderer(self, self._game_manager)
        self._screen: Surface = pygame.display.set_mode((1280, 720))
        self._draw_icons()
        self._sound_controller = SoundController(self)

    def get_token_renderer(self) -> TokenRenderer:
        """
        Gets token renderer

        Returns:
            TokenRenderer: Current token renderer
        """
        return self._token_renderer

    def get_screen(self) -> Surface:
        """
        Returns screen attribute

        Returns:
            Surface: the pygame object which elements are rendered on
        """
        return self._screen

    def get_sound_controller(self) -> SoundController:
        """
        Gets sound controller

        Returns:
            SoundController: Current sound controller
        """
        return self._sound_controller

    def _draw_board(self) -> None:
        """
        Draws the board image on the screen.

        This method loads an image from the assets folder and scales it to fit a 400x400 rectangle.
        It then centers the image on the bottom two-thirds of the screen and blits it on the screen surface.
        """

        # Load an image and get its rectangle
        image: Surface = pygame.image.load("./assets/svg/nmm.svg")
        image = pygame.transform.smoothscale(image, (400, 400))
        rect: Rect = image.get_rect()

        screen: Surface = self.get_screen()

        screen_width, screen_height = screen.get_size()
        rect.center = (screen_width // 2, screen_height // 3 * 2)

        screen.blit(image, rect)

    def _draw_icon(
        self,
        image_path: str,
        x: int,
        y: int,
        width: int,
        height: int,
        callback=None,
        colour=CONSTANTS.SCREEN_COLOUR,
    ) -> Button:
        """
        Draws an icon from the image_path parameter

        Args:
            image_path (str): path to the asset (use absolute path from root directory)
            x (int): x positioning of the icon
            y (int): y positioning of the icon
            width (int): width of icon
            height (int): height of icon
            callback (function, optional): a function to run when the button is clicked. Defaults to None.

        Returns:
            Button: A pygame widgets Button object
        """

        image: Surface = self._create_image(image_path, 50)

        button = Button(
            self.get_screen(),
            x,
            y,
            width,
            height,
            image=image,
            onClick=callback,
            inactiveColour=colour,
            hoverColour=colour,
            pressedColour=colour,
        )

        return button

    def create_end_of_game_restart_button(self, callback) -> Button:
        """
        Creates restart button at the end of the game

        Args:
            callback (function): Callback function

        Returns:
            Button: Restart button
        """
        screen_width, screen_height = self.get_screen().get_size()
        return self._draw_icon(
            "./assets/svg/end_of_game_restart.svg",
            screen_width // 2 - 25,
            screen_height // 2 + 25,
            50,
            50,
            callback,
            colour=CONSTANTS.WHITE,
        )

    def _draw_profile(
        self, profile_path: str, is_left_side: bool, is_turn_to_move=False
    ) -> None:
        """
        Draws a profile picture on the screen.

        This function draws a profile picture on the screen, either on the left or right side depending on the isLeftSide argument. It also adds a white border around the picture if it is the turn of the player to move.

        Args:
            profile_path (str): The path to the image file of the profile picture.
            isLeftSide (bool): A flag indicating whether to draw the picture on the left or right side of the screen.
            isTurnToMove (bool, optional): A flag indicating whether it is the turn of the player to move. Defaults to False.
        """

        OFFSET_FROM_EDGE = 150
        PROFILE_HEIGHT = 100
        BORDER_WIDTH = 25

        screen_width, screen_height = self._screen.get_size()

        x_offset: int = (
            OFFSET_FROM_EDGE if is_left_side else screen_width - OFFSET_FROM_EDGE
        )
        rect_center: tuple[int, int] = (x_offset, screen_height // 2)

        if is_turn_to_move:
            # Draw white border around profile picture
            profile_pic_rect = pygame.Rect(
                0, 0, PROFILE_HEIGHT + BORDER_WIDTH, PROFILE_HEIGHT + BORDER_WIDTH
            )
            profile_pic_rect.center = rect_center
            pygame.draw.rect(
                self._screen, (255, 255, 255), profile_pic_rect, 0, border_radius=10
            )

        image: Surface = self._create_image(profile_path, PROFILE_HEIGHT)

        # Center profile images
        rect: Rect = image.get_rect()
        rect.center = rect_center

        screen: Surface = self.get_screen()
        screen.blit(image, rect)

    def _draw_profiles(self) -> None:
        """
        Draws the profile pictures of both players on the screen.

        This function draws the profile pictures of both players on the screen, one on the left and one on the right. It also adds a white border around the picture of the player whose turn it is to move. It uses the _draw_profile method to draw each picture.
        """

        is_left = True
        is_player1_turn: bool = self._game_manager.get_is_player1_turn()
        if self._game_manager.get_is_vs_computer():
            player2_profile_pic = "./assets/images/profiles/robot.png"
        else:
            player2_profile_pic = "./assets/images/profiles/player2.png"

        self._draw_profile(
            "./assets/images/profiles/player1.png", is_left, is_player1_turn
        )
        self._draw_profile(player2_profile_pic, not is_left, not is_player1_turn)

        screen_width, screen_height = self._screen.get_size()
        OFFSET_FROM_EDGE = 150
        PROFILE_HEIGHT = 100
        font = pygame.font.Font("./assets/fonts/Acme-Regular.ttf", 16)

        self._draw_text(
            self._game_manager.get_player1().get_name(),
            (255, 255, 255),
            OFFSET_FROM_EDGE,
            screen_height // 2 + PROFILE_HEIGHT / 2 + 35,
            font,
        )
        self._draw_text(
            self._game_manager.get_player2().get_name(),
            (255, 255, 255),
            screen_width - OFFSET_FROM_EDGE,
            screen_height // 2 + PROFILE_HEIGHT / 2 + 35,
            font,
        )

    def _draw_turn_indicator(self, player_name: str, move_type: MoveType) -> None:
        """
        Draws a turn indicator on the screen.

        This function draws a turn indicator on the screen, which shows which player's turn it is to move. It draws a white rectangle with rounded corners and a text that says "PLAYER 1 TO MOVE" or "PLAYER 2 TO MOVE" depending on the player_1_to_move argument. It also draws a token of the corresponding color inside the rectangle. It uses the _draw_text and _draw_token methods to draw the text and the token.

        Args:
            green_to_move (bool, optional): A flag indicating whether it is player 1's turn to move or not. Defaults to True.
        """
        outline = None
        screen_width, screen_height = self.get_screen().get_size()
        green_to_move: bool = self._game_manager.get_is_player1_turn()
        INDICATOR_HEIGHT = 120
        INDICATOR_WIDTH = 400
        INDICATOR_Y = 120
        INDICATOR_X: float = screen_width / 2

        TOKEN_RADIUS = 35
        TOKEN_Y = INDICATOR_Y + 12
        TOKEN_X: float = INDICATOR_X

        # Draw white square
        rect = pygame.Rect(0, 0, INDICATOR_WIDTH, INDICATOR_HEIGHT)
        rect.center = (INDICATOR_X, INDICATOR_Y)
        pygame.draw.rect(self._screen, (238, 238, 249), rect, border_radius=10)

        font = pygame.font.Font("./assets/fonts/Roboto-Regular.ttf", 16)
        self._draw_text(
            f"{player_name} TO {move_type.value.upper()}",
            (0, 0, 0),
            INDICATOR_X,
            INDICATOR_Y - INDICATOR_HEIGHT / 2 + 15,
            font,
        )

        if move_type == MoveType.REMOVE:
            outline = Outline.RED
            green_to_move = not green_to_move

        self.draw_token(TOKEN_X, TOKEN_Y, TOKEN_RADIUS, green_to_move)

        if move_type == MoveType.REMOVE:
            self.draw_outline(TOKEN_X, TOKEN_Y, TOKEN_RADIUS, outline)

    def draw_line(self, outline: MoveType, start_pos: tuple, end_pos: tuple):
        LINE_THICKNESS = 10
        pygame.draw.line(
            self._screen, outline.value, start_pos, end_pos, width=LINE_THICKNESS
        )

    def _draw_text(
        self,
        text: str,
        colour: Tuple[int, int, int],
        x: int,
        y: int,
        font: pygame.font.Font,
    ):
        """
        Draws a text on the screen.

        This function draws a text on the screen with a given colour, font and position. It uses the pygame.font module to render the text and blit it on the screen.

        Args:
            text (str): The text to be drawn on the screen.
            colour (tuple[int, int, int]): The RGB colour of the text.
            x (int): The x coordinate of the center of the text.
            y (int): The y coordinate of the center of the text.
            font (pygame.font.Font): The font object of the text.
        """

        # Create a text surface object, on which text is drawn on it.
        text_surface = font.render(text, True, colour)

        # Create a rectangular object for the text surface object
        text_rect = text_surface.get_rect()

        # Set the center of the rectangular object.
        text_rect.center = (x, y)
        self._screen.blit(text_surface, text_rect)

    def draw_token(self, x: int, y: int, radius: int, is_green: bool) -> None:
        """
        Draws a token on the screen.

        This function draws a token on the screen with a given colour, position and radius. It uses the pygame.draw module to draw a circle on the screen.

        Args:
            x (int): The x coordinate of the center of the circle.
            y (int): The y coordinate of the center of the circle.
            radius (int): The radius of the circle.
            is_green (bool): A flag indicating whether the token is green or blue.
            outline (str): The colour of the outline of the circle. Defaults to None.
        """

        pygame.draw.circle(
            self._screen,
            CONSTANTS.WHITE_TOKEN_COLOUR if is_green else CONSTANTS.BLACK_TOKEN_COLOUR,
            (x, y),
            radius,
        )

    def draw_outline(self, x, y, radius, outline):
        pygame.draw.circle(
            self._screen, outline.value, (x, y), radius, width=int(radius / 2.75)
        )

    def _create_image(self, image_path: str, size: int) -> Surface:
        """
        Creates an image surface from a file.

        This function creates an image surface from a file given by the image_path argument. It also resizes the image to the given size using the pygame.transform.smoothscale method.

        Args:
            image_path (str): The path to the image file.
            size (int): The desired size of the image surface in pixels.

        Returns:
            Surface: A pygame.Surface object that represents the image.
        """

        image: Surface = pygame.image.load(image_path)
        image = pygame.transform.smoothscale(image, (size, size))
        return image

    def draw_screen(self) -> None:
        """
        Drawing screen
        """

        self._draw_board()
        self._draw_token_counters(
            self._game_manager.get_green_token_count(),
            self._game_manager.get_blue_token_count(),
        )
        self._draw_profiles()
        self._draw_turn_indicator(
            self._game_manager.get_mover_name(), self._game_manager.get_move_type()
        )

    def _draw_icons(self):
        self._draw_icon("./assets/svg/home.svg", 75, 50, 50, 50, self.go_to_menu)
        self._draw_icon(
            "./assets/svg/restart.svg",
            1200,
            50,
            50,
            50,
            self._game_manager.initialise_game,
        )

    def clear_screen(self):
        """
        Clears screen
        """
        self.get_screen().fill(CONSTANTS.SCREEN_COLOUR)
        self.draw_screen()

    def _toggle_mute(self):
        """
        Toggle mute
        """
        self._sound_controller.toggle_mute()

    def _draw_token_counters(self, green_count: int, blue_count: int):
        """
        Draws the token counters for the green and blue players on the screen.

        Args:
            green_count (int): The number of tokens left for the green player.
            blue_count (int): The number of tokens left for the blue player.
        """

        screen_width, screen_height = self.get_screen().get_size()

        TOKEN_HEIGHT = 550
        TOKEN_RADIUS = 25
        TOKEN_OFFSET = 150
        self.draw_token(TOKEN_OFFSET, TOKEN_HEIGHT, TOKEN_RADIUS, True)
        self.draw_token(screen_width - TOKEN_OFFSET, TOKEN_HEIGHT, TOKEN_RADIUS, False)

        font = pygame.font.Font("./assets/fonts/Acme-Regular.ttf", 16)
        self._draw_text(
            f"{green_count} remaining",
            (255, 255, 255),
            TOKEN_OFFSET,
            TOKEN_HEIGHT + TOKEN_RADIUS + 25,
            font,
        )
        self._draw_text(
            f"{blue_count} remaining",
            (255, 255, 255),
            screen_width - TOKEN_OFFSET,
            TOKEN_HEIGHT + TOKEN_RADIUS + 25,
            font,
        )

    def draw_winner_dialogue(self, winner: str) -> None:
        """
        Draws winner dialogue

        Args:
            winner (str): Winner name
        """
        screen_width, screen_height = self.get_screen().get_size()
        rect = pygame.Rect(0, 0, 500, 250)
        rect.center = (screen_width // 2, screen_height // 2)
        pygame.draw.rect(self._screen, CONSTANTS.WHITE, rect, border_radius=10)

        font = pygame.font.Font("./assets/fonts/Roboto-Regular.ttf", 60)
        self._draw_text(
            f"{winner} wins!",
            CONSTANTS.BLACK,
            screen_width // 2,
            screen_height // 2 - 50,
            font,
        )

    def go_to_menu(self) -> None:
        """
        Creates a menu and renders it.

        The result of create menu tells whether it is vs a computer or a human, it is stored in the _is_vs_computer variable.

        The _render_game function is then called to start the game.
        """

        menu = Menu(self)
        is_vs_computer: bool = menu.create_menu()
        self._game_manager.set_is_vs_computer(is_vs_computer)
        self._game_manager.initialise_game()
