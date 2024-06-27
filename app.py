from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)

db = Database.load_state()
# db.clear()

@app.route('/')
def home():
    return 'Success!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Creates an new account for the user.

    If entered username is already in use, user must choose a different username.
    '''
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.contains(username):
            print('Username already in use.')
            error = 'Username already in use. Please try again.'
        else:
            print('Register successful.')
            db.add_record(username)
            db.add_record([username, password])
            return redirect(url_for('home'))
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
        if not db.contains(username):
            print('Username not in database.')
            error = f'No account associated with username: {username}. Please try again.'
        elif not db.contains([username, password]):
            print('Incorrect password.')
            error = 'Username or password is incorrect. Please try again.'
        else:
            print('Log in successful.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)