#include petrosyan.jpg

def ultimate_goal(sudo = False):
    '''tell me your ultimate goal
    !suppress'''
    print('Our ultimate goal is to help you in writing contests.')
    if not sudo:
        return
    print('Just kidding.')
    print('Our ultimate goal is to take over the world.')

def echo(args):
    '''echo args...
    !suppress'''
    import sys
    print("I'm not really unix shell, but you asked politely enough.", file = sys.stderr)
    end = '\n'
    if args[0] == '-n':
        args.pop(0)
        end = ''
    print(*args, end=end)

def take_over_the_world(sudo = False):
    '''take over the world
    !suppress'''
    import time
    import random
    from please.log import logger
    from sys import stdout
    random_junk = [
        'Measuring world temperature',
        'Checking if math is true',
        'Using hyperspace to extend CPU number',
        'Connecting to Skynet for further instructions',
        'Proving M-theory',
        'Using Riemann hypothesis',
        'Proving null hypothesis',
        'Finishing GNU/Hurd',
        'Writing random junk on the screen',
        'Catching them all',
        'Loafing around',
        'Being stared by abyss',
    ]
    howmuch = random.randint(10, 12)
    l = len(random_junk)
    idx = random.randrange(l)
    for i in range(howmuch):
        logger.info(random_junk[idx])
        doit = True
        while doit:
            time.sleep(random.random())
            doit = random.random() < 0.05
            if doit:
                logger.warning('... taking longer than expected ...')
        idx = idx2
        while idx == idx2 or idx2 < idx - 1 or idx2 > idx + 4:
            idx2 = random.randrange(l)
    if not sudo:
        logger.error('Not enough permissions to save data.')
        logger.error('Failed.')
    else:
        logger.info('Finishing...')
        time.sleep(2)
        logger.warning('Strange activity detected!')
        time.sleep(1)
        logger.info('Finishing will require 1 + 1/2 + 1/4 + ... seconds.')
        logger.info('Please wait...')
        t = 1.0
        while True:
            stdout.write('.')
            stdout.flush()
            time.sleep(t)
            t /= 2

def sudo(args):
    '''sudo args...
    !suppress'''
    from please.log import logger
    logger.warning('sudo is not very polite command.')
    logger.warning('Results can be unexpected.')
    from please.commands import get_please_matcher
    m = get_please_matcher()
    tpl, handler, args = m.match_template(args)
    if handler is None:
        logger.error('I really cannot do this!')
        logger.error('Why you are forcing me?')
        logger.error('Please is throwing a tantrum!')
    else:
        from inspect import getargspec
        vargs = getargspec(handler)[0]
        if 'sudo' not in vargs:
            logger.warning('This command does not require extra permission.')
        else:
            args['sudo'] = True
        handler(**args)

def make_me_food(food, sudo = False):
    '''make me food...
    !suppress'''
    from please.log import logger
    if not sudo:
        if len(food) == 1 and food[0] == 'smile':
            logger.info('I can smile to you.')
            smile()
        logger.error('What? Do it yourself.')
    elif len(food) == 1 and food[0] == 'sandwich':
        logger.info('Okay.')
        logger.info('I hope you know about xkcd.com.')
    else:
        logger.warning('Do know know how to make ' + ' '.join(food) + '. Delegating to cook.')
        logger.error('ImportError: module please.cook not found.')

def smile():
    '''smile
    !suppress'''
    from please.log import logger
    import random
    smile = random.choice(('^_^', # japan-smile
                           '(^ ^)', # another one
                           ':)', # short smile
                           ':-)', # long smile
                           ')', # Russian smile
                           ')))', # gurovic smile
                           '(:', # confusion smile
                           '\u263a', # unicode smile
                           '\u263b', # afroamerican smile
                           'ッ', # katakana smile
                           'ت', # arabic smile
                           ':D', # grin smile
                           ':-D', # long grin smile
                           'ХД', # stupid smile
                           '(_8(|)', # Homer smile
                          ))
    logger.info("I'm always glad to see you! " + smile)

