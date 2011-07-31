from colorama import Fore, Back, Style, init
init()

def warning(text):
    return(Fore.YELLOW + text + Fore.RESET)
def error(text):
    return(Fore.RED + text + Fore.RESET)
def ok(text):
    return(Fore.GREEN + text + Fore.RESET)
