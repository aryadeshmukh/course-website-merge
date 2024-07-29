'''Module containing all assignment data handling functions.'''

import requests
from services.database import get_course_link
from services.scrapers.eecs16b_scraper import scrape_eecs16b
from services.scrapers.cs61b_scraper import scrape_cs61b
from services.scrapers.data8_scraper import scrape_data8
from services.assignments_info import AssignmentsInfo
from services.dates import date_comparator

# map containing course and its scrape function pairs
SCRAPE_FUNCS = {
    'EECS16B' : scrape_eecs16b,
    'COMPSCI61B' : scrape_cs61b,
    'DATAC8' : scrape_data8
}

def all_assignments_data(user_courses: list) -> iter:
    """Returns a zip of assignment information from all of user's selected courses.
    
    Assignments are sorted by closest approaching due date.

    Args:
        user_courses (list): list of courses user has selected

    Returns:
        iter: zip containing assignment information for all classes in user_courses
        sorted in order of closest approaching due date
    """
    all_assignments_info = AssignmentsInfo([], [], [], [], [])

    for course_code in user_courses:
        course_url = get_course_link(course_code)
        response = requests.get(course_url)
        if response.status_code == 200:
            course_assignments_info = SCRAPE_FUNCS[course_code](response.text)
            for i, _ in enumerate(all_assignments_info):
                all_assignments_info[i].extend(course_assignments_info[i])
    return sorted(zip(
        all_assignments_info.assignment_courses,
        all_assignments_info.assignment_types,
        all_assignments_info.assignment_names,
        all_assignments_info.due_dates,
        all_assignments_info.links_info),
                  key=lambda assignment: date_comparator(assignment[3]))
