def convert(file):
    """
    This method converts all ends of lines to native
    Do nothing if unable to open file in utf-8
    """
    data = None
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()
    except UnicodeDecodeError as e:
        pass #ignore this error
    
    if (data is None):
        return
    
    with open(file, 'w', encoding='utf-8') as g:
        g.write(data)
    
