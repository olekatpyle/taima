import curses
from _taima.main.routines.animation.keyframes.anima_kf import ANIMA

#-----------------------------------------------------------------------------
# MAIN ANIMATION
#
# This module defines the function, that calculates the frame at a given
# frame index of the main animation defined in the keyframe package.
# After calculation, the frame is drawn to the window, which then gets 
# prepared for refresh with noutrefresh().
# Using a single frame calculation proofs to have faster react times to 
# key events. It also helps to resume the animation at the frame, that it
# was initially paused at.
#-----------------------------------------------------------------------------

def render(anima: object, frame_index: int) -> None:
    """
    Routine to draw a single frame of the main-animation, based on the supplied
    frame index.
    """
    
    keyframe: tuple = ANIMA
        
    #center on the y axis
    y: int = (curses.LINES - 4) // 2 - len(ANIMA[0]) // 2 
    for string in keyframe[frame_index]:
        length: list = []
        for substring in string:
            length.append(len(substring))

        #the obtained lengths of the substring serve the 
        #purpose to position the substrings in a way, that
        #once concatenated to the complete line, this line will be 
        #centered based on the size of the screen.
        i: int = 0
        for substring in string:
            if i == 0:
                x = curses.COLS // 3 // 2 - length[1] // 2 - length[0]
            elif i == 2:
                x = curses.COLS // 3 // 2 + length[1] // 2
                    #we need to take care of repositioning the
                    #last substring, if the middle one has an uneven
                    #char count.
                if length[1] % 2 != 0:
                    x += 1
            else:
                x = curses.COLS // 3 // 2 - length[1] // 2
            #finally add the calculated line to the window

            anima.addstr(y, x, substring, curses.color_pair(string[substring]) | curses.A_BOLD)
            i += 1
        y += 1
    anima.noutrefresh()        

