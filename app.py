# This module contains the server implmentation of Course Website Merger

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from exceptions import InvalidCredentials, InvalidUsername
from constants import USERS_DB
from database import get_db_connection, initialize_users_db

app = Flask(__name__)

initialize_users_db(erase=False)

@app.route('/')
def home():
    return 'Success!'

def _register(username: str, password: str) -> None:
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Endpoint for user to create new account.

    For posts, entered username and password are passed into _register function.
    Error message is returned if _register function raises InvalidUsername error.
    For gets, screen for user to register is shown.
    '''
    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            _register(username, password)
            return redirect(url_for('login'))
        except InvalidUsername:
            error = 'Username already in use. Please try again.'
    return render_template('register.html', error=error)

def _login(username: str, password: str) -> None:
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
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Logs in user.

    If username is not associated with an account or if password is incorrect, user must try again before
    proceeding.
    '''
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            _login(username, password)
            return redirect(url_for('home'))
        except InvalidUsername:
            error = 'No account associated with username. Please try again.'
        except InvalidCredentials:
            error = 'Username or password is incorrect. Please try again.'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)