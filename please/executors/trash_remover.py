import os
import logging

def remove_trash (diff, is_trash):
    for token in diff:
        if is_trash(token):
            os.remove(token)


def remove_logs_in_depth(logs_names_list, base_dir):            
    logger = logging.getLogger("please_logger.executors.remove_logs_in_depth")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            for log in logs_names_list:
                if file == log:
                    logger.info("Removing log " + log + " in " + root)
                    os.remove(os.path.join(root, log))