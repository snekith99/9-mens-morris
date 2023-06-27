import CONSTANTS
from screens.renderable_token import RenderableToken

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class AnimatedPiece(RenderableToken):
    def __init__(
        self,
        start_x,
        start_y,
        end_x,
        end_y,
        start_radius,
        end_radius,
        destination_piece_index: int,
        is_green: bool,
        duration,
    ) -> None:
        """
        Initialises animated piece class

        Args:
            start_x (): Start X
            start_y (): Start Y
            end_x (): End X
            end_y (): End Y
            start_radius (): Start Radius
            end_radius (): End radius
            destination_piece_index (int): Destination piece index
            is_green (bool): True if green
            duration (): Duration
        """
        # animation attributes
        self._start_position: list[int, int] = (start_x, start_y)
        self._current_position: list[int, int] = [start_x, start_y]
        self._end_position: list[int, int] = (end_x, end_y)

        self._start_radius = start_radius
        self._current_radius = start_radius
        self._end_radius = end_radius

        self._destination_piece_index: int = destination_piece_index
        self._is_green = is_green

        self._duration = duration

        self._frames_passed = 0

    def tick(self) -> None:
        """
        Updates the animation
        """
        self._frames_passed += 1
        progress = self.get_progress()

        location_difference_x = self._end_position[0] - self._start_position[0]
        location_difference_y = self._end_position[1] - self._start_position[1]
        radius_difference = self._end_radius - self._start_radius

        self._current_position[0] = (
            self.ease_out_bounce(progress) * location_difference_x
            + self._start_position[0]
        )
        self._current_position[1] = (
            self.ease_out_bounce(progress) * location_difference_y
            + self._start_position[1]
        )

        self._current_radius = (
            self.ease_out_bounce(progress) * radius_difference + self._start_radius
        )

        if progress >= 1:
            return True

        return False

    def ease_out_bounce(self, x: float) -> float:
        """
        Ease out bounce

        Args:
            x (float): x

        Returns:
            float: True if complete
        """
        n1 = 7.5625
        d1 = 2.75

        res = 0

        if x < 1 / d1:
            res = n1 * x * x
        elif x < 2 / d1:
            x -= 1.5 / d1
            res = n1 * x * x + 0.75
        elif x < 2.5 / d1:
            x -= 2.25 / d1
            res = n1 * x * x + 0.9375
        else:
            x -= 2.625 / d1
            res = n1 * x * x + 0.984375
        return res

    def get_destination_piece_index(self) -> int:
        """
        Gets destination piece index

        Returns:
            int: Destination piece index
        """
        return self._destination_piece_index

    def get_x_pos(self) -> int:
        """
        Gets x position

        Returns:
            int: x position
        """
        return self._current_position[0]

    def get_y_pos(self) -> int:
        """
        Gets y position

        Returns:
            int: y position
        """
        return self._current_position[1]

    def get_radius(self) -> float:
        """
        Gets radius

        Returns:
            int: radius
        """
        return self._current_radius

    def get_is_green(self) -> bool:
        """
        Checks if green

        Returns:
            bool: True if green
        """
        return self._is_green

    def get_progress(self) -> int:
        """
        Gets progress

        Returns:
            int: Progress
        """
        return min(self._frames_passed / (self._duration * CONSTANTS.FPS), 1)
