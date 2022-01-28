import curses
from _taima.gen.screen.Pad import Pad #correct import for production
from _taima.main.queries import GET_RECENT_TASKS
from concurrent.futures import ThreadPoolExecutor
import datetime

class Tassk(Pad):
    """
    Pseudo wrapper class for the taskboard window. A pad is being used underneath,
    to allow for future implementation of scrolling, aswell as simplifiying
    toggling between pad regions.
    The pad has following structure:
    
      window_width   OFF  window_width  OFF
    ----------------|---|--------------|---|
    *---------------*---*--------------*---*  ---+-
    |               |###|              |###|     |
    |    CONTENT    |###|              |###|     |
    |               |###|              |###|     | window_height
    |               |###|              |###|     |
    |               |###|              |###|     |
    *---------------*------------------*---*  ---+-
    |     FOR       |###|              |###| 
    |     SCROLL    |###|              |###|
    |               |###|              |###|

    """
    
    #Wrapper class for the taskboard window of the appliction. The use of a wrapper 
    #class should provide better management of breakpoints, when the screen is
    #manually resized. However, this feature will be available in later versions.

    def __init__(self, height: int, width: int, mode: dict):
        super().__init__(height, width)    

        # the mode currently doesn't really matter, since there is only one
        # mode, which is the default one. It should give an idea for the coming 
        # screen resizing and screen handling mechanism.

        self._win_width:  int = mode['win_width']
        self._win_height: int = mode['win_height']
        self._offset_x:   int = 100
        
        # x_coordinates, that mark the beginning of the different pad areas.
        # tb -> taskboard
        self._tb_empty_x:             int = 0
        self._tb_unselected_x_paused: int = self._tb_empty_x + self._win_width + self._offset_x
        self._tb_unselected_x_active: int = self._tb_unselected_x_paused + self._win_width + self._offset_x
           
        self.__draw_banner() 
        self.__db_obj:  object = None
        self.__db_objs: dict = None
            
        self.display_tb_empty()

    
    # function to draw the banner of each region on the pad. 
    def __draw_banner(self) -> None:
   
        tb: str = ' TASKBOARD '
        
        for i in range(len(tb)):
            
            # not exactly centering the banner.
            y: int = (curses.LINES-4) // 2 - len(tb) // 2 + i 
            
            with ThreadPoolExecutor() as exec:
                exec.submit(self._pad.addstr, y, self._tb_empty_x, ' ', self.W_BG)            
                exec.submit(self._pad.addstr, y, self._tb_empty_x+1, tb[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._tb_empty_x+2, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_paused, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_paused+1, tb[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_paused+2, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_active, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_active+1, tb[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._tb_unselected_x_active+2, ' ', self.W_BG)

    
    # function to update all regions, that need to be updated.
    def update_taskboard(self, db_obj: object) -> None:
        self.__db_obj = db_obj
        self.__db_objs = GET_RECENT_TASKS()
        

        BOLD: object = curses.A_BOLD

        paused:  str = '-> paused'
        active:  str = '-> active'
        current: str = 'Current activity:'
        recent:  str = 'Recent activity:'
        paused_clr: object = curses.color_pair(11) #yellow
        active_clr: object = curses.color_pair(10) #green
        
        #place date
        
        date: str = '[' + self.__db_obj.date.strftime('%b-%d-%Y') + ']'
        
        y:    int = 0
        x1:   int = self._tb_unselected_x_paused + self._win_width // 2 - len(date) // 2
        x2:   int = self._tb_unselected_x_active + self._win_width // 2 - len(date) // 2 
        
        with ThreadPoolExecutor() as exec:
            exec.submit(self._pad.addstr, y, x1, date)
            exec.submit(self._pad.addstr, y, x2, date)
        
        #draw 'current' tag
        y = 2
        x1 = self._tb_unselected_x_paused + 4
        x2 = self._tb_unselected_x_active + 4
        with ThreadPoolExecutor() as exec:
            exec.submit(self._pad.addstr, y, x1, current)
            exec.submit(self._pad.addstr, y, x2, current)


        #place taskname
        y = 3 
        x1 = self._tb_unselected_x_paused + 4
        x2 = self._tb_unselected_x_active + 4
        with ThreadPoolExecutor() as exec:
            exec.submit(self._pad.addstr, y, x1, self.__db_obj.task, BOLD)
            exec.submit(self._pad.addstr, y, x2, self.__db_obj.task, BOLD)


        #draw status
        y = 4 
        x1 = self._tb_unselected_x_paused + 6
        x2 = self._tb_unselected_x_active + 6

        with ThreadPoolExecutor() as exec:
            exec.submit(self._pad.addstr, y, x1, paused, paused_clr)
            exec.submit(self._pad.addstr, y, x2, active, active_clr)

        #draw 'recent' tag 
        y = 6
        x1 = self._tb_unselected_x_paused + 4
        x2 = self._tb_unselected_x_active + 4

        with ThreadPoolExecutor() as exec:
            exec.submit(self._pad.addstr, y, x1, recent)
            exec.submit(self._pad.addstr, y, x2, recent)

        #draw recent tasks
        y = 7
        
        for i in range(len(self.__db_objs)):
            s = self.__db_objs[i].task + ' (' + str(self.__db_objs[i].total) + 'min)' 
            with ThreadPoolExecutor() as exec:
                exec.submit(self._pad.addstr, y, x1, s)
                exec.submit(self._pad.addstr, y, x2, s)
            y += 1    
    
    
    # display methods, performing the refreshes.
    # This simplyfies the implementation in other places of the codebase.
    
    def display_tb_empty(self) -> None:
        self._pad.noutrefresh(0,self._tb_empty_x,2,0,curses.LINES-2,curses.COLS // 3 - 1)
    
    def display_tb_unselected_active(self) -> None:
        self._pad.noutrefresh(0,self._tb_unselected_x_active,2,0,curses.LINES-2,curses.COLS // 3 - 1)
    
    def display_tb_unselected_paused(self) -> None:
        self._pad.noutrefresh(0,self._tb_unselected_x_paused,2,0,curses.LINES-2,curses.COLS // 3 - 1)

    
    # erase the lines, that need to be deleted, before making a clean refresh.
    # Used, when a new task is loaded into the taskboard.
    
    def erase_taskboard(self) -> None:
        coord: tuple = (self._tb_unselected_x_paused, self._tb_unselected_x_active)
        
        def helper(x):
            for y in range(3, self._win_height):
                for i in range(self._win_width):
                    self._pad.addstr(y, x+i+4, ' ')
        
        with ThreadPoolExecutor() as exec:
            exec.submit(helper, coord[0])
            exec.submit(helper, coord[1])

        self._pad.refresh(0,self._tb_unselected_x_paused,2,0,curses.LINES-2,curses.COLS // 3 - 1)
        self._pad.noutrefresh(0,self._tb_unselected_x_active,2,0,curses.LINES-2,curses.COLS // 3 - 1)       
