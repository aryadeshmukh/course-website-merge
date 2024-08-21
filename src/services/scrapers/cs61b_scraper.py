'''This module contains scraper function for cs61b course website.'''

import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from services.database import get_course_link
from services.dates import convert_date_to_code, format_date_code
from services.assignments_info import AssignmentsInfo

def scrape_homework_info(
    row,
    curr_date: date,
    assigned_date: date,
    prev_scrape_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str,
    course_url: str) -> None:
    """Scrapes homework information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        row (Tag): tag containing information about to be extracted
        curr_date (date): current date
        assigned_date (date): date the homework would have been assigned
        prev_scrape_date (date): date of previous assignment scrape
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
        course_url (str): course url
    """
    homework_td = row.find('td', class_='homework')
    if (homework_td and
        assigned_date <= curr_date and
        (not prev_scrape_date or prev_scrape_date < assigned_date)):
        homework_a_tag = homework_td.find('a')
        if homework_a_tag:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Homework')
            assignments_info.assignment_names.append(homework_a_tag.text)
            assignments_info.due_dates.append(
                format_date_code(homework_td.text.split()[3][:-1]).isoformat())
            link = homework_a_tag['href']
            link_prefix = '' if 'gradescope' in link else course_url
            assignments_info.links_info.append([(link_prefix + link, homework_a_tag.text)])

def scrape_project_info(
    row,
    curr_date: date,
    assigned_date: date,
    prev_scrape_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str,
    course_url: str) -> None:
    """Scrapes project information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        row (Tag): tag containing information about to be extracted
        curr_date (date): current date
        assigned_date (date): date the project would have been assigned
        prev_scrape_date (date): date of previous assignment scrape
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
        course_url (str): course url
    """
    project_td = row.find('td', class_='project')
    if (project_td and
        assigned_date <= curr_date and
        (not prev_scrape_date or prev_scrape_date < assigned_date)):
        project_a_tags = project_td.find_all('a')
        for project_a_tag in project_a_tags:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Project')
            if '/' in project_td.text:
                assignments_info.assignment_names.append(
                    project_a_tag.text + project_a_tags[-1].next_sibling.text)
            else:
                assignments_info.assignment_names.append(project_a_tag.text)
            if 'Project' not in assignments_info.assignment_names[-1]:
                labeled_project_name = f'Project {assignments_info.assignment_names[-1]}'
                assignments_info.assignment_names[-1] = labeled_project_name
            assignments_info.due_dates.append(
                format_date_code(project_td.text.split()[-1][:-1])
                .isoformat())
            link = project_a_tag['href']
            assignments_info.links_info.append([(
                course_url + link,
                assignments_info.assignment_names[-1])])

def scrape_lab_info(
    row,
    curr_date: date,
    assigned_date: date,
    prev_scrape_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str,
    course_url: str) -> None:
    """Scrapes lab information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        row (Tag): tag containing information about to be extracted
        curr_date (date): current date
        assigned_date (date): date the lab would have been assigned
        prev_scrape_date (date): date of previous assignment scrape
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
        course_url (str): course url
    """
    lab_td = row.find(lambda tag: tag.name == 'td' and 'Lab' in tag.text)
    if (lab_td and
        assigned_date <= curr_date and
        (not prev_scrape_date or prev_scrape_date < assigned_date)):
        first_a_tag = lab_td.find('a')
        if first_a_tag:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Lab')
            assignments_info.assignment_names.append(first_a_tag.text)
            due_date = re.search(r'\(due (\d+/\d+)\)', lab_td.text)
            if due_date:
                assignments_info.due_dates.append(
                    format_date_code(due_date.group(1)).isoformat())
            else:
                assignments_info.due_dates.append('')
            lab_links_info = []
            for lab_a_tag in lab_td.find_all('a'):
                link_prefix = '' if 'http' in lab_a_tag['href'] else course_url
                lab_links_info.append((link_prefix + lab_a_tag['href'], lab_a_tag.text))
            assignments_info.links_info.append(lab_links_info)

def scrape_exam_info(
    row,
    prev_scrape_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes exam information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        row (Tag): tag containing information about to be extracted
        prev_scrape_date (date): date of previous assignment scrape
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    exam_strong = row.find('strong')
    if exam_strong and 'Midterm' in exam_strong.text:
        date_text = row.find('td', class_='border-hack').text.split()[-2:]
        exam_date = convert_date_to_code(date_text[0][-3:], date_text[1])
        if not prev_scrape_date or prev_scrape_date + timedelta(weeks=1) < exam_date:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Exam')
            assignments_info.assignment_names.append(exam_strong.text)
            date_text = row.find('td', class_='border-hack').text.split()[-2:]
            assignments_info.due_dates.append(exam_date.isoformat())
            assignments_info.links_info.append([(None, None)])

def scrape_cs61b(website_text: str, curr_date: date, prev_scrape_date: date) -> AssignmentsInfo:
    """Returns scraped assignment information from cs61b website.

    Args:
        website_text (str): html text for cs61b course website
        curr_date (date): upper bound assign date for assignments to be scraped
        prev_scrape_date (date): lower bound assign date for assignments to be scraped
        None if first time scraping

    Returns:
        AssignmentsInfo: named tuple containing scraped assignment information
    """
    course_code = 'COMPSCI61B'
    course_url = get_course_link(course_code) or ''

    soup = BeautifulSoup(website_text, 'html.parser')
    rows = soup.find_all('tr')

    assignments_info = AssignmentsInfo([], [], [], [], [])

    for row in rows:

        # Exit loop if assignments have not been assigned yet
        date_td = row.find('td', class_=re.compile('border-hack'))
        if date_td:
            date_text = date_td.text.split()
            assigned_date = convert_date_to_code(date_text[0][-3:], date_text[1])
            if assigned_date - timedelta(weeks=1) > curr_date:
                break
            if prev_scrape_date and assigned_date + timedelta(weeks=1) <= prev_scrape_date:
                continue
        else:
            continue

        scrape_homework_info(
            row,
            curr_date,
            assigned_date,
            prev_scrape_date,
            assignments_info,
            course_code,
            course_url)
        scrape_project_info(
            row,
            curr_date,
            assigned_date,
            prev_scrape_date,
            assignments_info,
            course_code,
            course_url)
        scrape_lab_info(
            row,
            curr_date,
            assigned_date,
            prev_scrape_date,
            assignments_info,
            course_code,
            course_url)
        scrape_exam_info(row, prev_scrape_date, assignments_info, course_code)

    return assignments_info
