'''This module contains scraper function for eecs16b course website.'''

import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from services.assignments_info import AssignmentsInfo
from services.dates import convert_date_to_code, format_date_code
from services.database import get_course_link

def get_first_text(element) -> str:
    """Returns only the first text in html elmenet

    Args:
        element (Tag): html element contents

    Returns:
        str: first text in html element
    """
    for item in element:
        if isinstance(item, str):
            return item.strip()
    return ""

def scrape_homework_info(
    table_data: list,
    curr_date: date,
    assigned_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str,
    course_url: str) -> date:
    """Scrapes homework information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        table_data (list): list of tags containing information to be extracted
        curr_date (date): current date
        assigned_date (date): date the homework would have been assigned
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
        course_url (str): course url

    Returns:
        date: date that homework would be due
    """
    hw_due_date = None
    homework_td = table_data[-1]
    homework_links = homework_td.find_all('a')
    if homework_links and assigned_date <= curr_date:
        assignments_info.assignment_courses.append(course_code)
        assignments_info.assignment_types.append('Homework')
        assignment_text = homework_td.text.split()
        assignments_info.assignment_names.append(' '.join(assignment_text[:2]))
        hw_due_date = format_date_code(assignment_text[3]).isoformat()
        assignments_info.due_dates.append(hw_due_date)
        homework_links_info = []
        for link in homework_links:
            homework_links_info.append((course_url + link['href'], link.text))
        if len(homework_links_info) == 0:
            homework_links_info = [(None, None)]
        assignments_info.links_info.append(homework_links_info)
    return hw_due_date

def scrape_lab_info(
    table_data: list,
    curr_date: date,
    assigned_date: date,
    due_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes lab information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        table_data (list): list of tags containing information to be extracted
        curr_date (date): current date
        assigned_date (date): date the lab would have been assigned
        due_date (date): due date of lab assignments
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    lab_td = table_data[-2]
    lab_text = get_first_text(lab_td.contents)
    if lab_text[:3] == 'Lab' and assigned_date <= curr_date:
        assignments_info.assignment_courses.append(course_code)
        assignments_info.assignment_types.append('Lab')
        assignments_info.assignment_names.append(lab_text)
        assignments_info.due_dates.append(due_date)
        lab_links_info = []
        for link in lab_td.find_all('a'):
            lab_links_info.append((link['href'], link.text))
        if len(lab_links_info) == 0:
            lab_links_info = [(None, None)]
        assignments_info.links_info.append(lab_links_info)

def scrape_exam_info(table_data: list, assignments_info: AssignmentsInfo, course_code: str) -> None:
    """Scrapes exam information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        table_data (list): list of tags containing information to be extracted
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    exam_td = table_data[0]
    if exam_td.text and 'MT' in exam_td.text:
        assignments_info.assignment_courses.append(course_code)
        assignments_info.assignment_types.append('Exam')
        assignment_text = exam_td.text.split()
        assignments_info.assignment_names.append(' '.join(assignment_text[1:3])[:-1])
        assignments_info.due_dates.append(convert_date_to_code(
            assignment_text[3],
            assignment_text[4]).isoformat())
        assignments_info.links_info.append([(None, None)])

def scrape_eecs16b(website_text: str, curr_date: date) -> AssignmentsInfo:
    """Returns scraped assignment information from eecs16b website.

    Args:
        website_text (str): html text for eecs16b course website
        curr_date (date): upper bound assign date for assignments to be scraped

    Returns:
        AssignmentsInfo: named tuple containing scraped assignment information
    """
    course_code = 'EECS16B'
    course_url = get_course_link(course_code) or ''

    soup = BeautifulSoup(website_text, 'html.parser')
    weeks = soup.find_all('tbody', id=re.compile('week'))

    assignments_info = AssignmentsInfo([], [], [], [], [])

    for week in weeks:

        table_data = week.find('tr').find_all('td')

        # Exit loop if assignments have not been assigned yet
        date_td = table_data[1]
        assigned_date = format_date_code(date_td.text.split()[0])
        if assigned_date - timedelta(weeks=1) > curr_date:
            break

        scrape_exam_info(table_data, assignments_info, course_code)
        hw_due_date = scrape_homework_info(
            table_data, curr_date, assigned_date, assignments_info, course_code, course_url)
        scrape_lab_info(
            table_data, curr_date, assigned_date, hw_due_date, assignments_info, course_code)

    return assignments_info
