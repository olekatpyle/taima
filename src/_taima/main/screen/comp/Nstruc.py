import curses
from _taima.gen.screen.Pad import Pad
from _taima.gen.screen.Color import Color as c

#------------------------------------------------------------------------------
# INSTRUCTION PAD
#
# The wrapper class for the instruction pad. On initialization, the pad
# is populated with every instruction set. In order to toggle between the
# sets, every set has a display method.


class Nstruc(Pad):
    """
    Pseudo wrapper class for the instruction window. A pad is being used
    underneath, in order to only draw the instruction sets once, afterwards
    just toggle between the different sets instead of redrawing them every
    time.
    The pad has the following structure:

                             curses.COLS - 1
    |------------------------------------------------------------|
   
    *------------------------------------------------------------*
    | SET 1                                                      |
    *------------------------------------------------------------*
    | SET 2                                                      |
    *------------------------------------------------------------*
    | SET 3                                                      |

    """
    
    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self._pad.bkgd(' ', curses.color_pair(c.W_BG.value))
        self._pad.nodelay(0)

        self.__populate_pad() 
        self.display_empty()

    
    # method, to write every used instruction set to the pad.
    
    def __populate_pad(self) -> None:
        W_BLACK: object = curses.color_pair(c.W_BLACK.value)

        q:            str = '[q] quit'
        q_to_menu:    str = '[q] back to menu'
        space_start:  str = '[SPACE] start timer'
        space_pause:  str = '[SPACE] pause timer'
        space_resume: str = '[SPACE] resume timer'
        enter_new:    str = '[e] enter new task'

        #main
        y: int = 1
        x: int = 0
        
        self._pad.addstr(y, x, q, W_BLACK)
        
        x += len(q) + 4
        self._pad.addstr(y, x, space_start, W_BLACK)

        x += len(space_start) + 4
        self._pad.addstr(y, x, enter_new, W_BLACK)

        #in running session
        y = 2
        x = 0
        self._pad.addstr(y, x, space_pause, W_BLACK)

        #in paused session first time
        y = 3
        x = 0
        self._pad.addstr(y, x, q_to_menu, W_BLACK)

        x += len(q_to_menu) + 4
        self._pad.addstr(y, x, space_start, W_BLACK)

        #in paused session
        y = 4
        x = 0
        self._pad.addstr(y , x, q_to_menu, W_BLACK)

        x += len(q_to_menu) + 4
        self._pad.addstr(y, x, space_resume, W_BLACK)

    # display functions, wrapping the pad refreshes to simplify usage in other
    # places of the code.
    def display_empty(self) -> None:
        self._pad.noutrefresh(0,0,curses.LINES-1,0,curses.LINES-1,curses.COLS-2)

    def display_main(self) -> None:
        self._pad.noutrefresh(1,0,curses.LINES-1,0,curses.LINES-1,curses.COLS-2)

    def display_running_session(self) -> None:
        self._pad.noutrefresh(2,0,curses.LINES-1,0,curses.LINES-1,curses.COLS-2)     
    
    def display_paused_session(self) -> None:
        self._pad.noutrefresh(3,0,curses.LINES-1,0,curses.LINES-1,curses.COLS-2)

    def display_resume_session(self) -> None:
        self._pad.noutrefresh(4,0,curses.LINES-1,0,curses.LINES-1,curses.COLS-2)
