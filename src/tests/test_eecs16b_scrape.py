'''This module tests scraping assignment information from EECS16B course website.'''

from datetime import date
import sys
import os
import pytest
from helper_test_functions import filter_assignments_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.assignments_info import AssignmentsInfo
from services.scrapers.eecs16b_scraper import scrape_eecs16b
from services.constants import YEAR

@pytest.fixture(scope='module')
def assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing EECS16B assignment information.

    Returns:
        AssignmentInfo: AssignmentInfo object containing EECS16B assignment information.
    """
    end_date = date(YEAR, 5, 5)
    with open('course_websites/eecs16b_full.txt', 'r', encoding='utf-8') as file:
        return scrape_eecs16b(file.read(), end_date)

@pytest.fixture
def dated_assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing EECS16B assignment information up to a certain date.

    Returns:
        AssignmentInfo: AssignmentInfo object containing EECS16B assignment information.
    """
    mid_date = date(YEAR, 2, 20)
    with open('course_websites/eecs16b_full.txt', 'r', encoding='utf-8') as file:
        return scrape_eecs16b(file.read(), mid_date)

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 14, 'Homework'),
    ('Exam', 2, 'MT'),
    ('Lab', 11, 'Lab')
])
def test_assignment_scraping(
    assignments_info: AssignmentsInfo,
    assignment_type: str,
    num_assignments: int,
    assignment_type_indicator: str):
    '''Tests correct scraping of all non-link assignment data.'''
    assignment_type_indices = []
    for i, type_ in enumerate(assignments_info.assignment_types):
        if type_ == assignment_type:
            assignment_type_indices.append(i)

    # Test that all assignments were scraped
    assert len(assignment_type_indices) == num_assignments

    filtered_assignments_info = filter_assignments_info(assignments_info, assignment_type_indices)

    # Test that all assignments are EECS16B assignments
    for course in filtered_assignments_info.assignment_courses:
        assert course == 'EECS16B'

    # Test that selected assignments are of correct type
    for assignment in filtered_assignments_info.assignment_names:
        assert assignment_type_indicator in assignment

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 6, 'Homework'),
    ('Exam', 1, 'MT'),
    ('Lab', 5, 'Lab')
])
def test_dated_assignment_scraping(
    dated_assignments_info: AssignmentsInfo,
    assignment_type: str,
    num_assignments: int,
    assignment_type_indicator: str):
    '''Tests correct scraping of all in scope assignment data.'''
    assignment_type_indices = []
    for i, type_ in enumerate(dated_assignments_info.assignment_types):
        if type_ == assignment_type:
            assignment_type_indices.append(i)

    # Test that all assignments were scraped
    assert len(assignment_type_indices) == num_assignments

    filtered_assignments_info = filter_assignments_info(
        dated_assignments_info,
        assignment_type_indices)

    # Test that selected assignments are of correct type
    for assignment in filtered_assignments_info.assignment_names:
        assert assignment_type_indicator in assignment

def test_assignment_links_scraping(assignments_info: AssignmentsInfo):
    '''Tests correct scraping of all link assignment data.'''
    homework_indices = []
    exam_indices = []
    lab_indices = []
    for i, type_ in enumerate(assignments_info.assignment_types):
        if type_ == 'Homework':
            homework_indices.append(i)
        elif type_ == 'Exam':
            exam_indices.append(i)
        else:
            lab_indices.append(i)

    homework_links_info = (
        filter_assignments_info(assignments_info, homework_indices)
        .links_info)
    exam_links_info = (
        filter_assignments_info(assignments_info, exam_indices)
        .links_info
    )
    lab_links_info = (
        filter_assignments_info(assignments_info, lab_indices)
        .links_info
    )

    # Test homework links
    for i, links in enumerate(homework_links_info):
        if i != 8:
            assert len(links) == 1
        else:
            assert len(links) == 3

    # Test exam links
    for links in exam_links_info:
        assert links == [(None, None)]

    # Test lab links
    assert len(lab_links_info[0]) == 5
    assert len(lab_links_info[2]) == 6
    assert lab_links_info[7] == [(None, None)]
