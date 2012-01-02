import os

def is_program_detect(path):
    if "." in path:
        programm_suffix = [".c", 
                ".cpp",
                ".c++",
                ".cs",
                ".pas",
                ".java",
                ".py",
                ".dpr"]
        file_suffix = os.path.splitext(path)[1]
        if file_suffix in programm_suffix:
            return True
        else:
            return False
    else:
        return False
    
