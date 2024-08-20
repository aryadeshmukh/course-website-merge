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

MID_DATE = date(YEAR, 3, 1)

@pytest.fixture(scope='module')
def assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing DATAC8 assignment information.

    Returns:
        AssignmentInfo: AssignmentInfo object containing DATAC8 assignment information.
    """
    end_date = date(YEAR, 5, 8)
    with open('course_websites/data8_full.txt', 'r', encoding='utf-8') as file:
        return scrape_data8(file.read(), end_date, None)

@pytest.fixture
def dated_assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing DATAC8 assignment information up to a certain date.

    Returns:
        AssignmentInfo: AssignmentInfo object containing DATAC8 assignment information.
    """
    with open('course_websites/data8_full.txt', 'r', encoding='utf-8') as file:
        return scrape_data8(file.read(), MID_DATE, None)

@pytest.fixture
def in_between_assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing DATAC8 assignment information up to a certain date
    and following a previous scraping.

    Returns:
        AssignmentInfo: AssignmentInfo object containing DATAC8 assignment information.
    """
    farther_date = date(YEAR, 3, 15)
    with open('course_websites/data8_full.txt', 'r', encoding='utf-8') as file:
        return scrape_data8(file.read(), farther_date, MID_DATE)

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

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 1, 'Homework'),
    ('Lab', 1, 'Lab'),
    ('Project', 0, 'Project'),
    ('Exam', 0, 'Midterm')
])
def test_in_between_assignment_scraping(
    in_between_assignments_info: AssignmentsInfo,
    assignment_type: str,
    num_assignments: int,
    assignment_type_indicator: str):
    '''Tests correct scraping of all in scope assignment data assigned after previous scraping.'''
    assignment_type_indices = []
    for i, type_ in enumerate(in_between_assignments_info.assignment_types):
        if type_ == assignment_type:
            assignment_type_indices.append(i)

    # Test that all assignments were scraped
    assert len(assignment_type_indices) == num_assignments

    filtered_assignments_info = filter_assignments_info(
        in_between_assignments_info,
        assignment_type_indices)

    # Test that selected assignments are of correct type
    for assignment in filtered_assignments_info.assignment_names:
        assert assignment_type_indicator in assignment

def test_assignment_links_scraping(assignments_info: AssignmentsInfo):
    '''Tests correct scraping of all link assignment data.'''
    for links in assignments_info.links_info:
        assert len(links) == 1
