from lxml import etree

def make_language_choice(elements):
    for element in elements:
        if element.get('language') == 'russian':
            return element
    for element in elements:
        if element.get('language') == 'english':
            return element
    return elements[0]