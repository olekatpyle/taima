import curses
from _taima.main.routines.animation.keyframes.prompter_kf import PROMPTER

#------------------------------------------------------------------------------
# This module holds functions for the prompter animation before entering a 
# taskname.
# The loop function renders the full keyframe, while the single_frame funcition
# renders the frame, that was passed to the function as parameter.

keyframe: tuple = PROMPTER

def loop(prompter: object) -> None:
    """
    Iterate over every frame in the keyframe, add it to the prompter and 
    refresh.
    """
    
    global keyframe
    
    ms: int = 33 
    
    for frame in keyframe:
        y: int = 0 
        x: int = 0
        for comp in frame:
            prompter.addstr(y,x,comp[0],curses.color_pair(comp[1]))
            x += 1
        prompter.refresh()
        curses.napms(ms) 
        ms += 3

    
def single_frame(prompter: object, frame: int)->None:
    """
    Add the specified frame to the prompter and refresh.
    """    
    
    global keyframe
    
    y: int = 0
    x: int = 0
    
    for comp in keyframe[frame]:
        prompter.addstr(y,x,comp[0],curses.color_pair(comp[1]))
        x += 1
    prompter.refresh()    


