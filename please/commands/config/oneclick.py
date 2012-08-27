def clean():
    '''clean|clear
       Cleans all temporary files
    '''
    from please.cleaner import cleaner
    cleaner.Cleaner().cleanup

def build():
    '''build [all]
       Generate all tests, validate them and test all solutions
    '''
    from please.build_all.build_tools import build_all
    build_all()
