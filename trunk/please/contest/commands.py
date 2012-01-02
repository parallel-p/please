import os.path
import logging
from . import contest

CONTEST_FILE = "%s.contest"

def get_contest_config(name, path = '.'):
    return os.path.join(path, CONTEST_FILE % name)

def create_contest(name, problems):
    logger = logging.getLogger("please_logger.contest.contest_commands.create_contest")
    if os.path.exists(get_contest_config(name)):
        logger.error('Contest with config %s already exists' % get_contest_config(name))
        return
    if len(problems) >= 3 and problems[-2] == "as":
        ids = problems[-1].split(',')
        if len(set(ids)) != len(ids):
            # dublicate IDs
            logger.error('Your problem IDs definition contains duplicate names')
            return
        problems = zip(problems, ids)
    else:
        problems = zip(problems, [False] * len(problems))
    new_contest = contest.Contest(get_contest_config(name), ok_if_not_exists = True)

    for problem, id in problems:
        new_contest.problem_add(problem, id)
    with open(get_contest_config(name), 'w') as f:
        f.write(new_contest.config.get_text())
