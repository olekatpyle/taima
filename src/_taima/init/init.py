#!/usr/bin/env python3

from pathlib import Path 
import sqlite3
from .queries import CREATE_TABLE

#-----------------------------------------------------------------------------#
# INITIALIZATION MODULE
#
# Initialization of the application database.
#
# In order to run the application, you first need to init a database. Currently
# if you supply the argument 'init' to the program, this function will check
# wether there already exists a '.taima/' directory, thus an initialization was 
# already performed. If not, the function will create that directory and create
# the 'workload.db' wiht the needed database table inside of it.
# NOTE: The application won't initialize in directories where user has no 
#       permissions.


def initialize() -> None:
    '''
    Initiation of the database inside the current working directory for the
    application.
    '''
    
    path:    str = str(Path().cwd()) + '/.taima'
    db_path: str = path + '/workload.db'
    
    if not Path(path).exists():
        try:
            Path(path).mkdir(mode=0o770)
        except PermissionError:
            print('Initialization in this directory per default not permitted.')
            exit()
        connection = sqlite3.connect(db_path)
        CREATE_TABLE(connection)
        
        connection.close()
        print("Initilizing database sucessful!")
    else:
        print("The database is already initialized..") 
    exit()
