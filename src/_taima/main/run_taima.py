
import curses
from curses import wrapper
from _taima.gen.DB_Object import DB_Object 
from _taima.gen.util.db_connection import ping_db
from _taima.gen.screen.Color import Color as c
from _taima.main.screen.Screen import Screen
from _taima.main.routines import enter_taskname
from _taima.main.routines.animation import init_anima
from _taima.main.Session import Session 
from _taima.main import queries

#------------------------------------------------------------------------------
# MAIN
#
# Main runs the argument_handler which calls the corresponding functions, runs the
# screen initialization, opens and closes the connection to the database
# and starts the timer sessions. The timer sessions
# are embedded in the main loop, that sets up the task to be worked on and allows
# the correct exit out of the program.
# The main loop is to be seen as the main menu of the application.
# It is wrapped in the curses wrapper, to simplify curses init.
#------------------------------------------------------------------------------

def run(stdscr: object, arg: str) -> None:
    #----
    # SETUP
    #----
    
    virt: object = Screen(stdscr, 'default_mode')

    # check, if a connection can be established.
    if ping_db(virt.mesg) == -1:
        curses.napms(3000)
        exit()
    
    curses.napms(1000)
    virt.mesg.erase()
    
    # check if task argument was supplied on program call
    if arg:
        task: str = arg.strip()
        arg = None        
    # if not, run the enter_taskname routine to let the user define one
    else:
        task: str = enter_taskname.run(virt.prompter, virt.prompt, virt.mesg) 
        curses.napms(500)

    # initialize the db_object, to handle the data for the database and check,
    # wether there already exists a task with the same name.
    db_obj: object = DB_Object()
    db_obj.task = task
    db_obj = queries.CHECK_TASK(db_obj, virt.mesg)

    virt.tassk.update_taskboard(db_obj)
    virt.taima.update_todo(db_obj)
    curses.doupdate()
    
    # initialize a timer session
    session: object = Session(db_obj, virt)

    # TODO: Refactor the following class into a seperate module inside a
    # listener package

    #----
    # MAIN LOOP
    #----

    inMain: bool = True
    doInit: bool = True

    while inMain:
        
        # run the initial animation and refresh all needed windows
        if doInit:
            virt.nstruc.display_main()
            virt.tassk.display_tb_unselected_paused()
            virt.taima.display_todo_unselected()
            curses.doupdate()
            init_anima.run(virt.anima)
            doInit = False
            curses.napms(800)
            virt.mesg.erase()
            virt.mesg.refresh()
        try:
            key: int = virt.nonblo.getch()
        except:
            key = None

        # start the session with space    
        if key == 32:
            session.run()
        # quit out of the program with q
        elif key == 113:
            virt.mesg.erase()
            virt.mesg.addstr(0, 0, 'Goodbye!', curses.color_pair(c.W_BLACK.value))
            virt.mesg.refresh()
            curses.napms(1000)
            break
        # specify a new task with e
        elif key == 101:
            # delete the current session instance and clear the taima window
            # for the new task
            del session
            virt.taima.erase_taima()

            #update windows
            virt.taima.display_todo_empty()
            virt.anima.erase()
            virt.anima.noutrefresh()
            curses.doupdate()

            #set up new task
            task = enter_taskname.run(virt.prompter, virt.prompt, virt.mesg)
            db_obj = DB_Object()
            db_obj.task = task
            db_obj = queries.CHECK_TASK(db_obj, virt.mesg)
            session = Session(db_obj, virt)

            #update windows
            virt.tassk.erase_taskboard()
            virt.tassk.update_taskboard(db_obj)
            virt.taima.display_todo_unselected()
            curses.doupdate()

            # initial animation
            init_anima.run(virt.anima)
            curses.napms(500)
            virt.mesg.erase()
            virt.mesg.refresh()



