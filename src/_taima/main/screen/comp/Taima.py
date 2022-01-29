import curses
from _taima.gen.screen.Pad import Pad
from _taima.main.queries import GET_RECENT_TASKS
from _taima.gen.Time import Time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Taima(Pad):
    """
    Pseudo wrapper class for the taima window. A pad is being used underneath,
    to allow for future implementation of scrolling, aswell as simplifying
    toggling between pad regions.
    The pad has the following structure:

      WINDOW_WIDTH    OFF  WINDOW_WIDTH     OFF
    |----------------|---|-----------------|---|
    
    *----------------*---*-----------------*---*  ---+-
    |                |XXX|                 |XXX|     |
    |                |XXX|                 |XXX|     |
    |    CONTENT     |XXX|                 |XXX|     | WINDOW_HEIGHT
    |                |XXX|                 |XXX|     |
    |                |XXX|                 |XXX|     |
    *----------------*---*-----------------*---*  ---+-
    |    FOR         |XXX|                 |XXX|     |
    |    SCROLL      |XXX|                 |XXX|     |
    |                |XXX|                 |XXX|     |

    """ 
    
    def __init__(self, height: int, width: int, mode: dict):
        super().__init__(height, width)
       
        # the mode currently doesn't really matter, since there is only one
        # mode, which is the default one. It should give an idea for the coming
        # screen resizing and screen handling mechanism.
        self._win_width:  int = mode['win_width']
        self._win_height: int = mode['win_height']
        self._offset_y:   int = 10
        self._offset_x:   int = 200

        # x_coordinates, at which the different pad areas start.
        # td -> todo, tm -> taima
        self._td_empty_x: int = 0
        self._tm_empty_x: int = self._td_empty_x + self._win_width + self._offset_x
        self._td_unselected_x: int = self._tm_empty_x + self._win_width + self._offset_x
        self._tm_unselected_x: int = self._td_unselected_x + self._win_width + self._offset_x
            
        self.__draw_banner()
        self.__db_obj = None
        self.__db_objs = None 
        self.display_todo_empty()
    
    
    # method, to draw the banner for each region on the pad.
    
    def __draw_banner(self) -> None:
        td: str = '   TODO    '
        tm: str = '   TAIMA   '

        for i in range(len(td)):
            y = (curses.LINES-4) // 2 - len(td) // 2 + i
            with ThreadPoolExecutor() as exec:
                #empty todo
                exec.submit(self._pad.addstr, y, self._td_empty_x+self._win_width, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._td_empty_x+self._win_width-1, td[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._td_empty_x+self._win_width-2, ' ', self.W_BG)
                #empty taima
                exec.submit(self._pad.addstr, y, self._tm_empty_x+self._win_width, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tm_empty_x+self._win_width-1, tm[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._tm_empty_x+self._win_width-2, ' ', self.W_BG)
                #todo unselected
                exec.submit(self._pad.addstr, y, self._td_unselected_x+self._win_width, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._td_unselected_x+self._win_width-1, td[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._td_unselected_x+self._win_width-2, ' ', self.W_BG)
                #taima unselected
                exec.submit(self._pad.addstr, y, self._tm_unselected_x+self._win_width, ' ', self.W_BG)
                exec.submit(self._pad.addstr, y, self._tm_unselected_x+self._win_width-1, tm[i], self.W_BLACK)
                exec.submit(self._pad.addstr, y, self._tm_unselected_x+self._win_width-2, ' ', self.W_BG)
    
    
    # display methods, wrapping the pad refreshes, in order to simplify usage
    # in other places of the codebase.
    
    def display_todo_unselected(self) -> None:
        #currently only used for showcase of future feature
        self._pad.noutrefresh(0, self._td_unselected_x, 2, self._win_width*2, curses.LINES-2, curses.COLS-1)
    
    def display_todo_empty(self) -> None:
        self._pad.noutrefresh(0, self._td_empty_x, 2, self._win_width*2, curses.LINES-2, curses.COLS-1) 
    
    def update_todo(self, db_obj: object) -> None:
        y: int = 0
        x: int = self._td_unselected_x + 2
        self._pad.addstr(y, x, 'Nothing TODO', curses.A_BOLD) 
    
    # update function for the taima window.
    def update_taima(self, db_obj: object, update_counter: int) -> None:
        
        # using a list to store color values, in order to get an 
        # iterable for when drawing on the pad.
        colors: list = [
                        self.DEF_PURP__,
                        self.DEF_PURP_0,
                        [
                            self.DEF_PURP_1,
                            self.DEF_PURP_2,
                            self.DEF_PURP_3,
                            self.DEF_PURP_4,
                            self.DEF_PURP_5,
                            self.DEF_PURP_6 
                        ],
                        self.DEF_PURP_7
                        ]
        
        # get the latest times of the db_obj
        latest: list = list(reversed(sorted(db_obj.times.keys())))[:6]
        latest.reverse()
        times: dict = db_obj.times
 
        # draw the lines for the taima window
        y: int = 2 
        
        # draw 'task total'
        x: int = self._tm_unselected_x + 1    
        s: str = 'Task total:          '
        
        self._pad.addstr(y, x, s)
        x += len(s)
        self._pad.addstr(y, x, f'{str(db_obj.total)}min', colors[3] | self.BOLD)

        y = 5

        # draw the dots, if the list consists more than six entries.
        # the update counter is defined in the run function of the Session class.
        # It helps to track how many updates were peformed, and respectively
        # add one dot the first time, 7 time entries were made, afterwards
        # adding two dots. If the session was initialized with an db_obj that
        # already had that many entries, draw two dots (update_counter == 0)
        
        # TODO: This is not working correctly. However the exact behaviour needs
        # to be examined further in detail. 
        
        x = self._tm_unselected_x + 1
        
        if update_counter == 7:
            y = 4
            for i in range(self._win_width - 4):
                self._pad.addstr(y, x+i, ' ')
            self._pad.refresh(0,self._tm_unselected_x,2,self._win_width*2,curses.LINES-2,curses.COLS-1)   

            #add one dot
            self._pad.addstr(y,x,'.',colors[0])
            y = 5
             
        if update_counter > 7:
            y = 3
            #clear the lines for the dots starting at x + i.
            #subtract 4 to not delete the banner.
            for i in range(self._win_width - 4):
                self._pad.addstr(y, x+i, ' ')
                self._pad.addstr(y+1, x+i, ' ')
            self._pad.refresh(0,self._tm_unselected_x,2,self._win_width*2,curses.LINES-2,curses.COLS-1)     
            
            #add two dots
            self._pad.addstr(y,x,'.',colors[0])
            y += 1
            self._pad.addstr(y,x,'..',colors[1])
            y += 1 
        
        if update_counter == 0 and len(latest) > 5:
            y = 3
            #clear the lines for the dots starting at x + i.
            #subtract 4 to not delete the banner.
            for i in range(self._win_width - 4):
                self._pad.addstr(y, x+i, ' ')
                self._pad.addstr(y+1, x+i, ' ')
            self._pad.refresh(0,self._tm_unselected_x,2,self._win_width*2,curses.LINES-2,curses.COLS-1)     
            
            #add two dots
            self._pad.addstr(y,x,'.',colors[0])
            y += 1
            self._pad.addstr(y,x,'..',colors[1])
            y += 1

        #draw all entries line by line
        for i in range(len(latest)):
            t = Time()
            t.start = datetime.strptime(latest[i], '%c')
            t.end = datetime.strptime(times[latest[i]], '%c')
            t.calculate_total()
            stamps = t.strf('%X')
            s = stamps[0]
            e = stamps[1]

            x = self._tm_unselected_x + 1
            self._pad.addstr(y, x, s)
            
            x += len(s) + 1
            self._pad.addstr(y, x, ':')
            x += 2
            self._pad.addstr(y, x, e)
            x += len(e)+2
            s = str(t.total) + 'min'
            self._pad.addstr(y, x, s, colors[2][i])
            
            y += 1

        self._pad.noutrefresh(0,self._tm_unselected_x,2,self._win_width*2,curses.LINES-2,curses.COLS-1)

    
    # function to clear all lines in every region that is specified by its x-
    # coordinate. The implementation is already designed, to clear multiple 
    # region of the pad concurrently in the future.
    def erase_taima(self) -> None:
        coord: tuple = (self._tm_unselected_x, -1)

        def helper(x: int) -> None:
            for y in range(2, 12):
                for i in range(self._win_width-4):
                    self._pad.addstr(y, x+i, ' ')
   
        with ThreadPoolExecutor() as exec:
            exec.submit(helper, coord[0])

        self._pad.noutrefresh(0,self._tm_unselected_x,2,self._win_width*2,curses.LINES-2,curses.COLS-1) 

