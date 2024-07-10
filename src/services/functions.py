'''This module contains helper functions used in the app.'''

from werkzeug.security import generate_password_hash, check_password_hash
from services.constants import USERS_DB, COURSES_DB, USER_COURSES_DB
from services.database import get_db_connection
from services.exceptions import InvalidCredentials, InvalidUsername

def register_user(username: str, password: str) -> None:
    '''
    Creates a new account for the user and stores credentials in users database.

    If entered username is already associated with an account, an InvalidUsername exception is
    raised.
    
    Keyword arguments:
    username -- entered username
    password -- entered password
    '''
    hashed_password = generate_password_hash(password)
    with get_db_connection(USERS_DB) as con:
        if con.execute('SELECT username FROM users WHERE username = ?', (username,)).fetchone():
            raise InvalidUsername
        else:
            con.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                        (username, hashed_password))
            con.commit()

def login_user(username: str, password: str) -> None:
    '''
    Logs user in based on entered credentials.

    If entered username does not correspond to any account, an InvalidUsername exception is
    raised. If entered password is incorrect for entered username, an InvalidCredentials exception
    is raised.

    Keyword arguments:
    username -- entered username
    password -- entered password
    '''
    with get_db_connection(USERS_DB) as con:
        user = (
            con
            .execute('SELECT hashed_password FROM users WHERE username = ?', (username,))
            .fetchone()
        )
        if user is None:
            raise InvalidUsername
        elif not check_password_hash(user['hashed_password'], password):
            raise InvalidCredentials

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

def add_course_to_user(username: str, course: str) -> None:
    """Adds a new course to user's course list.

    Args:
        username (str): user to whom course should be added
        course (str): course to be added to user
    """
    raise NotImplementedError

def remove_course_from_user(username: str, course: str) -> None:
    """Removes a course from user's course list.

    Args:
        username (str): user from whom course should be deleted
        course (str): course to be deleted from user
    """
    raise NotImplementedError

def list_user_courses(username: str) -> list:
    """Returns the user's selected course list.

    Args:
        username (str): user whos course list should be returned

    Returns:
        list: list containing all courses in user's course list
    """
    raise NotImplementedError
