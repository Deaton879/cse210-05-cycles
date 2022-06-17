from game.scripting.action import Action


class DrawActorsAction(Action):
    """
    An output action that draws all the actors.
    
    The responsibility of DrawActorsAction is to draw all the actors.

    Attributes:
        _video_service (VideoService): An instance of VideoService.
    """

    def __init__(self, video_service):
        """Constructs a new DrawActorsAction using the specified VideoService.
        
        Args:
            video_service (VideoService): An instance of VideoService.
        """
        self._video_service = video_service

    def execute(self, cast, script):
        """Executes the draw actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        score = cast.get_first_actor("scores")
        cycles = cast.get_actors("cycles")
        
        banners = cast.get_actors("banners")

        self._video_service.clear_buffer()
        for cycle in cycles:
            segments = cycle.get_segments()
            self._video_service.draw_actors(segments)

        # Banners are last to have topmost priority
        # over all other items.
        self._video_service.draw_banners(banners, True)
        self._video_service.flush_buffer()