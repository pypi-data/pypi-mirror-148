from colorama import Fore, Style

def Logger(message: str, _type: str = "INFO", _save: bool = False, path: str = "") -> None:
    _type = _type.upper()
    _msg_bk = message
    if _type == "INFO":
        message = f"[{Fore.CYAN} INFO {Style.RESET_ALL}]=:> {message}"
    elif _type == "WARNING":
        message = f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}]=:> {message}"
    elif _type == "ERROR":
        message = f"[{Fore.RED} ERROR {Style.RESET_ALL}]=:> {message}"
    elif _type == "SUCCESS":
        message = f"[{Fore.GREEN} SUCCESS {Style.RESET_ALL}]=:> {message}"
    else:
        message = f"[{Fore.MAGENTA} UNKNOWN {Style.RESET_ALL}]=:> {message}"
    
    print(message)
    
    if _save == True:
        with open(path, "a") as log:
            log.write(f"[ {_type} ]=:> " + _msg_bk + "\n")

    del message, _type, _save, _msg_bk


def Banner(author: str = "", license: str = "", project: str = "") -> None:
    print("""
    
                        _                   
                       | |                  
  _ __  _   _ _ __ ___ | |__   ___ _ __ ___ 
 | '_ \| | | | '_ ` _ \| '_ \ / _ \ '__/ __|
 | | | | |_| | | | | | | |_) |  __/ |  \__ \\
 |_| |_|\__,_|_| |_| |_|_.__/ \___|_|  |___/
                                            
                                            

    """)