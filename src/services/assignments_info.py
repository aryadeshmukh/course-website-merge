'''This module contains definition for AssignmentInfo named tuple.'''

import collections

AssignmentsInfo = collections.namedtuple('AssignmentsInfo', [
    'assignment_courses',
    'assignment_types',
    'assignment_names',
    'due_dates',
    'links_info',
])
