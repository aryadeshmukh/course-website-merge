'''Module containing all assignment data handling functions.'''

from datetime import date
import requests
from services.database import get_course_link
from services.database import get_pending_assignments, get_completed_assignments
from services.scrapers.eecs16b_scraper import scrape_eecs16b
from services.scrapers.cs61b_scraper import scrape_cs61b
from services.scrapers.data8_scraper import scrape_data8
from services.constants import SCRAPE_TIMEOUT

# map containing course and its scrape function pairs
SCRAPE_FUNCS = {
    'EECS16B' : scrape_eecs16b,
    'COMPSCI61B' : scrape_cs61b,
    'DATAC8' : scrape_data8
}

# map containing course and its test file pairs
TEST_FILES = {
    'EECS16B' : 'course_websites/eecs16b_full.txt',
    'COMPSCI61B' : 'course_websites/cs61b_full.txt',
    'DATAC8' : 'course_websites/data8_full.txt'
}

def course_assignment_data(course_code: str, curr_date: date, test: bool=False) -> list:
    """Returns a zipped list of all in scope assignment information from selected course.

    Args:
        course_code (str): course code of selectec course
        curr_date (date): date for assignments in scope
        test (bool): indicates whether this function is being used for testing purposes

    Returns:
        list: zipped list of all assignment information
    """
    try:
        if test:
            with open(TEST_FILES[course_code], 'r', encoding='utf-8') as file:
                assignments_info = SCRAPE_FUNCS[course_code](file.read(), curr_date)
        else:
            course_url = get_course_link(course_code)
            response = requests.get(course_url, timeout=SCRAPE_TIMEOUT)
            if response.status_code == 200:
                assignments_info = SCRAPE_FUNCS[course_code](response.text, curr_date)
        return list(zip(
            assignments_info.assignment_courses,
            assignments_info.assignment_types,
            assignments_info.assignment_names,
            assignments_info.due_dates,
            assignments_info.links_info
        ))
    except TimeoutError:
        return list(zip([], [], [], [], []))

def all_pending_assignments(username: str) -> list:
    """Returns a list of assignment information for all of user's pending assignments.
    
    Assignments are sorted by closest approaching due date.

    Args:
        username (str): username of user

    Returns:
        list: sorted list containing assignment information for all pending assignments
    """
    pending_assignments = get_pending_assignments(username)
    pending_assignments_list = []
    for course in pending_assignments:
        pending_assignments_list.extend(pending_assignments[course])
    return sorted(pending_assignments_list, key=lambda assignment: assignment[3])

def all_completed_assignments(username: str) -> list:
    """Returns a list of assignment information for all of user's completed assignments.
    
    Assignments are sorted by furthest approaching due date.

    Args:
        username (str): username of user

    Returns:
        list: sorted list containing assignment information for all completed assignments.
    """
    completed_assignments = get_completed_assignments(username)
    completed_assignments_list = []
    for course in completed_assignments:
        completed_assignments_list.extend(completed_assignments[course])
    return sorted(completed_assignments_list, key=lambda assignment: assignment[3], reverse=True)
