import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Cycle(Actor):
    """
    An old-school light-cycle that leaves a solid beam of light as it's trail.
    
    The responsibility of Cycle is to move itself.

    Attributes:
        _player_number (int): Identifies which player the cycle instance belongs to.
        _segments (list[Actor]): The list of Actors representing trailing segments that make the light-wall for this cycle.
        _color (Color): The color that the light wall should be rendered.
        _wall_active (bool): Whether or not new wall segments are being drawn from this cycle.
    
        All other attributes inherited from Actor.
    """
    def __init__(self, color, player_number=0):
        super().__init__()
        self._segments = []
        self._player_number = player_number
        self._color = color
        self._wall_active = True
        self._prepare_cycle()

    def get_segments(self):
        """Returns the list of segments that make up the entirety of the cycle and its 
        light wall.

        Returns: list[Actor]
        """
        return self._segments

    def move_next(self):
        """Moves all segments according to their velocities, updates all segments
        to grab new velocity of the member in front of it to make them follow
        each other.
        """
        for segment in self._segments:
            segment.move_next()
        # update velocities
        for i in range(len(self._segments) - 1, 0, -1):
            trailing = self._segments[i]
            previous = self._segments[i - 1]
            velocity = previous.get_velocity()
            trailing.set_velocity(velocity)

    def get_head(self):
        """Returns the first element in the _segments list, which is the 'cycle' (head segment).
        
        Returns: Actor
        """
        return self._segments[0]

    def grow_tail(self, number_of_segments):
        """Increases the list of segments by the number specified to make the light-wall longer,
        but only if _wall_active == True.
        
        Args:
            number_of_segments (int): The number of segments to add to the list.
        """
        if self._wall_active:
            for i in range(number_of_segments):
                tail = self._segments[-1]
                velocity = tail.get_velocity()
                offset = velocity.reverse()
                position = tail.get_position().add(offset)
                
                segment = Actor()
                segment.set_position(position)
                segment.set_velocity(velocity)
                segment.set_text(constants.TAIL_SHAPES[self._player_number])
                segment.set_color(self._color)
                self._segments.append(segment)

    def start_wall(self):
        """Sets the growing of the tail wall to be active.
        """
        self._wall_active = True


    def stop_wall(self):
        """Sets the growing of the tail wall to be inactive.
        """
        self._wall_active = False


    def turn_head(self, velocity):
        """Turns the 'head' of the light cycle to match a given velocity.

        Args:
            velocity (Point): A user-provided velocity in terms of (Vx, Vy). 
        """
        self._segments[0].set_velocity(velocity)
    
    def _prepare_cycle(self):
        """Prepares a light cycle based on the instance's assigned player number.
        """
        text = constants.CYCLE_SHAPE
        
        for i in range(constants.CYCLE_LENGTH):
            if self._player_number == 1:
                x = int(constants.CELL_SIZE * 15)
                y = int(constants.CELL_SIZE * 10)
                position = Point(x - (i * constants.CELL_SIZE), y)
                velocity = Point(1 * constants.CELL_SIZE, 0)
            else:
                x = int(constants.CELL_SIZE * 45)
                y = int(constants.CELL_SIZE * 30)
                position = Point(x + (i * constants.CELL_SIZE), y)
                velocity = Point(-1 * constants.CELL_SIZE, 0)
            
            # Makes the head or lead segment yellow, to stand out.
            color = constants.YELLOW
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text(text)
            segment.set_color(color)
            self._segments.append(segment)
        
        

        