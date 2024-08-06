'''This module contains helper functions used in the app.'''

import json
from werkzeug.security import generate_password_hash, check_password_hash
from services.constants import USERS_DB, COURSES_DB, USER_COURSES_DB
from services.database import user_exists, add_new_user, get_hashed_password
from services.database import list_user_courses, user_courses_db_contains_user
from services.database import add_new_user_course_list, update_user_course_list
from services.database import add_new_user_to_user_assignments, add_pending_assignments
from services.database import get_pending_assignments, update_pending_assignments
from services.exceptions import InvalidCredentials, InvalidUsername, CourseAlreadySelected
from services.assignment_data import course_assignment_data

def register_user(username: str, password: str) -> None:
    '''
    Creates a new account for the user and stores credentials in users database.

    If entered username is already associated with an account, an InvalidUsername exception is
    raised.
    
    Keyword arguments:
    username -- entered username
    password -- entered password
    '''
    hashed_password = generate_password_hash(password)
    if user_exists(username):
        raise InvalidUsername
    else:
        add_new_user(username, hashed_password)
        add_new_user_to_user_assignments(username)

def login_user(username: str, password: str) -> None:
    '''
    Logs user in based on entered credentials.

    If entered username does not correspond to any account, an InvalidUsername exception is
    raised. If entered password is incorrect for entered username, an InvalidCredentials exception
    is raised.

    Keyword arguments:
    username -- entered username
    password -- entered password
    '''
    hashed_password = get_hashed_password(username)
    if not hashed_password:
        raise InvalidUsername
    elif not check_password_hash(hashed_password, password):
        raise InvalidCredentials

def add_course_to_user(username: str, course_code: str) -> None:
    """Adds a new course to user's course list.
    
    If course is already in user's course list, a CourseAlreadySelected exception is raised.

    Args:
        username (str): user to whom course should be added
        course_code (str): code of course to be added to user
    """
    if not user_courses_db_contains_user(username):
        user_course_list = [course_code]
        new_user_courses_json = json.dumps(user_course_list)
        add_new_user_course_list(username, new_user_courses_json)
    else:
        user_course_list = list_user_courses(username)
        if course_code in user_course_list:
            raise CourseAlreadySelected
        else:
            user_course_list.append(course_code)
            new_user_courses_json = json.dumps(user_course_list)
            update_user_course_list(username, new_user_courses_json)

def remove_course_from_user(username: str, course_code: str) -> None:
    """Removes a course from user's course list.

    Args:
        username (str): user from whom course should be deleted
        course_code (str): code of course to be deleted from user
    """
    user_course_list = list_user_courses(username)
    user_course_list.remove(course_code)
    new_user_courses_json = json.dumps(user_course_list)
    update_user_course_list(username, new_user_courses_json)

def add_new_course_assignments(username: str) -> None:
    """Add assignments of newly added courses to user's pending assignment list.

    Args:
        username (str): user adding a new course
    """
    user_course_list = list_user_courses(username)
    user_pending_assignments = get_pending_assignments(username)
    new_user_courses = []
    for course in user_course_list:
        if course not in user_pending_assignments:
            new_user_courses.append(course)
    for course_code in new_user_courses:
        assignments = course_assignment_data(course_code)
        add_pending_assignments(username, course_code, assignments)

def remove_course_assignments(username: str) -> None:
    """Remove course assignments of removed courses from both pending and completed lists.

    Args:
        username (str): username of user
    """
    user_course_list = list_user_courses(username)
    user_pending_assignments = get_pending_assignments(username)
    removed_courses = []
    for course in user_pending_assignments:
        if course not in user_course_list:
            removed_courses.append(course)
    for course in removed_courses:
        del user_pending_assignments[course]
    pending_assignments_data = json.dumps(user_pending_assignments)
    update_pending_assignments(username, pending_assignments_data)
