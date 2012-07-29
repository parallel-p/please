# I'm really not that much into it.
# SOmebody, wirte an appropriate documentation.
def import_polygon_contest(name):
    '''import polygon contest $name
    Import a contest from Polygon.'''
    from please.import_from_polygon import create_contest
    create_contest(name)
    # TODO: ensure it is well-written.

def import_polygon_problem(problem, contest):
    '''import polygon problem $problem from $contest
    Import a problem from Polygon contest.'''
    from please.import_from_polygon import import_problem_from_polygon
    import_problem_from_polygon(contest_id = contest,
                                problem_letter = problem)

def import_polygon_package(package):
    '''import polygon package $package
    Import a package from Polygon.'''
    from please.import_from_polygon import create_problem
    create_problem(package)
