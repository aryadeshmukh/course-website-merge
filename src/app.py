'''This module contains the server implmentation of Course Website Merger.'''

from flask import Flask, render_template, request, redirect, url_for
from services.exceptions import InvalidCredentials, InvalidUsername
from services.database import initialize_users_db
from services.functions import register_user, login_user

app = Flask(__name__)

initialize_users_db(erase=False)

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
            return redirect(url_for('home'))
        except InvalidUsername:
            error = 'No account associated with username. Please try again.'
        except InvalidCredentials:
            error = 'Username or password is incorrect. Please try again.'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
