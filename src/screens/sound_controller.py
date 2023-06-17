from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame_widgets.button import Button

if TYPE_CHECKING:
    from screens.display import Display

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class SoundController:
    def __init__(self, display: Display) -> None:
        """
        Initialises sound controller class

        Args:
            display (Display): Current display
        """
        self._muted: bool = False
        self._display: Display = display
        self._volume_button: Button = self._display._draw_icon(
            self._get_image_path(),
            1100,
            50,
            50,
            50,
            self.toggle_mute,
        )

    def set_volume_button(self, volume_button: Button) -> None:
        """
        Set volume button

        Args:
            volume_button (Button): new volume button
        """
        self._volume_button = volume_button

    def toggle_mute(self) -> None:
        """
        Toggle mute
        """
        self._muted: bool = not self._muted
        image: Surface = self._display._create_image(self._get_image_path(), 50)
        self._volume_button.setImage(image)

        pygame.mixer.music.stop()

    def _get_image_path(self) -> str:
        """
        Gets image path

        Returns:
            Image path
        """
        return "./assets/svg/mute.svg" if self._muted else "./assets/svg/unmuted.svg"

    def play_winner_sound(self):
        """
        Plays winner sound
        """
        image_paths = [
            "./assets/sounds/cheer1.wav",
            "./assets/sounds/cheer2.wav",
            "./assets/sounds/flute.wav",
        ]
        self.play_from_list(image_paths)

    def place_piece_sound(self) -> None:
        """
        Plays place piece sound
        """
        image_paths = ["./assets/sounds/dice_roll.mp3"]
        self.play_from_list(image_paths)

    def play_start_game_sound(self) -> None:
        """
        Plays start game sound
        """
        self.play_from_list(["./assets/sounds/heres_the_moves_it_starts_with.mp3"])

    def piece_move_sound(self) -> None:
        """
        Plays move piece sound
        """
        self.play_from_list(
            [
                "./assets/sounds/slide_the_queen_and_bait_it.mp3",
                "./assets/sounds/resign_now.mp3",
                "./assets/sounds/big_mistake.mp3",
                "./assets/sounds/you_cant_save_it.mp3",
            ]
        )

    def remove_piece_sound(self) -> None:
        """
        Plays remove piece sound
        """
        self.play_from_list(["./assets/sounds/blunder.mp3"])

    def play_from_list(self, image_paths) -> None:
        """
        Plays from list

        Args:
            Image paths
        """
        if self._muted:
            return

        pygame.mixer.music.load(image_paths[random.randint(0, len(image_paths) - 1)])
        pygame.mixer.music.play()
