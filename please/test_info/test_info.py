class TestInfo:
    def __init__():
        raise NotImplementedError()
    
    def tests():
        raise NotImplementedError()
    
    def get_tags():
        raise NotImplementedError()
    
    def to_please_format():
        raise NotImplementedError()
    
    def get_to_please_format_prefix(tags):
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