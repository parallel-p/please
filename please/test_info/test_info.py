class TestInfo:
    def __init__(self, tags, comment):
        self.__tags = tags
        self.__comment = str(comment).strip()
    
    def tests(self):
        raise NotImplementedError()
    
    def get_tags(self):
        return self.__tags
    
    def to_please_format(self):
        raise NotImplementedError()
    
    def set_tag(self, item, value):
        self.__tags[item] = value
        
    def get_prefix(self):
        tags_list = []
        for key, value in sorted(self.__tags.items()):
            curtag = str(key)
            if value is not None:
                curtag += " = " + str(value)
            tags_list.append(curtag)
        if len(tags_list) > 0:
            return "[" + ', '.join(tags_list) + "]"
        else:
            return ''
    
    def get_suffix(self):
        return ('#' + self.__comment) if self.__comment != '' else ''
