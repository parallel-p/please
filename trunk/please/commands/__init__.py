#!/usr/bin/python

"""Different please commands."""

from .base import Help, Update
from . import problem

from .base import ALL_COMMANDS
ALL_COMMANDS.append(Help)
ALL_COMMANDS.append(Update)
ALL_COMMANDS.append(problem.Inspect)

__all__ = [Help, Update, problem]
