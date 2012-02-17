from .matcher import Matcher

_matchers = {}
def get_matcher(name):
    if name not in _matchers:
        _matchers[name] = Matcher() # some day will be more sophisticated
    return matcher[name]

def init_please_matcher():
    m = get_matcher('please')
    from . import config
    for mod in config.modules:
        m.add_module(mod)
    return m

