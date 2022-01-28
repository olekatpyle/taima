from datetime import datetime

#-----------------------------------------------------------------------------
# TIME CLASS
#
# The time class wraps datetime objects and allow application specific
# methods to manage time inside the application.


class Time(object):

    def __init__(self):
        self.__start: object = None
        self.__end:   object = None
        self.__total: int = 0


    def __get_start(self) -> object:
        return self.__start
    
    def __get_end(self) -> object:
        return self.__end
    
    def __get_total(self) -> int:
        return self.__total

    def __set_start(self, start: object) -> None:
        self.__start = start
    
    def __set_end(self, end: object) -> None:
        self.__end = end
   
    
    start = property(__get_start, __set_start)
    end =   property(__get_end, __set_end)
    total = property(__get_total)

    
    def start_t(self) -> None:
        """
        Set start time.
        """
        self.__start = datetime.now()

    def end_t(self) -> None:
        """
        Set end time.
        """
        self.__end = datetime.now()
    
    
    # function, to calculate the total, and rounding the result up, when 30 seconds
    # and more are left.
    # TODO: currently there is a bug, when calculation the total between a 
    # time stamp before 12pm and a timestamp after 12pm.

    def calculate_total(self) -> None:
        """
        Calculate the total for this time instance.
        """
        self.__total = self.__end - self.__start
        self.__total = int(round(self.__total.total_seconds() / 60))
    
    
    # stringify this instances start and end time and return both stored 
    # in a tuple.
    
    def strf(self) -> tuple:
        """
        Return start and end as string inside of a tuple, for this time
        instance.
        """
        s: str = self.__start.strftime('%X')
        e: str = self.__end.strftime('%X')

        return (s, e)

      
