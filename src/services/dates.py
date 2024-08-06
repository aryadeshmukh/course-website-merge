'''Module containing all date handling functions.'''

from datetime import date
import calendar
from services.constants import YEAR
from services.constants import MONTH_CODES

def convert_date_to_code(month: str, day: str) -> date:
    """Converts input month and day strings a date object.
    
    If month is invalid, None is returned.

    Args:
        month (str): month of date
        day (str): day of date

    Returns:
        date: date object representing input
    """
    try:
        month = month.lower()
        day = day.lower()[:2]
        if not day[-1].isdigit():
            day = day[0]
        month_code = MONTH_CODES[month[:3]]
        if len(day) < 2:
            day = f'0{day}'
        elif int(day) > calendar.monthrange(YEAR, int(month_code))[1]:
            day = f'0{day[0]}'
        return date.fromisoformat(f'{YEAR}-{month_code}-{day}')
    except Exception:
        return None

def convert_date_string(date_str: str) -> date:
    """Converts an input date string in the form 'Mon' to a date object.

    Args:
        date_str (str): date string to be converted

    Returns:
        date: date object representing input date string
    """
    try:
        date_components = date_str.split()
        month = date_components[0]
        day = date_components[1]
        return convert_date_to_code(month, day)
    except Exception:
        return None

def format_date_code(date_code: str) -> date:
    """Returns a date object corresponding to an incomplete date_code input.
    
    Args:
        date_code (str): incomplete date code

    Returns:
        date: date object corresponding to date in date_code
    """
    if '/' not in date_code:
        return None
    date_parts = date_code.split('/')
    month = date_parts[0]
    day = date_parts[1]
    if len(month) == 1:
        month = f'0{month}'
    if len(day) == 1:
        day =f'0{day}'
    return date.fromisoformat(f'{YEAR}-{month}-{day}')
