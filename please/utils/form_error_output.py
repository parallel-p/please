def form_err_string_by_std(stdout, stderr):
    result = ""
    if stderr.strip() != "":
        result += "\n\t\tSTDERR:\n" + stderr
    if stdout.strip() != "":
        result += "\n\t\tSTDOUT:\n" + stdout
    return result

def process_err_exit(err_str, verd, ex_code, stdout, stderr):
    out_err_str = err_str + " " + verd
    if verd == "RE":
        out_err_str += " with exit code: " + str(ex_code)
    out_err_str += form_err_string_by_std(stdout, stderr)
    return out_err_str