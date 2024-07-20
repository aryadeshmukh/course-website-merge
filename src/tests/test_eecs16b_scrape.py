'''This module tests scraping assignment information from EECS16B cpirse website.'''

import sys
import os
from typing import List, Tuple
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.scraping import _scrape_eecs16b
from services.dates import date_comparator

@pytest.fixture(scope='module')
def assignments_info() -> Tuple[List[str], List[str], List[str], List[str], List[Tuple[str]]]:
    """Returns a tuple containing lists of EECS16B assignment information to run tests on.

    Returns:
        Tuple[List[str], List[str], List[str], List[str], List[Tuple[str]]]:
        tuple containing lists of EECS16B assignment information
    """
    return _scrape_eecs16b(test_link='https://eecs16b.org/')

def filter_assignments_info(assignments_info, indices):
    '''Filters assignments_info to only contain assignments corresponding to those in indices.'''
    class_ = [assignments_info[0][i] for i in indices]
    assignments = [assignments_info[2][i] for i in indices]
    due_dates = [assignments_info[3][i] for i in indices]
    links = [assignments_info[4][i] for i in indices]
    return class_, assignments, due_dates, links

def test_homeworks(assignments_info):
    '''Tests correct scraping of homework data'''
    homework_indices = []
    for i, assignment_type in enumerate(assignments_info[1]):
        if assignment_type == 'Homework':
            homework_indices.append(i)

    # Test that all homework assignments were scraped
    assert len(homework_indices) == 14

    homework_class, assignments, due_dates, links = filter_assignments_info(
        assignments_info, homework_indices)

    # Test that all assignments are EECS16B assignments
    for class_ in homework_class:
        assert class_ == 'EECS16B'

    # Test that selected assignments are homework assignments
    for assignment in assignments:
        assert 'Homework' in assignment

    # Test that assignments are sorted in nearest-due-date order
    prev_due_date_val = 0
    for date in due_dates:
        curr_date_val = date_comparator(date)
        assert curr_date_val > prev_due_date_val
        prev_due_date_val = curr_date_val

    # Test homework links
    for i, homework_link_info in enumerate(links):
        if i != 8:
            assert len(homework_link_info) == 1
        else:
            assert len(homework_link_info) == 3

def test_exams(assignments_info):
    '''Tests correct scraping of exam data'''
    exam_indices = []
    for i, assignment_type in enumerate(assignments_info[1]):
        if assignment_type == 'Exam':
            exam_indices.append(i)

    # Test that all exam assignments were scraped
    assert len(exam_indices) == 2

    exam_class, assignments, due_dates, links = filter_assignments_info(
        assignments_info, exam_indices)

    # Test that all assignments are EECS16B assignments
    for class_ in exam_class:
        assert class_ == 'EECS16B'

    # Test that selected assignments are exam assignments
    for assignment in assignments:
        assert 'MT' in assignment

    # Test that assignments are sorted in nearest-due-date order
    prev_due_date_val = 0
    for date in due_dates:
        curr_date_val = date_comparator(date)
        assert curr_date_val > prev_due_date_val
        prev_due_date_val = curr_date_val

    # Test exam links
    for exam_link_info in links:
        assert exam_link_info == [(None, None)]

def test_labs(assignments_info):
    '''Tests correct scraping of lab data'''
    lab_indices = []
    for i, assignment_type in enumerate(assignments_info[1]):
        if assignment_type == 'Lab':
            lab_indices.append(i)

    # Test that all lab assignments were scraped
    assert len(lab_indices) == 11

    lab_class, assignments, due_dates, links = filter_assignments_info(
        assignments_info, lab_indices)

    # Test that all assignments are EECS16B assignments
    for class_ in lab_class:
        assert class_ == 'EECS16B'

    # Test that selected assignments are lab assignments
    for assignment in assignments:
        assert 'Lab' in assignment

    # Test that assignments are sorted in nearest-due-date order
    prev_due_date_val = 0
    for date in due_dates:
        curr_date_val = date_comparator(date)
        assert curr_date_val > prev_due_date_val
        prev_due_date_val = curr_date_val

    # Test lab links
    assert len(links[0]) == 5
    assert len(links[2]) == 6
    assert links[7] == [(None, None)]
