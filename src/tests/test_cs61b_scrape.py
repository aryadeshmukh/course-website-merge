'''This module tests scraping assignment information from COMPSCI61B course website.'''

import sys
import os
import pytest
from helper_test_functions import filter_assignments_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.assignments_info import AssignmentsInfo
from services.scrapers.cs61b_scraper import scrape_cs61b
from services.dates import date_comparator

@pytest.fixture(scope='module')
def assignments_info() -> AssignmentsInfo:
    """Returns AssignmentInfo object containing EECS16B assignment information.

    Returns:
        AssignmentInfo: AssignmentInfo object containing EECS16B assignment information.
    """
    with open('course_websites/cs61b_full.txt', 'r', encoding='utf-8') as file:
        return scrape_cs61b(file.read())

@pytest.mark.parametrize('assignment_type, num_assignments, assignment_type_indicator', [
    ('Homework', 6, 'Homework'),
    ('Exam', 3, ' '),
    ('Lab', 10, 'Lab'),
    ('Project', 11, 'Project')
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

    # Test that all assignments are COMPSCI61B assignments
    for course in filtered_assignments_info.assignment_courses:
        assert course == 'COMPSCI61B'

    # Test that selected assignments are of correct type
    for assignment in filtered_assignments_info.assignment_names:
        assert assignment_type_indicator in assignment

def test_assignment_links_scraping(assignments_info: AssignmentsInfo):
    '''Tests correct scraping of all link assignment data.'''
    homework_indices = []
    exam_indices = []
    lab_indices = []
    project_indices = []
    for i, type_ in enumerate(assignments_info.assignment_types):
        if type_ == 'Homework':
            homework_indices.append(i)
        elif type_ == 'Exam':
            exam_indices.append(i)
        elif type_ == 'Project':
            project_indices.append(i)
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
    project_links_info = (
        filter_assignments_info(assignments_info, project_indices)
        .links_info
    )

    # Test homework links
    for links in homework_links_info:
        assert len(links) == 1

    # Test exam links
    for links in exam_links_info:
        assert links == [(None, None)]
    
    # Test project links
    for links in project_links_info:
        assert len(links) == 1

    # Test lab links
    assert len(lab_links_info[0]) == 2
    assert len(lab_links_info[6]) == 3
    assert len(lab_links_info[9]) == 2
