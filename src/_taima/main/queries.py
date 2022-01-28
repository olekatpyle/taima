import sqlite3
from _taima.gen.DB_Object import DB_Object    
from _taima.gen.util.db_connection import connect
from _taima.gen.screen.Color import Color as c
import json
import curses

#------------------------------------------------------------------------------
# QUERIES
#
# This module holds all db queries, wrapped in function, that are called during 
# runtime of the application.
# The queries are called in various places, mostly the Session
# class, the main program or in the window classes. In general, a query gets 
# passed the connection, the current db_object and a screen component to display
# notifications.
#------------------------------------------------------------------------------


# helper function for UPDATE_DB 
def parseTimes(db_obj: object) -> str:
    return json.dumps(db_obj.times)


# query, to get the most recent tasks, that were worked on.
# Returning all db_objects representing those tasks, in order for
# the task board to work with.
def GET_RECENT_TASKS() -> dict:
    '''
    Return a dictionary of the 5 latest entries in the database by date.
    '''    

    connection: object = connect()
    cur:        object = connection.cursor()

    query:      object = cur.execute("""
                            SELECT * FROM workload 
                            ORDER BY rowid DESC LIMIT 0,5
                            """)

    entries: dict = {}
    
    i = 0
    for row in query.fetchall():
        db_obj = DB_Object()
        db_obj.task = row[0]
        db_obj.date = row[1]    
        db_obj.times = row[2]
        db_obj.total = row[3]
        entries.update({i:db_obj})
        i += 1       
    
    connection.close()     
    return entries 
    

# query, to check the status of a supplied taskname. If the task was already
# inserted in the database with todays date, user continues on that task,
# rather than creating a new entry in the database

def CHECK_TASK(db_obj: object, mesg: object) -> object:
    '''
    Check, if the task was already added today.
    '''

    connection: object = connect()
    cur: object = connection.cursor()
   
    mesg.erase()
    mesg.refresh()
    
    cur.execute("""
                SELECT * FROM workload
                WHERE task = ? AND date = ?;
                """,
                (db_obj.task, db_obj.date))
    
    stat: tuple = cur.fetchone()
    if not stat:
        cur.execute("""
                    INSERT INTO workload VALUES(?,?,"{}",0);
                    """,
                    (db_obj.task, db_obj.date))
        
        connection.commit()     
        
        notify: str = f'New entry {db_obj.task} in database was created!'
        mesg.addstr(0,0,notify,curses.color_pair(c.W_BLACK.value))
        mesg.noutrefresh() 
    else:
        cur.execute("""
                    SELECT times, total FROM workload
                    WHERE task = ? AND date = ?;
                    """,
                    (db_obj.task, db_obj.date))
    
        vals: list = list(cur.fetchone())
        db_obj.times = vals[0]
        db_obj.total = vals[1]
        notify = f'Continuing to work on task {db_obj.task}!'
        mesg.addstr(0,0,notify,curses.color_pair(c.W_BLACK.value))
        mesg.noutrefresh() 

    connection.close()
    return db_obj


# query to update the times for the database entry that user is currently 
# working on. 

def UPDATE_DB(db_obj: object, mesg: object) -> None:
    
    connection: object = connect()
    cur: object = connection.cursor()

    cur.execute("""
                UPDATE workload
                SET times = ?,
                total = ?
                WHERE task = ? AND date = ?;
                """, 
                (parseTimes(db_obj), db_obj.total, db_obj.task, db_obj.date))
    
    mesg.erase()
    mesg.refresh()
    
    if cur.rowcount == 1:
        mesg.addstr(0,0,'Database updated successfully', curses.color_pair(c.W_GREEN.value))
    else:
        mesg.addstr(0,0,'Couldn\'t update database..', curses.color_pair(c.W_RED.value))
    
    mesg.noutrefresh()
    connection.commit()
    connection.close()


