import os

def remove_trash (diff, is_trash):
    for token in diff:
        if is_trash(token):
            os.remove(token)

def remove_logs_in_depth(logs_names_list, base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            for log in logs_names_list:
                if file == log:
                    os.remove(os.path.join(root, log))