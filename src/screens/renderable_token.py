from abc import ABC, abstractmethod

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class RenderableToken(ABC):
    def __init__(self) -> None:
        pass

        @abstractmethod
        def get_x_pos(self):
            pass

        @abstractmethod
        def get_y_pos(self):
            pass

        @abstractmethod
        def get_radius(self):
            pass

        @abstractmethod
        def get_is_green(self):
            pass
