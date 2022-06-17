import constants
from game.scripting.action import Action
from game.shared.point import Point


class ControlActorsAction(Action):
    """
    An input action that controls the cycle.
    
    The responsibility of ControlActorsAction is to get the direction and move the cycle's head.

    Attributes:
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service):
        """Constructs a new ControlActorsAction using the specified KeyboardService.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
        """
        self._keyboard_service = keyboard_service
        # self._direction1 = Point(constants.CELL_SIZE, 0)
        # self._direction2 = Point(constants.CELL_SIZE, 0)

    def execute(self, cast, script):
        """Executes the control actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        cycle1 = cast.get_actors("cycles")[0]
        cycle2 = cast.get_actors("cycles")[1]

        current_dir1 = cycle1.get_segments()[0].get_velocity()
        current_dir2 = cycle2.get_segments()[0].get_velocity()

        # left
        if self._keyboard_service.is_key_down('a'):
            current_dir1 = Point(-constants.CELL_SIZE, 0)
        
        # right
        if self._keyboard_service.is_key_down('d'):
            current_dir1 = Point(constants.CELL_SIZE, 0)
        
        # up
        if self._keyboard_service.is_key_down('w'):
            current_dir1 = Point(0, -constants.CELL_SIZE)
        
        # down
        if self._keyboard_service.is_key_down('s'):
            current_dir1 = Point(0, constants.CELL_SIZE)
        
        cycle1.turn_head(current_dir1)

        # left
        if self._keyboard_service.is_key_down('j'):
            current_dir2 = Point(-constants.CELL_SIZE, 0)
        
        # right
        if self._keyboard_service.is_key_down('l'):
            current_dir2 = Point(constants.CELL_SIZE, 0)
        
        # up
        if self._keyboard_service.is_key_down('i'):
            current_dir2 = Point(0, -constants.CELL_SIZE)
        
        # down
        if self._keyboard_service.is_key_down('k'):
            current_dir2 = Point(0, constants.CELL_SIZE)
        
        cycle2.turn_head(current_dir2)