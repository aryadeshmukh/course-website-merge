'''This module tests marking and unmarking assignments as complete for different users.'''

from datetime import date
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.database import initialize_user_info
from services.functions import register_user, add_course_to_user, remove_course_from_user
from services.functions import add_new_course_assignments, remove_course_assignments
from services.functions import mark_assignment_complete, mark_assignment_incomplete
from services.assignment_data import all_pending_assignments, all_completed_assignments
from services.constants import YEAR

USER_1 = 'test-user-1'
USER_2 = 'test-user-2'
TEST_DATE = date(YEAR, 1, 26)
EECS_HW_1 = f'EECS16B||Homework 00||{YEAR}-01-20'
EECS_LAB_1 = f'EECS16B||Lab 1: Introduction to S1XT33N||{YEAR}-01-27'
CS_HW_1 = f'COMPSCI61B||Homework 0A||{YEAR}-01-19'
CS_LAB_1 = f'COMPSCI61B||Lab 1: Setup||{YEAR}-01-19'

@pytest.fixture(scope='module', autouse=True)
def clean_db():
    '''Enables use of a clean database.'''
    initialize_user_info(reset=True)
    register_user(USER_1, 'password')
    register_user(USER_2, 'password')
    add_course_to_user(USER_1, 'EECS16B')
    add_course_to_user(USER_1, 'COMPSCI61B')
    add_course_to_user(USER_2, 'EECS16B')
    add_new_course_assignments(USER_1, TEST_DATE, True)
    add_new_course_assignments(USER_2, TEST_DATE, True)

def test_pending_assignments():
    '''This function tests whether all newly scraped assignments are added to
    pending assignments.'''
    first_user_pending_assignments = all_pending_assignments(USER_1)
    second_user_pending_assignments = all_pending_assignments(USER_2)
    assert len(first_user_pending_assignments) == 9
    assert len(second_user_pending_assignments) == 3
    first_user_completed_assignments = all_completed_assignments(USER_1)
    second_user_completed_assignments = all_completed_assignments(USER_2)
    assert len(first_user_completed_assignments) == 0
    assert len(second_user_completed_assignments) == 0

def test_mark_assignments_complete():
    '''This function tests that assignments marked as complete are removed from
    pending assignments and added to completed assignments.'''
    mark_assignment_complete(USER_1, EECS_HW_1)
    mark_assignment_complete(USER_1, CS_HW_1)
    mark_assignment_complete(USER_2, EECS_LAB_1)
    first_user_pending_assignments = all_pending_assignments(USER_1)
    second_user_pending_assignments = all_pending_assignments(USER_2)
    first_user_completed_assignments = all_completed_assignments(USER_1)
    second_user_completed_assignments = all_completed_assignments(USER_2)
    assert len(first_user_pending_assignments) == 7
    assert len(second_user_pending_assignments) == 2
    assert len(first_user_completed_assignments) == 2
    assert len(second_user_completed_assignments) == 1

def test_add_and_remove_courses():
    '''This function tests each user's assignments lists after changing courses.'''
    remove_course_from_user(USER_1, 'COMPSCI61B')
    add_course_to_user(USER_2, 'DATAC8')
    remove_course_assignments(USER_1)
    add_new_course_assignments(USER_2, TEST_DATE, True)
    first_user_pending_assignments = all_pending_assignments(USER_1)
    second_user_pending_assignments = all_pending_assignments(USER_2)
    first_user_completed_assignments = all_completed_assignments(USER_1)
    second_user_completed_assignments = all_completed_assignments(USER_2)
    assert len(first_user_pending_assignments) == 2
    assert len(second_user_pending_assignments) == 6
    assert len(first_user_completed_assignments) == 1
    assert len(second_user_completed_assignments) == 1

def test_mark_assignments_incomplete():
    '''This function tests that assignments marked as incomplete are removed from
    completed assignments and added back to pending assignments.'''
    mark_assignment_incomplete(USER_1, EECS_HW_1)
    mark_assignment_incomplete(USER_2, EECS_LAB_1)
    first_user_pending_assignments = all_pending_assignments(USER_1)
    second_user_pending_assignments = all_pending_assignments(USER_2)
    first_user_completed_assignments = all_completed_assignments(USER_1)
    second_user_completed_assignments = all_completed_assignments(USER_2)
    assert len(first_user_pending_assignments) == 3
    assert len(second_user_pending_assignments) == 7
    assert len(first_user_completed_assignments) == 0
    assert len(second_user_completed_assignments) == 0
