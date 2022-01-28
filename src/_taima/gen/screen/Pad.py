import curses
from _taima.gen.screen.Color import Color as c

class Pad(object):
    """
    Pseudo wrapper class for the tassk window object.
    """
    # This class is used to wrap curses pads and allow for own pad objects that
    # inherit from this class. This makes managing the pads in the children
    # classes easier with specific function definitions.

    def __init__(self, height: int, width: int):
        self._pad:        object = curses.newpad(height, width)
        self._pad_height: int = height
        self._pad_width:  int = width
        self._pad.nodelay(0)
        
        # colors
        self.DEF_BG:     object = curses.color_pair(c.DEF_BG.value)
        self.DEF_WHITE:  object = curses.color_pair(c.DEF_WHITE.value)
        self.DEF_PURPLE: object = curses.color_pair(c.DEF_PURPLE.value)
        self.DEF_YELLOW: object = curses.color_pair(c.DEF_YELLOW.value)
        self.DEF_GREEN:  object = curses.color_pair(c.DEF_GREEN.value)
        self.DEF_RED:    object = curses.color_pair(c.DEF_RED.value)

        
        self.DEF_PURP__: object = curses.color_pair(c.DEF_PURP__.value)
        self.DEF_PURP_0: object = curses.color_pair(c.DEF_PURP_0.value)
        self.DEF_PURP_1: object = curses.color_pair(c.DEF_PURP_1.value)
        self.DEF_PURP_2: object = curses.color_pair(c.DEF_PURP_2.value)
        self.DEF_PURP_3: object = curses.color_pair(c.DEF_PURP_3.value)
        self.DEF_PURP_4: object = curses.color_pair(c.DEF_PURP_4.value)
        self.DEF_PURP_5: object = curses.color_pair(c.DEF_PURP_5.value)
        self.DEF_PURP_6: object = curses.color_pair(c.DEF_PURP_6.value)
        self.DEF_PURP_7: object = curses.color_pair(c.DEF_PURP_7.value)

        self.W_BG:     object = curses.color_pair(c.W_BG.value)
        self.W_PURPLE: object = curses.color_pair(c.W_PURPLE.value)
        self.W_BLACK:  object = curses.color_pair(c.W_BLACK.value)
        self.W_YELLOW: object = curses.color_pair(c.W_YELLOW.value)
        self.W_RED:    object = curses.color_pair(c.W_RED.value)
        self.W_GREEN:  object = curses.color_pair(c.W_GREEN.value)

        self.W_PURP_1: object = curses.color_pair(c.W_PURP_1.value)
        self.W_PURP_2: object = curses.color_pair(c.W_PURP_2.value)
        self.W_PURP_3: object = curses.color_pair(c.W_PURP_3.value)
        self.W_PURP_4: object = curses.color_pair(c.W_PURP_4.value)
        self.W_PURP_5: object = curses.color_pair(c.W_PURP_5.value)
        self.W_PURP_6: object = curses.color_pair(c.W_PURP_6.value)
        self.W_PURP_7: object = curses.color_pair(c.W_PURP_7.value)

        self.GRAY1: object = curses.color_pair(c.W_GRAY_1.value)
        self.GRAY2: object = curses.color_pair(c.W_GRAY_2.value)
        self.GRAY3: object = curses.color_pair(c.W_GRAY_3.value)

        self.BOLD:   object = curses.A_BOLD
        self.BLINK:  object = curses.A_BLINK
        self.NORMAL: object = curses.A_NORMAL
    
    # wrapper methods, acting like their curses pendant.

    def addstr(self, y: int, x: int, string: str, color: int) -> None:
        self._pad.addstr(y, x, string, curses.color_pair(color))

    def erase(self) -> None:
        self._pad.erase()

    def refresh(self, pminrow: int, pmincol: int, sminrow: int, smincol: int, smaxrow: int, smaxcol: int) -> None:
        self._pad.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
    
    def noutrefresh(self, pminrow: int, pmincol: int, sminrow: int, smincol: int, smaxrow: int, smaxcol: int) -> None:
        self._pad.noutrefresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
