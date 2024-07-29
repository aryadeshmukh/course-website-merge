'''This module contains scraper function for data8 course website.'''

from bs4 import BeautifulSoup
from services.assignments_info import AssignmentsInfo
from services.dates import format_date_code

def scrape_data8(website_text: str) -> AssignmentsInfo:
    """Returns scraped assignment information from data8 website.

    Args:
        website_text (str): html text for data8 course website

    Returns:
        AssignmentsInfo: named tuple containing scraped assignment information
    """
    course_code = 'DATAC8'

    soup = BeautifulSoup(website_text, 'html.parser')

    weeks = soup.find_all('div', class_='module')

    assignments_info = AssignmentsInfo([], [], [], [], [])

    for week in weeks:

        # Scraping homework information
        homework_strong = week.find('strong', class_='label label-homework')
        if homework_strong:
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
                assignments_info.due_dates.append(format_date_code(date_text))
                assignments_info.links_info.append([(
                    homework_link_tag['href'],
                    homework_link_tag.text)])

        # Scraping lab information
        lab_strong = week.find('strong', class_='label label-lab')
        if lab_strong:
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
                assignments_info.due_dates.append(format_date_code(date_text))
                assignments_info.links_info.append([(lab_link_tag['href'], lab_link_tag.text)])

        # Scraping project information
        project_strong = week.find('strong', class_='label label-project')
        if project_strong:
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
                assignments_info.due_dates.append(format_date_code(date_text))
                assignments_info.due_dates.append(format_date_code(date_text_checkpoint))
                assignments_info.links_info.append([(
                    project_link_tag['href'],
                    project_link_tag.text)])
                assignments_info.links_info.append([(
                    project_link_tag['href'],
                    project_link_tag.text)])

        # # Scraping exam information
        # exam_strong = week.find('strong', class_='label label-exam')
        # if exam_strong:
        #     assignment_courses.append(course_code)
        #     assignment_types.append('Exam')
        #     assignments.append(' '.join(exam_strong.parent.text.split()[1:]))
        #     due_dates.append(exam_strong.find_parent('dd').find_previous_sibling('dt').text)
        #     links_info.append([(None, None)])

    return assignments_info
