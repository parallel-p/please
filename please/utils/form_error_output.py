def form_err_string_by_std(stdout, stderr):
    result = ""
    if stderr.strip() != "":
        result += "\nSTDERR:\n" + stderr
    if stdout.strip() != "":
        result += "\nSTDOUT\n" + stdout
    return result