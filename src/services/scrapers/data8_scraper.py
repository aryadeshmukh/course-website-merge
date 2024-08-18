'''This module contains scraper function for data8 course website.'''

import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from services.assignments_info import AssignmentsInfo
from services.dates import format_date_code, convert_date_string

def scrape_homework_info(
    week,
    curr_date: date,
    hw_assign_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes homework information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        week (Tag): tag containing information about to be extracted
        curr_date (date): current date
        hw_assign_date (date): date the homework would have been assigned
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    homework_strong = week.find('strong', class_='label label-homework')
    if homework_strong and hw_assign_date <= curr_date:
        homework_link_tag = homework_strong.parent.find('a')
        if homework_link_tag:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Homework')
            assignments_info.assignment_names.append(homework_link_tag.text)
            homework_text = homework_strong.parent.text
            if 'Due' in homework_text:
                date_text = homework_text.split()[-1][:-1]
            else:
                date_text = homework_text.split()[-1][1:-1]
            assignments_info.due_dates.append(
                format_date_code(date_text).isoformat())
            assignments_info.links_info.append([(
                homework_link_tag['href'],
                homework_link_tag.text)])

def scrape_lab_info(
    week,
    curr_date: date,
    lab_assign_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes lab information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        week (Tag): tag containing information about to be extracted
        curr_date (date): current date
        lab_assign_date (date): date the lab would have been assigned
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    lab_strong = week.find('strong', class_='label label-lab')
    if lab_strong and lab_assign_date <= curr_date:
        lab_link_tag = lab_strong.parent.find('a')
        if lab_link_tag:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Lab')
            assignments_info.assignment_names.append(lab_link_tag.text)
            lab_text = lab_strong.parent.text
            if 'Due' in lab_text:
                date_text = lab_text.split()[-3][:-4]
            else:
                date_text = lab_text.split()[-3][1:-4]
            date_code = format_date_code(date_text)
            due_date_string = (date_code and date_code.isoformat()) or ''
            assignments_info.due_dates.append(due_date_string)
            assignments_info.links_info.append([(lab_link_tag['href'], lab_link_tag.text)])

def scrape_project_info(
    week,
    curr_date: date,
    project_assign_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes project information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        week (Tag): tag containing information about to be extracted
        curr_date (date): current date
        project_assign_date (date): date the project would have been assigned
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    project_strong = week.find('strong', class_='label label-project')
    if project_strong and project_assign_date <= curr_date:
        project_link_tag = project_strong.parent.find('a')
        if project_link_tag:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Project')
            assignments_info.assignment_types.append('Project')
            assignments_info.assignment_names.append(project_link_tag.text)
            assignments_info.assignment_names.append(project_link_tag.text + ' Checkpoint')
            project_text = project_strong.parent.text
            if 'Due' in project_text:
                date_text = project_text.split()[-3][:-1]
            else:
                date_text = project_text.split()[-3][1:-1]
            date_text_checkpoint = project_text.split()[-1][:-1]
            assignments_info.due_dates.append(format_date_code(date_text).isoformat())
            assignments_info.due_dates.append(
                format_date_code(date_text_checkpoint).isoformat())
            assignments_info.links_info.append([(
                project_link_tag['href'],
                project_link_tag.text)])
            assignments_info.links_info.append([(
                project_link_tag['href'],
                project_link_tag.text)])

def scrape_exam_info(
    week,
    exam_assign_date: date,
    assignments_info: AssignmentsInfo,
    course_code: str) -> None:
    """Scrapes exam information from the input row and updates assignments_info to contain
    the new assignment.

    Args:
        week (Tag): tag containing information about to be extracted
        exam_assign_date (date): date the exam would have been assigned
        assignments_info (AssignmentsInfo): AssignmentsInfo tuple to be updated with new assignment
        course_code (str): course code
    """
    exam_strong = week.find('strong', class_='label label-exam')
    if exam_strong and 'Midterm' in exam_strong.parent.text:
        assignments_info.assignment_courses.append(course_code)
        assignments_info.assignment_types.append('Exam')
        assignments_info.assignment_names.append(' '.join(exam_strong.parent.text.split()[1:]))
        assignments_info.due_dates.append(exam_assign_date.isoformat())
        assignments_info.links_info.append([(None, None)])

def scrape_data8(website_text: str, curr_date: date) -> AssignmentsInfo:
    """Returns scraped assignment information from data8 website.

    Args:
        website_text (str): html text for data8 course website
        curr_date (date): upper bound assign date for assignments to be scraped

    Returns:
        AssignmentsInfo: named tuple containing scraped assignment information
    """
    course_code = 'DATAC8'

    soup = BeautifulSoup(website_text, 'html.parser')

    weeks = soup.find_all('div', class_='module')

    assignments_info = AssignmentsInfo([], [], [], [], [])

    for week in weeks:

        # Exit loop if assignments have not been assigned yet
        dl_tag = week.find('dl')
        if dl_tag:
            dates = re.findall(
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}',
                dl_tag.text)
            if len(dates) > 0 and dates[0] == 'Apr 12':
                dates[0] = 'Apr 1'
            if len(dates) > 0 and dates[-1] == 'Mar 11':
                dates[-1] = 'Mar 1'
            if len(dates) > 0 and dates[-1] == 'Feb 28':
                dates[-1] = 'Feb 2'
            converted_dates = [convert_date_string(day) for day in dates]
            if len(converted_dates) >= 2:
                lab_assign_date = converted_dates[0]
                hw_assign_date = converted_dates[-1]
                if lab_assign_date - timedelta(weeks=1) > curr_date:
                    break
            else:
                continue
        else:
            continue

        scrape_homework_info(week, curr_date, hw_assign_date, assignments_info, course_code)
        scrape_lab_info(week, curr_date, lab_assign_date, assignments_info, course_code)
        scrape_project_info(week, curr_date, hw_assign_date, assignments_info, course_code)
        scrape_exam_info(week, hw_assign_date, assignments_info, course_code)

    return assignments_info
