import platform

def get_platform():
    '''
    Return tuple (os, bit), where os is 'Windows', 'Linux' or 'Darwin' and
    bit is '32' or '64'
    '''
    os = platform.system()
    bit = platform.architecture()[0]
    if not os in ['Windows', 'Linux', 'Darwin'] or not bit in ['32bit', '64bit']:
        raise Exception("unsupported platform: {0} {1}".format(os, bit))
    return (os, bit[:2])
