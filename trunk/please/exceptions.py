#!/usr/bin/python

"""Please exceptions."""

from . import locale

class PleaseError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message


class UserInputError(PleaseError):
    def __init__(self, message, command):
        if command:
           if not isinstance(command, str):
               command = command.NAMES[0]        
           self.message = locale.get('user-input-error').format(
                 message, command)
        else:
            self.message = locale.get('user-input-error-no-command').format(
                               message)

class MalformedProblemError(PleaseError):
    def __init__(self, message):
        self.message = locale.get('malformed-problem-error').format(message)

