from actions.fly_action import FlyAction
from actions.move_action import MoveAction
from actions.place_action import PlaceAction
from actions.remove_action import RemoveAction
from board_model.position import Position
from players.player import Player

__author__ = "Snekith, Patrick and Ashwin"
__date__ = "17/06/2023"


class Human(Player):
    def create_place_action(self, position: Position) -> bool:
        """
        Human creating a place action

        Args:
            position (Position): Position to add the piece

        Returns:
            bool: True if completed successfully
        """
        place_action = PlaceAction(position, self.game_manager)
        return place_action.execute()

    def create_move_action(self, origin: Position, destination: Position) -> bool:
        """
        Human creating a move action

        Args:
            origin (Position): Source position
            destination (Position): Position to move the piece

        Returns:
            bool: True if completed successfully
        """
        move_action = MoveAction(origin, destination, self.game_manager)
        return move_action.execute()

    def create_remove_action(self, position: Position) -> bool:
        """
        Human creating a remove action

        Args:
            position (Position): Piece to be removed at position

        Returns:
            bool: True if completed successfully
        """
        remove_action = RemoveAction(position, self.game_manager)
        return remove_action.execute()

    def create_fly_action(self, origin: Position, destination: Position) -> bool:
        """
        Human creating a fly action

        Args:
            origin (Position): Source position
            destination (Position): Position to fly the piece

        Returns:
            bool: True if completed successfully
        """
        fly_action = FlyAction(origin, destination, self.game_manager)
        return fly_action.execute()
