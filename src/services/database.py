'''Module containing all database handling functions.'''

import sqlite3
from services.constants import USERS_DB, COURSES_DB, COURSES_SQL, USER_COURSES_DB

def get_db_connection(db_file: str):
    '''
    Function to get a database connection
    
    Keyword arguments:
    db_file -- .db file representing the database
    '''
    con = sqlite3.connect(db_file)
    con.row_factory = sqlite3.Row
    return con

def initialize_users_db(reset: bool = False) -> None:
    '''
    Creates users database containing user credential information if it does not already exist.

    If reset is set to true then the existing database is deleted a brand new one is created.

    Keyword arguments:
    reste -- flag indicating whether the database should be erased
    '''
    with get_db_connection(USERS_DB) as con:
        if reset:
            con.execute('DROP TABLE IF EXISTS users')
        con.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            hashed_password TEXT)''')
        con.commit()

def initialize_courses_db(update: bool = False) -> None:
    """Loads in course records from COURSES_SQL if update is set to true or if table does not exist.

    Args:
        update (bool, optional): If true, courses database is reloaded. Defaults to False.
    """
    table_exists = False
    with get_db_connection(COURSES_DB) as con:
        courses = con.execute('''
                              SELECT name FROM sqlite_master WHERE type='table' AND name='courses'
                              ''')
        if courses.fetchone():
            table_exists = True
    if update or not table_exists:
        sql_script = ''
        with open(COURSES_SQL, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        with get_db_connection(COURSES_DB) as con:
            con.executescript(sql_script)

def initialize_user_courses_db(reset: bool = False) -> None:
    """Creates a database containing information about each user's selected courses.
    
    If reset is set to True, the existing database is deleted and a new one is created.

    Args:
        reset (bool, optional): Database is erased and reset if true. Defaults to False.
    """
    with get_db_connection(USER_COURSES_DB) as con:
        if reset:
            con.execute('DROP TABLE IF EXISTS user_courses')
        con.execute('''CREATE TABLE IF NOT EXISTS user_courses
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            course_list_data TEXT)''')
        con.commit()

def initialize_user_info(reset: bool = False) -> None:
    """Creates all user databases if they do not exist already.
    
    If reset is set to true, all user databases are erased and reset.

    Args:
        reset (bool, optional): If true, user databases are reset. Defaults to False.
    """
    initialize_users_db(reset=reset)
    initialize_user_courses_db(reset=reset)
    