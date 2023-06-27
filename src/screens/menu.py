from __future__ import annotations
from typing import TYPE_CHECKING, Callable

import pygame
import pygame_menu
from pygame_menu import BaseImage

if TYPE_CHECKING:
    from .display import Display

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Menu:
    def __init__(self, display: Display) -> None:
        """
        Initialise Menu Class with display attribute

        Args:
            display (Display): Display object to display menu
        """

        self._display: Display = display
        self._menu_active = True
        self._is_vs_computer = False

    def create_menu(self) -> bool:
        """
        Creates a menu for the game.

        This function creates a menu object using pygame_menu module. It sets the theme, size and title of the menu using the given parameters.

        Returns:
            bool: True if the vs computer menu item is clicked, False otherwise.
        """

        theme = pygame_menu.Theme(
            background_color=self._create_image(
                "./assets/images/backgrounds/menu_background.png"
            ),
            title=False,
            widget_font=pygame_menu.font.FONT_FIRACODE,
            widget_font_color=(255, 255, 255),
            widget_margin=(0, 15),
            widget_selection_effect=pygame_menu.widgets.NoneSelection(),
        )

        window_width, window_height = self._display.get_screen().get_size()
        self._menu = pygame_menu.Menu(
            height=window_height,
            width=window_width,
            mouse_motion_selection=True,
            theme=theme,
            title="",
        )

        self._draw_menu_buttons()
        while self._menu_active:
            self._menu.update(pygame.event.get())
            self._menu.draw(self._display.get_screen())
            pygame.display.update()

        return self._is_vs_computer

    def _create_button(
        self, image_url: str, callback: Callable[[], None], *args
    ) -> None:
        """
        Creates a button widget with an image and a callback function.

            Args:
                image_url (str): The URL of the image to be used as the button icon.
                callback (Callable[[], None]): The function to be executed when the button is clicked.
        """

        button_image: pygame_menu.BaseImage = self._create_image(image_url)
        rect: pygame.Rect = button_image.get_rect()

        button: pygame_menu.widgets.Button = self._menu.add.button(
            " ",
            callback,
            *args,
        )

        button.resize(rect.width, rect.height)
        button.translate(0, 50)
        button.set_margin(0, 25)

        button.get_decorator().add_baseimage(
            -rect.width / 2, -rect.height / 2, button_image
        )

    def _create_image(self, image_path: str) -> BaseImage:
        """
        Creates a BaseImage object from an image path.

            Args:
                image_path (str): The path to the image file.

            Returns:
                BaseImage: A BaseImage object that can be used as a background or a decoration for widgets.
        """

        return pygame_menu.baseimage.BaseImage(
            image_path=image_path,
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        )

    def _draw_menu_buttons(self) -> None:
        """
        Draws the menu buttons for choosing the game mode and quitting the game.

        The buttons are created using the _create_button method and have different images and callback functions.
        """

        # vs human
        self._create_button(
            "./assets/images/buttons/human.png", self._handle_vs_human_button
        )
        # vs computer
        self._create_button(
            "./assets/images/buttons/computer.png", self._handle_vs_computer_button
        )

        self._create_button("./assets/images/buttons/quit.png", pygame_menu.events.EXIT)

    def _handle_vs_computer_button(self) -> None:
        """
        Closes menu and sets vs computer flag to true
        """
        self._menu_active = False
        self._is_vs_computer = True

    def _handle_vs_human_button(self) -> None:
        """
        Closes menu and sets vs computer to false
        """

        self._menu_active = False
        self._is_vs_computer = False
