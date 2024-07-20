'''Module containing all scraping handling functions.'''

import re
from typing import List, Tuple, Any, Iterable
from bs4 import BeautifulSoup
import requests
from services.dates import convert_date_to_code, date_comparator
from services.database import get_course_link

def get_first_text(element) -> str:
    """Returns only the first text in html elmenet

    Args:
        element (_type_): html element contents

    Returns:
        str: first text in html element
    """
    for item in element:
        if isinstance(item, str):
            return item.strip()
    return ""

def scrape_eecs16b() -> Tuple[
    List[str],
    List[str],
    List[str],
    List[str],
    List[List[Tuple[str]]]]:

    """Calls _scrape_eecs16b without test_link.

    Returns:
        Tuple[ List[str], List[str], List[str], List[str], List[List[Tuple[str]]]]:
        return value of _scrape_eecs16b with default test_link
    """
    return _scrape_eecs16b()

def _scrape_eecs16b(test_link: str=None) -> Tuple[
    List[str],
    List[str],
    List[str],
    List[str],
    List[List[Tuple[str]]]]:
    """Scrapes assignment information from eecs16b website.
    
    Returns a tuple containing information of all assignments for the class.

    Args:
        test_link (str): url hardcoded in for testing purposes

    Returns:
        Tuple[ List[str], List[str], List[str], List[str], List[List[Tuple[str, str]]]]:
        
        Tuple containing lists of assignment class, type, name, due_date, and all information
        regarding associated assignment links.
    """
    course_code = 'EECS16B'
    course_url = get_course_link(course_code) if not test_link else test_link

    response = requests.get(course_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weeks = soup.find_all('tbody', id=re.compile('week'))
        assignment_courses = []
        assignment_types = []
        assignments = []
        due_dates = []
        links_info = []
        for week in weeks:

            table_data = week.find('tr').find_all('td')

            # Scraping exam information
            exam_td = table_data[0]
            if exam_td.text and 'MT' in exam_td.text:
                assignment_courses.append(course_code)
                assignment_types.append('Exam')
                assignment_text = exam_td.text.split()
                assignments.append(' '.join(assignment_text[1:3])[:-1])
                due_dates.append(convert_date_to_code(assignment_text[3], assignment_text[4]))
                links_info.append([(None, None)])

            # Scraping homework information
            homework_td = table_data[-1]
            homework_links = homework_td.find_all('a')
            if homework_links:
                assignment_courses.append(course_code)
                assignment_types.append('Homework')
                assignment_text = homework_td.text.split()
                assignments.append(' '.join(assignment_text[:2]))
                due_dates.append(assignment_text[3])
                homework_links_info = []
                for link in homework_links:
                    homework_links_info.append((course_url + link['href'], link.text))
                if len(homework_links_info) == 0:
                    homework_links_info = [(None, None)]
                links_info.append(homework_links_info)

            # Scraping lab information
            lab_td = table_data[-2]
            lab_text = get_first_text(lab_td.contents)
            if lab_text[:3] == 'Lab':
                assignment_courses.append(course_code)
                assignment_types.append('Lab')
                assignments.append(lab_text)
                due_dates.append(table_data[1].text.split()[0])
                lab_links_info = []
                for link in lab_td.find_all('a'):
                    lab_links_info.append((link['href'], link.text))
                if len(lab_links_info) == 0:
                    lab_links_info = [(None, None)]
                links_info.append(lab_links_info)

        return (assignment_courses, assignment_types, assignments, due_dates, links_info)

def all_assignments_data(user_courses: list) -> iter:
    """Returns a zip of assignment information from all of user's selected courses.
    
    Assignments are sorted by closest approaching due date.

    Args:
        user_courses (list): list of courses user has selected

    Returns:
        iter: zip containing assignment information for all classes in user_courses
        sorted in order of closest approaching due date
    """
    assignment_courses, assignment_types, assignments, due_dates, links_info = scrape_eecs16b()
    return sorted(zip(assignment_courses, assignment_types, assignments, due_dates, links_info),
                    key=lambda assignment: date_comparator(assignment[3]))
