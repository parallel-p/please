from .matcher import Matcher

_matchers = {}
def get_matcher(name):
    if name not in _matchers:
        _matchers[name] = Matcher() # some day will be more sophisticated
    return _matchers[name]

def get_please_matcher():
    m = get_matcher('please')
    if not hasattr(m, '_loaded'):
        from . import config
        for mod in config.modules:
            m.add_module(mod)
        m._loaded = True
    return m

