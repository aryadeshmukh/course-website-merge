'''This module contains the server implmentation of Course Website Merger.'''

import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from services.exceptions import InvalidCredentials, InvalidUsername
from services.database import initialize_user_info, initialize_courses_db
from services.functions import register_user, login_user, list_courses
from services.constants import ALPHABET

app = Flask(__name__)

app.secret_key = ''.join(secrets.choice(ALPHABET) for _ in range(16))

initialize_user_info(reset=False)
initialize_courses_db(update=False)

@app.route('/')
def home():
    return 'Success!'

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
            register_user(username, password)
            session['username'] = username
            return redirect(url_for('login'))
        except InvalidUsername:
            error = 'Username already in use. Please try again.'
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Logs in user.

    If username is not associated with an account or if password is incorrect, user must try again
    before proceeding.
    '''
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            login_user(username, password)
            session['username'] = username
            return redirect(url_for('home'))
        except InvalidUsername:
            error = 'No account associated with username. Please try again.'
        except InvalidCredentials:
            error = 'Username or password is incorrect. Please try again.'
    return render_template('login.html', error=error)

@app.route('/select-courses', methods=['GET', 'POST'])
def select_courses():
    error = None
    if request.method == 'POST':
        pass
    return render_template('course-selection.html', error=error, courses=list_courses())

if __name__ == '__main__':
    app.run(debug=True)
