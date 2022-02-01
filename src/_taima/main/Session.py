from _taima.main.queries import UPDATE_DB
from _taima.gen.Time import Time
from _taima.main.routines.animation import anima_per_frame
from _taima.main.routines.animation.keyframes.anima_kf import ANIMA
from concurrent.futures import ThreadPoolExecutor
import curses

# ----------------------------------------------------------------------------
# SESSION CLASS 
# Each timer session started on a task is represented by this class.
# It contains the timer loop and performs the DB update by setting up the 
# corresponding DB_Object.
# The class currently is desinged in a way, that hopefully will allow easy
# implementation of a SubSession class, that inherits from this class. For that
# reason e.g., class attributes instead of instance attributes were used for 
# this class. However this still might change in the future.


class Session(object):
    
    virt: object = None
    db_obj: object = None
    keyframe: tuple = ANIMA

    def __init__(self, db_obj: object, virt: object) -> None:
        type(self).virt = virt
        type(self).db_obj = db_obj                         
    
    
    #function, to update the dbo times and total based on the attributes
    #of the time object. After update of the dbo, the db gets updated too.
    def __update_dbo_and_db(self, time_obj: object):
        
        new_times: tuple = time_obj.strf('%c')
        type(self).db_obj.times.update({new_times[0]:new_times[1]})
        time_obj.calculate_total()
        type(self).db_obj.total += time_obj.total
        
        UPDATE_DB(type(self).db_obj, type(self).virt.mesg)

    
    def run(self) -> None:
        """
        Start the session loop. 
        """
        
        # init all session relevant variables
        exited: bool = False
        paused: bool = False
        frame_index: int = 0
        update_counter: int = 0 
        
        while not exited:
            time_obj = Time()
            time_obj.start_t() 
            
            while not paused:
                #update all windows
                with ThreadPoolExecutor() as exec:
                    exec.submit(type(self).virt.nstruc.display_running_session)
                    exec.submit(type(self).virt.tassk.display_tb_unselected_active)
                    exec.submit(type(self).virt.taima.update_taima, type(self).db_obj, update_counter)                
                                
                curses.doupdate()
                type(self).virt.nonblo.nodelay(1)
                try:
                    action = type(self).virt.nonblo.getch()
                except:
                    action = None

                # pause the timer, get the end time and update 
                # dbo and taima window
                if action == 32:
                    time_obj.end_t()
                    paused = True
                    update_counter += 1
                    self.__update_dbo_and_db(time_obj)
                    with ThreadPoolExecutor() as exec:
                        exec.submit(type(self).virt.taima.update_taima, type(self).db_obj, update_counter)
                        exec.submit(type(self).virt.nstruc.display_resume_session)
                        exec.submit(type(self).virt.tassk.display_tb_unselected_paused)
                    
                    curses.doupdate()
                    curses.napms(1000)
                    type(self).virt.mesg.erase()
                    type(self).virt.mesg.refresh()
                    break
                #---------------END OF PAUSE ----------------

                # calculate the next frame. 
                anima_per_frame.render(type(self).virt.anima, frame_index)

                curses.doupdate()
                curses.napms(167)
                type(self).virt.anima.erase()
                frame_index += 1
                
                # check, if the last frame of the keyframe was reached. If so,
                # reset the index to start from frame 0
                if frame_index == len(type(self).keyframe):
                    frame_index = 0
            

            action = type(self).virt.nonblo.getch()
            # in order to prevent maximum cpu usage by having a non-blocked
            # loop, set nodelay to false
            type(self).virt.nonblo.nodelay(0)
            if  action == 32:
                paused = False
            elif action == 113:
                type(self).virt.nstruc.display_main()
                curses.doupdate()
                exited = True
              
