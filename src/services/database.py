'''Module containing all database handling functions.'''

import sqlite3
import json
from services.constants import USERS_DB, COURSES_DB, COURSES_SQL, USER_COURSES_DB
from services.constants import USER_ASSIGNMENTS_DB, UPDATES_DB

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

def user_exists(username: str) -> bool:
    """Returns true if user with input username exists in users database.

    Args:
        username (str): username to be checked

    Returns:
        bool: true if user exists in users database with input username otherwise false
    """
    with get_db_connection(USERS_DB) as con:
        if con.execute('SELECT username FROM users WHERE username = ?', (username,)).fetchone():
            return True
        else:
            return False

def add_new_user(username: str, hashed_password: str) -> None:
    """Inserts record for new user in users database.

    Args:
        username (str): username of new user
        hashed_password (str): hashed password of new user
    """
    with get_db_connection(USERS_DB) as con:
        con.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                    (username, hashed_password))
        con.commit()

def get_hashed_password(username: str) -> str:
    """Returns hashed password of user associated with username.
    
    Returns None if user does not exists.

    Args:
        username (str): _description_

    Returns:
        str: _description_
    """
    if user_exists(username):
        with get_db_connection(USERS_DB) as con:
            user = (
                con
                .execute('SELECT hashed_password FROM users WHERE username = ?', (username,))
                .fetchone()
            )
            return user['hashed_password']
    else:
        return None

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

def list_courses() -> list:
    """Returns a list of all courses users can choose.

    Returns:
        list: A list of all courses users can choose
    """
    courses = []
    with get_db_connection(COURSES_DB) as con:
        rows = con.execute('SELECT course_code FROM courses').fetchall()
        for row in rows:
            courses.append(row['course_code'])
    return courses

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

def user_courses_db_contains_user(username: str) -> bool:
    """Returns true if user's data exists in user courses database.

    Args:
        username (str): user to check

    Returns:
        bool: true if user's data exists in user courses database otherwise false
    """
    with get_db_connection(USER_COURSES_DB) as con:
        user = (
            con
            .execute('SELECT username FROM user_courses WHERE username = ?', (username,))
            .fetchone()
        )
        if not user:
            return False
        else:
            return True

def list_user_courses(username: str) -> list:
    """Returns the user's selected course list.

    Args:
        username (str): user whos course list should be returned

    Returns:
        list: list containing all courses in user's course list
    """
    with get_db_connection(USER_COURSES_DB) as con:
        user_courses_json = (
            con
            .execute('SELECT course_list_data FROM user_courses WHERE username = ?', (username,))
            .fetchone()
        )
        if not user_courses_json:
            return []
        else:
            user_course_list = json.loads(user_courses_json[0])
            return user_course_list

def add_new_user_course_list(username: str, course_list_data: str) -> None:
    """Adds a new user's course list to the user course list database.

    Args:
        username (str): user whose data should be added
        course_list_data (str): data of user's course list
    """
    with get_db_connection(USER_COURSES_DB) as con:
        con.execute('INSERT INTO user_courses (username, course_list_data) VALUES (?, ?)',
                    (username, course_list_data))
        con.commit()

def update_user_course_list(username: str, course_list_data: str) -> None:
    """Updates user's course list.

    Args:
        username (str): user whose course list should be updated
        course_list_data (str): updated course list data
    """
    with get_db_connection(USER_COURSES_DB) as con:
        con.execute('UPDATE user_courses SET course_list_data = ? WHERE username = ?',
                    (course_list_data, username))
        con.commit()

def initialize_user_assignments_db(reset: bool = False) -> None:
    """Creates a database containing user assignment information for both pending and
    completed assignments.

    Args:
        reset (bool, optional): Erases and resets database if ture. Defaults to False.
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        if reset:
            con.execute('DROP TABLE IF EXISTS user_assignments')
        con.execute('''CREATE TABLE IF NOT EXISTS user_assignments
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            pending_assignments_data TEXT,
                            completed_assignments_data TEXT)''')
        con.commit()

def add_new_user_to_user_assignments(username: str) -> None:
    """Adds a new record to user_assignments database corresponding to new user.

    Args:
        username (str): user to be added to user_assignments database
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        con.execute('''INSERT INTO user_assignments
                    (username, pending_assignments_data, completed_assignments_data)
                    VALUES (?, ?, ?)''',
                    (username,
                     json.dumps({}),
                     json.dumps({})))
        con.commit()

def get_pending_assignments(username: str) -> dict:
    """Returns a dictionary containing all of the user's pending assignments.

    Args:
        username (str): username of user

    Returns:
        dict: dictionary containing all of the user's pending assignments
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        pending_assignments_json = (
            con
            .execute('SELECT pending_assignments_data FROM user_assignments WHERE username = ?',
                     (username,))
            .fetchone()
        )
        if not pending_assignments_json:
            return {}
        else:
            return json.loads(pending_assignments_json[0])

def get_completed_assignments(username: str) -> dict:
    """Returns a dictionary containing all of the user's completed assignments.

    Args:
        username (str): username of user

    Returns:
        dict: dictionary containing all of the user's completed assignments
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        completed_assignments_json = (
            con
            .execute('SELECT completed_assignments_data FROM user_assignments WHERE username = ?',
                     (username,))
            .fetchone()
        )
        if not completed_assignments_json:
            return {}
        else:
            return json.loads(completed_assignments_json[0])

def add_pending_assignments(username: str, course_code: str, assignments: list) -> None:
    """Adds the assignments to the list of user's pending assignments.

    Args:
        username (str): user with new pending assignments
        course_code (str): course to which new pending assignments belong
        assignments (list): list of tuples corresponding to new pending assignments
    """
    pending_assignments = get_pending_assignments(username)
    if course_code not in pending_assignments:
        pending_assignments[course_code] = []
    pending_assignments[course_code].extend(assignments)
    pending_assignments_json = json.dumps(pending_assignments)
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        con.execute('''UPDATE user_assignments SET pending_assignments_data = ?
                    WHERE username = ?''', (pending_assignments_json, username))
        con.commit()

def update_pending_assignments(username: str, pending_assignments_data: str) -> None:
    """Replaces existing pending assignment data with new input data.

    Args:
        username (str): user whose pending assignments are to be updated
        pending_assignments_data (str): new pending assignment data
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        con.execute('''UPDATE user_assignments SET pending_assignments_data = ?
                    WHERE username = ?''', (pending_assignments_data, username))
        con.commit()

def update_completed_assignments(username: str, completed_assignments_data: str) -> None:
    """Replaces existing completed assignment data with new input data.

    Args:
        username (str): user whos completed assignments are to be updated
        completed_assignments_data (str): new completed assignment data
    """
    with get_db_connection(USER_ASSIGNMENTS_DB) as con:
        con.execute('''UPDATE user_assignments SET completed_assignments_data = ?
                    WHERE username = ?''', (completed_assignments_data, username))
        con.commit()

def add_completed_assignment(username: str, completed_assignment: tuple) -> None:
    """Add an assignment to user's completed assignments.

    Args:
        username (str): username of user
        completed_assignment (tuple): information of completed assignment
    """
    completed_assignments = get_completed_assignments(username)
    course_code = completed_assignment[0]
    if course_code not in completed_assignments:
        completed_assignments[course_code] = []
    completed_assignments[course_code].append(completed_assignment)
    completed_assignments_data = json.dumps(completed_assignments)
    update_completed_assignments(username, completed_assignments_data)

def initialize_updates_db(reset: bool = False) -> None:
    """Creates a database containing each user's most recent update date.

    Args:
        reset (bool, optional): Erases and resets database if ture. Defaults to False.
    """
    with get_db_connection(UPDATES_DB) as con:
        if reset:
            con.execute('DROP TABLE IF EXISTS updates')
        con.execute('''CREATE TABLE IF NOT EXISTS updates
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            previous_update_date TEXT)''')
        con.commit()

def update_previous_update_date(username: str, new_date_str: str) -> None:
    """Updates previous update date of user to new update date if user record exists in
    updates database. Otherwise adds user record to updates database.

    Args:
        username (str): username of user
        new_date_str (str): date to update previous_update_date
    """
    with get_db_connection(UPDATES_DB) as con:
        new_user = (
            con
            .execute('SELECT username FROM updates WHERE username = ?', (username,))
            .fetchone() is None
        )
        if new_user:
            con.execute('''INSERT INTO updates
                        (username, previous_update_date)
                        VALUES (?, ?)''',
                        (username, new_date_str))
        else:
            con.execute('''UPDATE updates SET previous_update_date = ?
                        WHERE username = ?''', (new_date_str, username))
        con.commit()

def get_previous_update_date_str(username: str) -> str:
    """Returns the string representation of the previous date the user's assignments
    list was updated.

    Args:
        username (str): username of user

    Returns:
        str: string representation of previous date the user's assignments list was updated
    """
    with get_db_connection(UPDATES_DB) as con:
        prev_update_date_str = (
            con
            .execute('SELECT previous_update_date FROM updates WHERE username = ?',
                     (username,))
            .fetchone()
        )
        return prev_update_date_str and prev_update_date_str[0]

def initialize_user_info(reset: bool = False) -> None:
    """Creates all user databases if they do not exist already.
    
    If reset is set to true, all user databases are erased and reset.

    Args:
        reset (bool, optional): If true, user databases are reset. Defaults to False.
    """
    initialize_users_db(reset=reset)
    initialize_user_courses_db(reset=reset)
    initialize_user_assignments_db(reset=reset)
    initialize_updates_db(reset=reset)

def get_course_link(course_code: str) -> str:
    """Returns url of course page of course.
    
    Returns None if there is no entry in courses database corresponding to course_code.

    Args:
        course_code (str): course_code of course

    Returns:
        str: url of webpage of course
    """
    try:
        with get_db_connection(COURSES_DB) as con:
            course_url = (
                con
                .execute('SELECT course_link FROM courses WHERE course_code = ?',
                         (course_code,))
                .fetchone())
            return course_url[0]
    except Exception:
        return None
    