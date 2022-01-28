import json
from datetime import date, datetime

#-----------------------------------------------------------------------------
# DB_OBJECT CLASS
#
# In order to manage, read and write from and to the database inside the
# application, the DB_Object class serves as the data container for any 
# database entry. The class instance properties are used, to allow the 
# data manipulation inside the application.

class DB_Object(object):
    
    def __init__(self):
        self.__task:  str = '' 
        self.__date:  object = date.today()
        self.__times: dict = {} 
        self.__total: int = 0

    
    def __get_task(self) -> str:
        return self.__task
    
    def __get_date(self) -> object:
        return self.__date
    
    def __get_times(self) -> dict:
        return self.__times
    
    def __get_total(self) -> int:
        return self.__total

    def __set_task(self, task: str) -> None:
        self.__task = task
      
    def __set_date(self, date: object) -> None:
        self.__date = date
    
    def __set_times(self, times: str) -> None:
        self.__times = self.__jsonparser(times)

    def __set_total(self, total: int) -> None:
        self.__total = total

    
    # helper function for 'setTimes' to convert a json string into 
    # a python dictionary.
    # Whenever the database is read to initialize a new DB_Object, 
    # which represents an entry inside the database, the times
    # property is read as a json string, that needs to be converted into
    # a dictionary in order to manage the DB_Object in the application.  
    def __jsonparser(self, times: str) -> dict:
        if isinstance(times, str):
            try:
                return json.loads(times)
            except json.JSONDecodeError:
                return {}
    
       
    task =  property(__get_task, __set_task)
    date =  property(__get_date, __set_date)
    times = property(__get_times, __set_times)
    total = property(__get_total, __set_total)
