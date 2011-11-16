def form_err_string_by_std(stdout, stderr):
    result = ""
    if stderr.strip() != "":
        result += "\n\t\tSTDERR:\n" + stderr
    if stdout.strip() != "":
        result += "\n\t\tSTDOUT:\n" + stdout
    return result