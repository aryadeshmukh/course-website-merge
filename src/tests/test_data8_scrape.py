'''This module tests scraping assignment information from COMPSCI61B course website.'''

from datetime import date
import sys
import os
import pytest
from helper_test_functions import filter_assignments_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.assignments_info import AssignmentsInfo
from services.scrapers.data8_scraper import scrape_data8
from services.constants import YEAR

@pytest.fixture(scope='module')
def assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing EECS16B assignment information.

    Returns:
        AssignmentInfo: AssignmentInfo object containing EECS16B assignment information.
    """
    end_date = date(YEAR, 5, 8)
    with open('course_websites/data8_full.txt', 'r', encoding='utf-8') as file:
        return scrape_data8(file.read(), end_date)

@pytest.fixture
def dated_assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing EECS16B assignment information up to a certain date.

    Returns:
        AssignmentInfo: AssignmentInfo object containing EECS16B assignment information.
    """
    mid_date = date(YEAR, 3, 1)
    with open('course_websites/data8_full.txt', 'r', encoding='utf-8') as file:
        return scrape_data8(file.read(), mid_date)

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 13, 'Homework'),
    ('Lab', 10, 'Lab'),
    ('Project', 6, 'Project'),
    ('Exam', 1, 'Midterm')
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

    # Test that all assignments are DATAc8 assignments
    for course in filtered_assignments_info.assignment_courses:
        assert course == 'DATAC8'

    # Test that selected assignments are of correct type
    for assignment in filtered_assignments_info.assignment_names:
        assert assignment_type_indicator in assignment

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 7, 'Homework'),
    ('Lab', 6, 'Lab'),
    ('Project', 2, 'Project'),
    ('Exam', 1, 'Midterm')
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
    for links in assignments_info.links_info:
        assert len(links) == 1
