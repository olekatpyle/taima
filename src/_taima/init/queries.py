import sqlite3

#------------------------------------------------------------------------------
# QUERIES
#
# Module that contains all queries the init functionality needs.

def CREATE_TABLE(connection: object) -> None:
    '''
    Create the workload table in the database.
    '''

    cur: object = connection.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS workload(task TEXT NOT NULL,
                                                    date DATE NOT NULL,
                                                    times TEXT NOT NULL,
                                                    total INTEGER NOT NULL);
    """)

    connection.commit()

