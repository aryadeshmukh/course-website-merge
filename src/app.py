'''This module contains the server implmentation of Course Website Merger.'''

from datetime import date
import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from services.exceptions import InvalidCredentials, InvalidUsername
from services.exceptions import CourseAlreadySelected, NoCourseSelected
from services.database import initialize_user_info, initialize_courses_db
from services.database import list_courses, list_user_courses
from services.functions import register_user, login_user
from services.functions import add_course_to_user, remove_course_from_user
from services.functions import add_new_course_assignments, remove_course_assignments
from services.functions import mark_assignment_complete, mark_assignment_incomplete
from services.constants import ALPHABET
from services.assignment_data import all_pending_assignments, all_completed_assignments

app = Flask(__name__)

app.secret_key = ''.join(secrets.choice(ALPHABET) for _ in range(16))

initialize_user_info(reset=True)
initialize_courses_db(update=False)

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
            return redirect(url_for('select_courses'))
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
            return redirect(url_for('assignments'))
        except InvalidUsername:
            error = 'No account associated with username. Please try again.'
        except InvalidCredentials:
            error = 'Username or password is incorrect. Please try again.'
    return render_template('login.html', error=error)

@app.route('/select-courses', methods=['GET', 'POST'])
def select_courses():
    '''
    User directed to course selection page after successfull registration.
    
    If user selects a course that is already in the user's course list, user must try again.
    User must select at least one course before proceeding.
    '''
    username = session['username']
    error = None
    if request.method == 'POST':
        if request.form.get('form_id') == 'add-course':
            # User adds a new course
            try:
                course_code = request.form['course']
                if not course_code:
                    raise NoCourseSelected
                add_course_to_user(username, course_code)
            except CourseAlreadySelected:
                error = 'Course already selected.'
            except NoCourseSelected:
                error = None
        elif request.form.get('form_id') == 'remove-course':
            # User removes a course
            course_code = request.form['course']
            remove_course_from_user(username, course_code)
        else:
            # User submits selected courses
            if len(list_user_courses(username)) < 1:
                error = 'You must select at least one course to proceed.'
            else:
                remove_course_assignments(username)
                add_new_course_assignments(username, date.today())
                session['assignments-view'] = 'pending'
                return redirect(url_for('assignments'))
    return render_template('course-selection.html',
                           error=error,
                           courses=list_courses(),
                           user_courses=list_user_courses(username))

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    '''
    User is directed to assignments page after successful login or course selection.
    
    User sees assignments of all selected courses and assignment information.
    Assignments are shown in sorted order. The assignment with the nearest due date
    is shown first.
    '''
    username = session['username']
    if request.method == 'POST':
        assignments_view = request.form.get('assignments-view')
        if assignments_view:
            session['assignments-view'] = assignments_view
        assignments_view = session['assignments-view']
        minimum_assignment_info_str = request.form.get('marked-assignment')
        if minimum_assignment_info_str:
            if assignments_view == 'pending':
                mark_assignment_complete(username, minimum_assignment_info_str)
            else:
                mark_assignment_incomplete(username, minimum_assignment_info_str)
    assignments_view = session['assignments-view']
    if assignments_view == 'completed':
        assignments_info = all_completed_assignments(username)
    else:
        assignments_info = all_pending_assignments(username)
    return render_template('assignments-calendar.html',
                           assignments_info=assignments_info,
                           assignments_view=assignments_view)

if __name__ == '__main__':
    app.run(debug=True)
