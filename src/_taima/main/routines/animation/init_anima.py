from _taima.main.routines.animation.keyframes.init_anima_kf import INIT_ANIMA 
import curses

#------------------------------------------------------------------------------
# INIT ANIAMTION
#
# This module defines the function for the initial animation inside of the
# main program. Unlike the main animation, each frame is rendered and drawn
# on the window inside a loop.

def run(anima: object) -> None:
    """
    Run the init animation for the anima window.
    """
    
    keyframe: tuple = INIT_ANIMA
    anima.noutrefresh()
    curses.doupdate()
    
    ms: int = 50     
    
    for frame in keyframe:
        anima.erase() 
        
        # calculate the top y_coordinate, so the animation starts
        # centered vertically.

        y: int = (curses.LINES - 4) // 2 - len(frame) // 2 
        
        
        for string in frame:
            length: list = []
            for substring in string:
                length.append(len(substring))

            i: int = 0
            
            for substring in string:
                if i == 0:
                    x = curses.COLS // 3 // 2 - length[1] // 2 - length[0]
                elif i == 2:
                    x = curses.COLS // 3 // 2 + length[1] // 2
                    if length[1] % 2 != 0:
                        x += 1
                else:
                    x = curses.COLS // 3 // 2 - length[1] // 2
                            
                anima.addstr(y, x, substring, curses.color_pair(string[substring]) | curses.A_BOLD)
                i += 1
            y += 1
        
        anima.noutrefresh()
        curses.doupdate()
        curses.napms(ms)
        ms += 3

