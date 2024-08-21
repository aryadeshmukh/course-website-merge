'''This module tests refreshing pending assignments list from previous scrapes.'''

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

DATE_1 = date(YEAR, 1, 23)
DATE_2 = date(YEAR, 1, 31)
DATE_3 = date(YEAR, 2, 9)

EECS_HW_0 = f'EECS16B||Homework 00||{YEAR}-01-20'
EECS_LAB_1 = f'EECS16B||Lab 1: Introduction to S1XT33N||{YEAR}-01-27'
EECS_HW_1 = f'EECS16B||Homework 01||{YEAR}-01-27'

@pytest.fixture(scope='module', autouse=True)
def clean_db():
    '''Enables use of a clean database.'''
    initialize_user_info(reset=True)
    register_user(USER_1, 'password')
    add_course_to_user(USER_1, 'EECS16B')
    add_new_course_assignments(USER_1, DATE_1, True)

def test_scraping_after_all_assignments_complete():
    '''This function tests scraping new assignment information when there are no pending
    assignments in the user's pending assignment list.'''
    pending_assignments = all_pending_assignments(USER_1)
    assert len(pending_assignments) == 3
    mark_assignment_complete(USER_1, EECS_HW_0)
    mark_assignment_complete(USER_1, EECS_LAB_1)
    mark_assignment_complete(USER_1, EECS_HW_1)
    pending_assignments = all_pending_assignments(USER_1)
    completed_assignments = all_completed_assignments(USER_1)
    assert len(pending_assignments) == 0
    assert len(completed_assignments) == 3
    add_new_course_assignments(USER_1, DATE_2, True)
    pending_assignments = all_pending_assignments(USER_1)
    completed_assignments = all_completed_assignments(USER_1)
    assert len(pending_assignments) == 2
    assert len(completed_assignments) == 3

def test_adding_new_course():
    '''This function tests adding a new course when an existing course has been scraped.'''
    add_course_to_user(USER_1, 'COMPSCI61B')
    add_new_course_assignments(USER_1, DATE_2, True)
    pending_assignments = all_pending_assignments(USER_1)
    completed_assignments = all_completed_assignments(USER_1)
    assert len(pending_assignments) == 10
    assert len(completed_assignments) == 3

def test_remove_and_add_back_course():
    '''This function tests removing an existing course and then adding it back.'''
    remove_course_from_user(USER_1, 'EECS16B')
    remove_course_assignments(USER_1)
    pending_assignments = all_pending_assignments(USER_1)
    completed_assignments = all_completed_assignments(USER_1)
    assert len(pending_assignments) == 8
    assert len(completed_assignments) == 0
    add_course_to_user(USER_1, 'EECS16B')
    add_new_course_assignments(USER_1, DATE_2, True)
    pending_assignments = all_pending_assignments(USER_1)
    completed_assignments = all_completed_assignments(USER_1)
    assert len(pending_assignments) == 13
    assert len(completed_assignments) == 0

def test_new_user():
    '''This function tests that scraping data for a differnet user has no effect on existing users.'''
    register_user(USER_2, 'password')
    add_course_to_user(USER_2, 'DATAC8')
    add_new_course_assignments(USER_2, DATE_3, True)
    second_user_pending_assignments = all_pending_assignments(USER_2)
    second_user_completed_assignments = all_completed_assignments(USER_2)
    assert len(second_user_pending_assignments) == 10
    assert len(second_user_completed_assignments) == 0
    first_user_pending_assignments = all_pending_assignments(USER_1)
    first_user_completed_assignments = all_completed_assignments(USER_1)
    assert len(first_user_pending_assignments) == 13
    assert len(first_user_completed_assignments) == 0