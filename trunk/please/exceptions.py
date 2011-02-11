#!/usr/bin/python

"""Please exceptions."""

class PleaseError(Exception):
    pass


class UserInputError(PleaseError):
    def __init__(self, message, command):
        self.message = message
        if command is None:
            self.command = None
        elif isinstance(command, str):
            self.command = command
        else:
            self.command = command.NAMES[0]

class MalformedProblemError(PleaseError):
    def __init__(self, message):
        self.message = message

