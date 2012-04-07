import traceback
from .. import globalconfig

class PleaseException(Exception):
    def __init__(self, msg):
        super(PleaseException, self).__init__(msg)
        if globalconfig.DEBUG_MODE:
            traceback.print_stack()        
        
class MatcherException(Exception):
    pass
