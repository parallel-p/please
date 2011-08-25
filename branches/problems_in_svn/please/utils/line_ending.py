def convert(file):
    data = None
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    
    if (data is None):
        return
    
    with open(file, 'w', encoding='utf-8') as g:
        g.write(data)
    
