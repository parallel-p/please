import os
import shutil
import logging
from .. import globalconfig

def remove_trash (diff, is_trash):
    #diff == [[dirs], [files]]
    for token in diff[1]:
        if is_trash(token):
            os.remove(token)
    for token in diff[0]:
        if is_trash(token):
            shutil.rmtree(token)


def remove_logs_in_depth(logs_names_list=globalconfig.logs, base_dir='.', out=True, depth=True):            
    logging.shutdown()
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            for log in logs_names_list:
                if file == log:
                    if out:
                        print("Removing log " + log + " in " + root)
                    os.remove(os.path.join(root, log))
        if not depth:
            break
