'''Module containing all custom error classes.'''

class InvalidUsername(Exception):
    '''Error indicating bad username.'''

class InvalidCredentials(Exception):
    '''Error indicating username-password combination is incorrect.'''
