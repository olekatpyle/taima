import sqlite3
from _taima.gen.util.db_connection import connect

#---------------------------------------------------------------------------------------
# Module, containing all database queries, the wipe functionality uses.

def WIPE_DATABASE() -> int:
    '''
    Wipe every entry in the database. Return the total amount of rows
    affected by the transaction.
    '''

    connection: object = connect()
    cur: object = connection.cursor()

    cur.execute("""
                DELETE FROM workload;""")

    connection.commit()
    rows_affected: int = cur.rowcount

    connection.close()
    return rows_affected


def DELETE_TASK(task: str) -> int:
    '''
    Delete all entries for the specified task. Return the total amount of rows
    affected by the transaction.
    '''

    connection: object = connect()
    cur: object = connection.cursor()

    cur.execute("""
                DELETE FROM workload WHERE task = ?;
                """,(task,))

    connection.commit()
    rows_affected: int = cur.rowcount

    connection.close()
    return rows_affected
    
