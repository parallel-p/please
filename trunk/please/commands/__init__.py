#!/usr/bin/python

"""Different please commands."""

from .base import HelpCommand, UpdateCommand
from . import problem

from .base import ALL_COMMANDS
ALL_COMMANDS.append(HelpCommand)
ALL_COMMANDS.append(UpdateCommand)

__all__ = ALL_COMMANDS
