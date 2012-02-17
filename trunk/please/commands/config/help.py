
def help(command = None):
    '''help [command...]
    Help on a command or write a list of commands.'''
    from please.commands import get_matcher
    m = get_matcher('please')
    if command is None or command == ['commands']:
        for template, _ in m.templates:
            h = template.format()
            if h:
                print(h)
                print()
    elif command == ['me', 'Eirin']:
        print('Nice try, but I do not know path to Gensokyo.')
        print('Neither Eirin am I.')
    else:
        tpl = m.match_template(command)[0]
        if tpl is None or tpl.help() is None:
            print("I don't know how to " + ' '.join(command))



