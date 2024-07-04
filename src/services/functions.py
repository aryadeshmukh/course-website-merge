# This module contains helper functions used in the app.

from services.constants import USERS_DB
from services.database import get_db_connection
from services.exceptions import InvalidCredentials, InvalidUsername
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username: str, password: str) -> None:
    '''
    Creates a new account for the user and stores credentials in users database.

    If entered username is already associated with an account, an InvalidUsername exception is raised.
    
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

    If entered username does not correspond to any account, an InvalidUsername exception is raised.
    If entered password is incorrect for entered username, an InvalidCredentials exception is raised.

    Keyword arguments:
    username -- entered username
    password -- entered password
    '''
    with get_db_connection(USERS_DB) as con:
        user = con.execute('SELECT hashed_password FROM users WHERE username = ?', (username,)).fetchone()
        if user is None:
            raise InvalidUsername
        elif not check_password_hash(user['hashed_password'], password):
            raise InvalidCredentials