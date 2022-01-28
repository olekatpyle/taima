import curses

from _taima.gen.screen.Stdscr import Stdscr
from _taima.main.screen.comp.Nstruc import Nstruc
from _taima.main.screen.comp.Tassk import Tassk
from _taima.main.screen.comp.Taima import Taima

#-----------------------------------------------------------------------------
# SCREEN CLASS
# The screen class is the engine to allow the use of curses and easily make
# the windows and pads managable. In order to get access to the screen components,
# properties are being used, to allow calls in other places of the codebase.
# Having a screen class should allow for easy screen resizing and handling 
# features, such as color initialization, based on the properties of the 
# used terminal.


class Screen(Stdscr):
    
    def __init__(self, stdscr: object, mode: str):
        super().__init__(stdscr)       
        
        # mode definitions, to be passed to the main windows.
        default_mode: dict = {'mode': 'default', 'win_height': self.screen_height - 3, 'win_width': self.screen_width // 3}

        self.__mesg:     object = self.__init_window(1, curses.COLS, 0, 0, 232)
        self.__prompt:   object = self.__init_window(1, curses.COLS-4,1,4,232)
        self.__prompter: object = self.__init_window(1,4,1,0, 232)
        self.__anima:    object = self.__init_window(curses.LINES-3,curses.COLS//3,2,curses.COLS//3,232)
        self.__tassk:    object = Tassk(500, 10000, default_mode)
        self.__taima:    object = Taima(500, 10000, default_mode)
        self.__nstruc:   object = Nstruc(10,1000)
        self.__nonblo:   object = self.__init_window(1,1,curses.LINES-1,curses.COLS-1,232)
        
        self.__mesg.addstr(0,0,'Screen components initialized!', curses.color_pair(233) | curses.A_BOLD)
        self.__mesg.noutrefresh()
        curses.doupdate()
        curses.napms(1000)
        self.__mesg.erase()
    
    
    def __init_window(self, nlines: int, ncols: int, begin_y: int, begin_x: int, bkgd_color: int) -> object:
        window: object = curses.newwin(nlines, ncols, begin_y, begin_x)
        window.nodelay(0)
        window.bkgd(' ', curses.color_pair(bkgd_color))
        window.noutrefresh()

        return window

    #Getter and properties
    def __get_mesg(self) ->     object:
        return self.__mesg
    def __get_prompt(self) ->   object:
        return self.__prompt
    def __get_prompter(self) -> object:
        return self.__prompter
    def __get_anima(self) ->    object:
        return self.__anima
    def __get_taima(self) ->    object:
        return self.__taima
    def __get_tassk(self) ->    object:
        return self.__tassk
    def __get_nstruc(self) ->   object:
        return self.__nstruc
    def __get_nonblo(self) ->   object:
        return self.__nonblo


    mesg =      property(__get_mesg)
    prompt =    property(__get_prompt)
    prompter =  property(__get_prompter)
    anima =     property(__get_anima)
    taima =     property(__get_taima)
    tassk =     property(__get_tassk)
    nstruc =    property(__get_nstruc)
    nonblo =    property(__get_nonblo)
