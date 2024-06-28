from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_db_connection():
    '''Function to get a database connection'''
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    return con

with get_db_connection() as con:
    '''Create the users table if it doesn't exist.'''
    con.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE,
                     hashed_password TEXT)''')
    con.commit()

@app.route('/')
def home():
    return 'Success!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Creates a new account for the user.

    If entered username is already in use, user must choose a different username.
    Password is hashed before being stored in the database for security purposes.
    '''
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        with get_db_connection() as con:
            if con.execute('SELECT username FROM users WHERE username = ?', (username,)).fetchone():
                error = 'Username already in use. Please try again.'
            else:
                con.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                            (username, hashed_password))
                con.commit()
                return redirect(url_for('login'))
    return render_template('register.html', error=error)

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
        with get_db_connection() as con:
            user = con.execute('SELECT hashed_password FROM users WHERE username = ?', (username,)).fetchone()
            if user is None:
                error = 'No account associated with username. Please try again.'
            elif not check_password_hash(user['hashed_password'], password):
                error = 'Username or password is incorrect. Please try again.'
            else:
                return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)