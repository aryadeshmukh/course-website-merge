'''Module containing all constants.'''

import string
from datetime import datetime

# Database file containing user credentials
USERS_DB = 'databases/users.db'

# Database file containing course list
COURSES_DB = 'databases/courses.db'

# .sql file containing course list
COURSES_SQL = 'databases/courses.sql'

# Database file containing users' selected courses
USER_COURSES_DB = 'databases/user-courses.db'

# Database file containing users' assignment information
USER_ASSIGNMENTS_DB = 'databases/user-assignments.db'

# Database file containing user's previous updates
UPDATES_DB = 'databases/updates.db'

# String containing alphabet
ALPHABET = string.ascii_letters + string.digits + string.punctuation

# Current year
YEAR = datetime.now().year

# Translations from month labels to numbers
MONTH_CODES = {
    'jan' : '01',
    'feb' : '02',
    'mar' : '03',
    'apr' : '04',
    'may' : '05',
    'jun' : '06',
    'jul' : '07',
    'aug' : '08',
    'sep' : '09',
    'oct' : '10',
    'nov' : '11',
    'dec' : '12'
}

# Number of seconds to scrape before timeout has been reached
SCRAPE_TIMEOUT = 10
