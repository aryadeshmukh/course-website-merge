import pytest
import tempfile
import os
import sys
from flask import Flask
import sqlite3

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_db_connection

@pytest.fixture
def client():
    '''Create a temporary database for testing.'''
    db_path = 'users.db'
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path

    with app.test_client() as client:
        with app.app_context():
            init_db(db_path)
        yield client

    os.unlink(db_path)

def init_db(db_path):
    '''Initialize empty database.'''
    with get_db_connection(db_path) as con:
        con.execute('DROP TABLE IF EXISTS users')
        con.execute('''CREATE TABLE IF NOT EXISTS users
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        hashed_password TEXT)''')
        con.commit()

def test_register_user(client):
    '''Tests registering a new user.'''
    response = client.post('/register', data={'username': 'testuser2', 'password': 'testpassword'})
    assert response.status_code == 302
    # Check to see if new user has been added to database.
    with get_db_connection(app.config['DATABASE']) as con:
        user = con.execute('SELECT * FROM users where username = ?', ('testuser2',)).fetchone()
        assert user is not None

def test_register_existing_user(client):
    '''Tests registering user whose username already exists in database.'''
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    # Try to register same user again.
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Username already in use. Please try again.' in response.data

def test_login(client):
    '''Tests logging in with an existing account.'''
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302

def test_login_nonexistent_user(client):
    '''Tests logging in using credentials that do not exist.'''
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'No account associated with username. Please try again.' in response.data
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', data={'username': 'differenttestuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'No account associated with username. Please try again.' in response.data

def test_login_wrong_password(client):
    '''Tests logging in using incorrect password.'''
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Username or password is incorrect. Please try again.' in response.data