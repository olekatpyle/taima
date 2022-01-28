import sqlite3
import curses
from _taima.gen.screen.Color import Color as c

#-----------------------------------------------------------------------------
# DB_CONNECTION 
#utility function to connect to the database. Pass in a window to display
#status reports on the screen.


def ping_db(mesg: object) -> int:
    '''
    Ping the database, to check if it was already initialized.
    '''

    try:
        mesg.addstr(0,0,'Connecting to database..', curses.color_pair(c.W_YELLOW.value) | curses.A_BOLD)
        mesg.refresh()
        curses.napms(1000)
        connection: object = sqlite3.connect('.taima/workload.db',
                                detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.OperationalError:
        mesg.addstr(0,0,'No database found. Have you initialized it? See help (taima -h) for more information.', curses.color_pair(c.W_RED.value) | curses.A_BOLD)
        return -1
    except Exception as ex:
        mesg.addstr(0,0,'Unknown error occured..', curses.color_pair(c.W_RED.value) | curses.A_BOLD)
        return -1
    else:
        mesg.addstr(0,0,'Successfully connected to database..', curses.color_pair(c.W_GREEN.value) | curses.A_BOLD)
    finally:    
        mesg.refresh()
    return 0    


def connect() -> object:
    '''
    Silent connect.
    '''

    try:
        connection: object = sqlite3.connect('.taima/workload.db',
                                detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.OperationalError:
        return None 
    except Exception as ex:
        return None
    return connection  


# In order to connect from subpackages, the connection path needs to be
# altered.
def connect_subpkg() -> object:
    '''
    Silent connect for the queries inside the subpackages. 
    '''

    try:
        connection = sqlite3.connect('./.taima/workload.db',
                        detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.OperationalError:
        return None 
    except Exception as ex:
        return None
    return connection  


