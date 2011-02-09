#!/usr/bin/python

"""Different please commands."""

from .base import Help, Update, Run
from . import problem

from .base import ALL_COMMANDS
ALL_COMMANDS.append(Help)
ALL_COMMANDS.append(Update)
ALL_COMMANDS.append(problem.Inspect)
ALL_COMMANDS.append(Run)
ALL_COMMANDS.append(problem.Statement) #why do we need to list a command both in a context and here?

__all__ = [Help, Update, problem]
