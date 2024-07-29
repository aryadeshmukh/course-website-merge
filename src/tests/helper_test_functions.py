'''This module contains helper functions for testing.'''

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.assignments_info import AssignmentsInfo

def filter_assignments_info(assignments_info: AssignmentsInfo, indices: list):
    '''Filters assignments_info to only contain assignments corresponding to those in indices.'''
    filtered_assignments_info = AssignmentsInfo(
        [assignments_info.assignment_courses[i] for i in indices],
        [assignments_info.assignment_types[i] for i in indices],
        [assignments_info.assignment_names[i] for i in indices],
        [assignments_info.due_dates[i] for i in indices],
        [assignments_info.links_info[i] for i in indices])
    return filtered_assignments_info
