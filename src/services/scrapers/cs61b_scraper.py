'''This module contains scraper function for cs61b course website.'''

import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from services.database import get_course_link
from services.dates import convert_date_to_code, format_date_code
from services.assignments_info import AssignmentsInfo

def scrape_cs61b(website_text: str, curr_date: date) -> AssignmentsInfo:
    """Returns scraped assignment information from cs61b website.

    Args:
        website_text (str): html text for cs61b course website
        curr_date (date): upper bound assign date for assignments to be scraped

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
        else:
            continue

        # Scraping homework information
        homework_td = row.find('td', class_='homework')
        if homework_td and assigned_date <= curr_date:
            homework_a_tag = homework_td.find('a')
            if homework_a_tag:
                assignments_info.assignment_courses.append(course_code)
                assignments_info.assignment_types.append('Homework')
                assignments_info.assignment_names.append(homework_a_tag.text)
                assignments_info.due_dates.append(
                    format_date_code(homework_td.text.split()[3][:-1]))
                link = homework_a_tag['href']
                link_prefix = '' if 'gradescope' in link else course_url
                assignments_info.links_info.append([(link_prefix + link, homework_a_tag.text)])

        # Scraping project information
        project_td = row.find('td', class_='project')
        if project_td and assigned_date <= curr_date:
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
                    format_date_code(project_td.text.split()[-1][:-1]))
                link = project_a_tag['href']
                assignments_info.links_info.append([(
                    course_url + link,
                    assignments_info.assignment_names[-1])])

        # Scraping lab information
        lab_td = row.find(lambda tag: tag.name == 'td' and 'Lab' in tag.text)
        if lab_td and assigned_date <= curr_date:
            first_a_tag = lab_td.find('a')
            if first_a_tag:
                assignments_info.assignment_courses.append(course_code)
                assignments_info.assignment_types.append('Lab')
                assignments_info.assignment_names.append(first_a_tag.text)
                due_date = re.search(r'\(due (\d+/\d+)\)', lab_td.text)
                if due_date:
                    assignments_info.due_dates.append(format_date_code(due_date.group(1)))
                else:
                    assignments_info.due_dates.append('')
                lab_links_info = []
                for lab_a_tag in lab_td.find_all('a'):
                    link_prefix = '' if 'http' in lab_a_tag['href'] else course_url
                    lab_links_info.append((link_prefix + lab_a_tag['href'], lab_a_tag.text))
                assignments_info.links_info.append(lab_links_info)

        # Scraping exam information
        exam_strong = row.find('strong')
        if exam_strong and 'Midterm' in exam_strong.text:
            assignments_info.assignment_courses.append(course_code)
            assignments_info.assignment_types.append('Exam')
            assignments_info.assignment_names.append(exam_strong.text)
            date_text = row.find('td', class_='border-hack').text.split()[-2:]
            assignments_info.due_dates.append(convert_date_to_code(date_text[0][-3:], date_text[1]))
            assignments_info.links_info.append([(None, None)])

    return assignments_info
