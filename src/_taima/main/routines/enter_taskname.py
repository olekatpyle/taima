import curses
from _taima.main.routines.animation import prompter_animation as ani
from _taima.main.routines.animation.keyframes.prompter_kf import PROMPTER
from _taima.gen.screen.Color import Color as c

#-----------------------------------------------------------------------------
# ENTER TASKNAME
#
# This routine sets up a prompt for the user, to enter a taskname on the screen.
# It makes use of some animation features for visual pleasure.
#-----------------------------------------------------------------------------

def run(prompter: object, prompt: object, mesg: object) -> str:
    """
    Start the enter_taskname routine.
    The enter_taskname routine serves the purpose of letting the 
    user define a new task name. It then returns the taskname as 
    string.
    """
   
    #TODO: add KEY_UP and KEY_DOWN events, to select between already 
    #defined tasks in the past. Try a list as container for the last 
    #ten tasks, that were added to the database.

    #Disable newline mode, to remap the ENTER key to a submit functionality.
    curses.nonl()
    
    #Position the window cursor.    
    prompt.move(0,0) 

    keyframe: tuple = PROMPTER
    string: str = ''
    frame: int = 0
    x: int = 0
    
    mesg.addstr(0,0,'Enter task name', curses.color_pair(c.W_BLACK.value))
    mesg.refresh()
    
    # Run the prompter animation.
    
    ani.loop(prompter)
    prompt.addstr(0,0,'_',curses.color_pair(c.W_PURPLE.value) | curses.A_BLINK | curses.A_BOLD)
    
    while 1:
        try:
            key: str = prompt.getkey()
        except:
            key = None
        
        if key is None:
            continue
        # Submit taskname
        elif ord(key) == 13:
            prompter.erase()
            prompter.refresh()
            prompt.erase()
            prompt.refresh()
            mesg.erase()
            mesg.refresh()
            return string
        # Delete character
        elif ord(key) == 127:
            ani.single_frame(prompter, frame)
            if x == 0:
                continue
            string = string[:-1]
            x -= 1
            prompt.move(0,x)
            prompt.addstr(y,x,'_ ', curses.color_pair(c.W_PURPLE.value) | curses.A_BLINK | curses.A_BOLD)
            frame -= 1
            if frame == -1:
                frame = len(keyframe)-1
        # Write to prompt
        else:
            ani.single_frame(prompter, frame)
            y = 0
            if x > 25:
                continue 
            else:
                string += key
                prompt.addstr(y,x,key,curses.color_pair(c.W_BLACK.value))
                prompt.addstr(y,x+1,'_',curses.color_pair(c.W_PURPLE.value) | curses.A_BLINK | curses.A_BOLD)
                x += 1
            frame += 1
            if frame == len(keyframe):
                frame = 0
