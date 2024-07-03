# This module tests registration and login functionality

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import _register, _login
from database import get_db_connection, initialize_users_db
from exceptions import InvalidCredentials, InvalidUsername

USERS_DB = 'users.db'

@pytest.fixture(scope='module', autouse=True)
def clean_db():
    '''Enables use of a clean database.'''
    initialize_users_db(erase=True)

def test_register_user():
    '''Test registering new user.'''
    try:
        _register('testuser', 'testpassword')
        # with get_db_connection(USERS_DB) as con:
        #     user = con.execute('SELECT username WHERE username = ?', ('testuser',)).fetchone()
        #     assert user
    except InvalidUsername:
        assert False

def test_login_user():
    '''Test logging in existing user.'''
    try:
        _login('testuser', 'testpassword')
        # with get_db_connection(USERS_DB) as con:
        #     user = con.execute('SELECT username WHERE username = ?', ('testuser',)).fetchone()
        #     assert user
    except InvalidUsername:
        assert False
    except InvalidCredentials:
        assert False

def test_register_already_existing_username():
    '''Tests registering with an existing username.'''
    with pytest.raises(InvalidUsername):
        _register('testuser', 'othertestpassword')

def test_login_nonexistent_user():
    '''Tests logging in a non-existent user.'''
    with pytest.raises(InvalidUsername):
        _login('othertestuser', 'testpassword')

def test_login_incorrect_credentials():
    '''Tests logging in a user with incorrect credentials.'''
    with pytest.raises(InvalidCredentials):
        _login('testuser', 'othertestpassword')