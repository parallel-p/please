def form_err_string_by_std(stdout, stderr):
    result = ""
    if stderr.strip() != "":
        result += "\n\t\tSTDERR:\n" + stderr
    if stdout.strip() != "":
        result += "\n\t\tSTDOUT:\n" + stdout
    return result

def process_err_exit(err_str, verd, ex_code, stdout, stderr, logger):
    out_err_str = err_str + " " + verd
    if verd == "RE":
        out_err_str += " with exit code: " + str(ex_code)
    logger.error(out_err_str)
    formed_std = form_err_string_by_std(stdout, stderr)
    if formed_std != "": logger.error(formed_std)