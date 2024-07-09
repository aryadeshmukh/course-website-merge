'''Module containing all database handling functions.'''

import sqlite3
from services.constants import USERS_DB

def get_db_connection(db_file: str):
    '''
    Function to get a database connection
    
    Keyword arguments:
    db_file -- .db file representing the database
    '''
    con = sqlite3.connect(db_file)
    con.row_factory = sqlite3.Row
    return con

def initialize_users_db(erase=False) -> None:
    '''
    Creates users database containing user credential information if it does not already exist.

    If erase is set to true then the existing database is deleted a brand new one is created.

    Keyword arguments:
    erase -- flag indicating whether the database should be erased
    '''
    with get_db_connection(USERS_DB) as con:
        if erase:
            con.execute('DROP TABLE IF EXISTS users')
        con.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            hashed_password TEXT)''')
        con.commit()
