import os
def remove_trash (diff, is_trash):
    for token in diff:
        if is_trash(token):
            os.remove(token)