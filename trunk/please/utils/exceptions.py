import traceback
from .. import globalconfig

class PleaseException(Exception):
    def __init__(self, *args):
        super(PleaseException, self).__init__(args)
        if globalconfig.DEBUG_MODE:
            traceback.print_stack()        
        
class MatcherException(Exception):
    pass
