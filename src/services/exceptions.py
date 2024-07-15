'''Module containing all custom error classes.'''

class InvalidUsername(Exception):
    '''Error indicating bad username.'''

class InvalidCredentials(Exception):
    '''Error indicating username-password combination is incorrect.'''

class CourseAlreadySelected(Exception):
    '''Error indicating course is already in user's list.'''

class NoCourseSelected(Exception):
    '''Error indicating no course has been selected.'''
