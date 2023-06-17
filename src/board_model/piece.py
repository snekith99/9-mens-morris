__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Piece:
    def __init__(self, is_green: bool) -> None:
        """
        Initialising Piece class

        Args:
            is_green (bool): Check if piece is green (player 1)
        """
        self._is_green: bool = is_green

    def get_is_green(self) -> bool:
        """
        Gets boolean if green

        Returns:
            bool: true if green, else false
        """
        return self._is_green
