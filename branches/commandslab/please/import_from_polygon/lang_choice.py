def make_language_choice(elements):
    for element in elements:
        if element.get('language') == 'russian':
            return element
    for element in elements:
        if element.get('language') == 'english':
            return element
    if len(elements)>0:
        return elements[0]
    else:
        return None
    
