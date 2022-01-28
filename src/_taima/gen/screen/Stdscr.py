import curses

#-----------------------------------------------------------------------------
# STANDARD SCREEN CLASS
#
# Wrapper class for the stdscr - standard screen.
# It acts as default layer for the actual screens used by the funcionalities
# of this application, that support a GUI. 
# Default behaviour of the stdscr are being set up here aswell as the 
# initialization of the color palette used by the application.

class Stdscr(object):
    
    
    def __init__(self, stdscr: object):
        curses.start_color()
        curses.use_default_colors()
        
        self.__init_color_pairs()
   

        curses.curs_set(0)
        curses.cbreak(1)
        curses.noecho()
        stdscr.keypad(1)
        stdscr.nodelay(0)
        stdscr.clear()
        stdscr.refresh()    
        
        self.screen_width: int = curses.COLS
        self.screen_height: int = curses.LINES 
        
    
    # method, to enable all colors currently used in the application.
    # Although the for-loop initializes all supported 256 colors on
    # curses color_pairs in range 0 - 255, the color_pairs in range
    # 232 - 255 are being overwritten for the colors with white background.
    
    def __init_color_pairs(self) -> None:

        # initialize all colors with default background.
        for i in range(0, curses.COLORS):
            curses.init_pair(i,i,-1)

        #White Background
        curses.init_pair(232, -1, 231)
        #Black on white
        curses.init_pair(233, 0, 231)
        #Purple on white
        curses.init_pair(234, 171, 231)
        #Yellow on white
        curses.init_pair(235, 220, 231)
        #Red on white
        curses.init_pair(236, 160, 231)
        #Green on white
        curses.init_pair(237, 35, 231)
        
        #Purple gradient colors
        curses.init_pair(238, 225, 231)
        curses.init_pair(239, 219, 231)
        curses.init_pair(240, 213, 231)
        curses.init_pair(241, 177, 231)
        curses.init_pair(242, 171, 231)
        curses.init_pair(243, 135, 231)
        curses.init_pair(244, 129, 231)
         
        #colors for main animation
        curses.init_pair(245, 227, 231)
        curses.init_pair(246, 182, 231)

        #greyscale on white
        curses.init_pair(247, 248, 231)
        curses.init_pair(248, 251, 231)
        curses.init_pair(249, 254, 231)
        
        #curses.init_pair(248, -1, 171)
        #curses.init_pair(249, 183, 231)

        
