'''This module tests registration and login functionality.'''

import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.functions import register_user, login_user
from services.database import initialize_users_db
from services.exceptions import InvalidCredentials, InvalidUsername

@pytest.fixture(scope='module', autouse=True)
def clean_db():
    '''Enables use of a clean database.'''
    initialize_users_db(reset=True)

def test_register_user():
    '''Test registering new user.'''
    try:
        register_user('testuser', 'testpassword')
        # with get_db_connection(USERS_DB) as con:
        #     user = con.execute('SELECT username WHERE username = ?', ('testuser',)).fetchone()
        #     assert user
    except InvalidUsername:
        assert False

def test_login_user():
    '''Test logging in existing user.'''
    try:
        login_user('testuser', 'testpassword')
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
        register_user('testuser', 'othertestpassword')

def test_login_nonexistent_user():
    '''Tests logging in a non-existent user.'''
    with pytest.raises(InvalidUsername):
        login_user('othertestuser', 'testpassword')

def test_login_incorrect_credentials():
    '''Tests logging in a user with incorrect credentials.'''
    with pytest.raises(InvalidCredentials):
        login_user('testuser', 'othertestpassword')
