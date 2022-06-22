from constants import *
import pyray
from game.casting.actor import Actor
from game.shared.color import Color
from game.shared.point import Point


class Banner(Actor):
    """
    Banner adds a background box to make messages more readable. TO turn it off, set it's 
    alpha to 0 (transparent.)

    Attributes:
        _bkg_color (Color): The points earned in the game.
    """
    def __init__(self, text="", bkg_color = Color(0,0,0,0), font_size = 15, padding = 3):
        super().__init__()
        self._width = 0
        self._height = 0
        self._bkg_color = bkg_color
        self._padding = padding
        self._font_size = font_size
        self.set_text(text)
        

    def set_bkg_color(self, color):
        """Sets the background box to a given color.
        
        Args:
            color (Color): The color to set.
        """
        self._bkg_color = color


    def get_bkg_color(self):
        """This returns the value of the background color.
        
        Returns:
            (Color)
        """
        return self._bkg_color


    def set_padding(self, padding):
        """Sets the background box to a given color.
        
        Args:
            padding (int): The number of pixels of padding to add to all four sides of the box.
        """
        self._padding = padding
        self._recalculate_size()
    
    def get_padding(self):
        return self._padding

    def get_width(self):
        """Return the overall width of the background box in pixels.
        """
        return self._width

    def get_height(self):
        """Return the overall height of the background box in pixels.
        """
        return self._height

    # Polymorph these from the Actor class

    def set_text(self, text):
        """Updates the text to the given value. After that we need to recalculate the background size.
        
        Args:
            text (string): The given value.
        """
        self._text = text
        self._recalculate_size()


    def set_font_size(self, font_size):
        """Updates the font size to the given one. After that we need to recalculate the background size.
        
        Args:
            font_size (int): The given font size.
        """
        self._font_size = font_size
        self._recalculate_size()


    def screen_center(self):
        """Will use the MAX_X and MAX_Y constants to position this banner
        in the middle of the screen.
        """
        x = int(MAX_X / 2)
        y = int((MAX_Y / 2) - (self._height / 2))
        self.set_position(Point(x, y))


    ############

    def _recalculate_size(self):
        """When text or font size or padding values change, recalculate so that we have proper background.
        """
        lines = self._text.count("\n") + 1
        self._height = (self._font_size + 5) * lines + ( self._padding * 2 )
        self._width = pyray.measure_text(self._text, self._font_size) + (self._padding * 2)
    

