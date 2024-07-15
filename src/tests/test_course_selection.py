'''This module tests course selection functionality.'''

import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.functions import add_course_to_user, remove_course_from_user, list_user_courses
from services.exceptions import CourseAlreadySelected
from services.database import initialize_user_courses_db

@pytest.fixture(scope='module', autouse=True)
def clean_db():
    '''Enables use of a clean database.'''
    initialize_user_courses_db(reset=True)

def test_add_course_to_user():
    '''Tests adding a course to a user.'''
    add_course_to_user('user1', 'EECS16B')
    add_course_to_user('user1', 'COMPSCI61B')
    assert list_user_courses('user1') == ['EECS16B', 'COMPSCI61B']

def test_add_course_different_user():
    '''Tests adding courses to multiple users.'''
    add_course_to_user('user2', 'DATAC8')
    add_course_to_user('user2', 'EECS16B')
    assert list_user_courses('user1') == ['EECS16B', 'COMPSCI61B']
    assert list_user_courses('user2') == ['DATAC8', 'EECS16B']
    
def test_add_existing_course():
    '''Tests adding a course that a user already has selected.'''
    with pytest.raises(CourseAlreadySelected):
        add_course_to_user('user1', 'COMPSCI61B')
    assert list_user_courses('user1') == ['EECS16B', 'COMPSCI61B']
    
def test_remove_course_from_user():
    '''Tests removing a course from a user.'''
    remove_course_from_user('user1', 'EECS16B')
    assert list_user_courses('user1') == ['COMPSCI61B']
    assert list_user_courses('user2') == ['DATAC8', 'EECS16B']
