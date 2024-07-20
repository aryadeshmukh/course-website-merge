'''Module containing all date handling functions.'''

def convert_date_to_code(month: str, day: str) -> str:
    """Converts input month and day strings into one date code in the form of mm/dd.
    
    If month is invalid, None is returned.

    Args:
        month (str): month of date
        day (str): day of date

    Returns:
        str: date code in the form of mm/dd
    """
    month_codes = {
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
    try:
        month = month.lower()
        day = day.lower()[:2]
        if not day[-1].isdigit():
            day = day[0]
        print(month, day)
        month_code = month_codes[month[:3]]
        if len(day) < 2:
            day = f'0{day}'
        return f'{month_code}/{day}'
    except Exception:
        return None

def date_comparator(date_code: str) -> int:
    """Returns unique number associated with date_code in the form of mm/dd.
    
    Intended to be used to sort by date. 0 is returned if date_code is invalid.

    Args:
        date_code (str): 5-digit date code in the form of mm/dd

    Returns:
        int: unique number associated with date_code
    """
    try:
        num_days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_num = int(date_code[:2])
        day = int(date_code[-2:])
        unique_code = 0
        for i in range(1, month_num):
            unique_code += num_days_in_month[i]
        return unique_code + day
    except Exception:
        return 0
