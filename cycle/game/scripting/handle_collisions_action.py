import constants
from game.casting.banner import Banner
from game.scripting.action import Action
from game.shared.point import Point
from game.shared.color import Color

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the cycle collides
    with the food, or the cycle collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._winner = ""
        self._winning_color = constants.GREY_80PCT

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_item_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_item_collision(self, cast):
        """Unused right now, but could allow for possibility of picking up bonuses,
        power-ups, other obstacles, etc...?
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # score = cast.get_first_actor("scores")
        # cycle = cast.get_first_actor("cycles")
        # head = cycle.get_head()

        # if head.get_position().equals(food.get_position()):
        #     points = food.get_points()
        #     cycle.grow_tail(points)
        #     score.add_points(points)
        #     food.reset()
        pass

    def _check_collision(self, head, seg1, seg2):
        """Check if a head has collided either one segment or another.
        
        Returns: (boolean) True is collision occurred.
        """
        return head.get_position().equals(seg1.get_position()) or head.get_position().equals(seg2.get_position())

    def _set_winner(self, player_num = 0):
        """Sets the winner to the appropriate player:
            1 : Player 1
            2 : Player 2
            All other numbers = Nobody.
            
        Args:
            player_num (int): Either 1, or 2 depending on who won.
        """
        if player_num == 1:
            self._winner = "Player 1"
            self._winning_color = constants.GREEN_80PCT
        elif player_num == 2:
            self._winner = "Player 2"
            self._winning_color = constants.RED_80PCT
        else:
            self._winner = "Nobody"
            self._winning_color = constants.GREY_80PCT


    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the cycle collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycles = cast.get_actors("cycles")
        
        head1 = cycles[0].get_segments()[0]
        head2 = cycles[1].get_segments()[0]

        segments1 = cycles[0].get_segments()[1:]
        segments2 = cycles[1].get_segments()[1:]

        for seg1, seg2 in zip(segments1, segments2):
            if self._check_collision(head1, seg1, seg2):
                self._is_game_over = True
                self._set_winner(2)

            if self._check_collision(head2, seg1, seg2):
                self._is_game_over = True
                # Check if both players triggered collision within the exact same frame...
                if self._winner == "":
                    self._set_winner(1)
                else:
                    self._set_winner(0)

          
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the cycle and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycles = cast.get_actors("cycles")
            bkg_color = self._winning_color
            message = Banner()
            message.set_padding(15)
            message.set_bkg_color(bkg_color)
            line1 = "Game Over".center(21)
            line2 = f"{self._winner} Wins!".center(21)
            message.set_text(f"{line1}\n{line2}")
            message.set_font_size(40)

            x = int(constants.MAX_X / 2)
            h = message.get_font_size() + 2 * message.get_padding()
            y = int((constants.MAX_Y / 2) - (h / 2))
            position = Point(x, y)
            message.set_position(position)

            cast.add_actor("banners", message)

            for cycle in cycles:
                cycle.set_color(constants.WHITE)
                cycle.stop_wall()
                segments = cycle.get_segments()

                for segment in segments:
                    segment.set_color(constants.WHITE)