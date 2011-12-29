class TestInfo:
    def __init__(self):
        raise NotImplementedError()
    
    def tests(self):
        raise NotImplementedError()
    
    def get_tags(self):
        raise NotImplementedError()
    
    def to_please_format(self):
        raise NotImplementedError()
    
    def get_to_please_format_prefix(self, tags):
        tags_list = []
        for key, value in tags.items():
            curtag = str(key)
            if value is not None:
                curtag += " = " + str(value)
            tags_list.append(curtag)
        if len(tags_list) > 0:
            return "[" + ', '.join(tags_list) + "] "
        else:
            return ""