from colorama import Fore

__all__ = [
    "black", "red", "green", "yellow",
    "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white"
]

def coloured_text_func_builder(colour: Fore, text: str | int) -> str:
    return "\n".join(f"{colour}{line}{Fore.RESET}" for line in str(text).split("\n"))

def black(text: str | int) -> str:
    return coloured_text_func_builder(Fore.BLACK, text)

def red(text: str | int) -> str:
    return coloured_text_func_builder(Fore.RED, text)

def green(text: str | int) -> str:
    return coloured_text_func_builder(Fore.GREEN, text)

def yellow(text: str | int) -> str:
    return coloured_text_func_builder(Fore.YELLOW, text)

def blue(text: str | int) -> str:
    return coloured_text_func_builder(Fore.BLUE, text)

def magenta(text: str | int) -> str:
    return coloured_text_func_builder(Fore.MAGENTA, text)

def cyan(text: str | int) -> str:
    return coloured_text_func_builder(Fore.CYAN, text)

def white(text: str | int) -> str:
    return coloured_text_func_builder(Fore.WHITE, text)

def bright_black(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTBLACK_EX, text)

def bright_red(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTRED_EX, text)

def bright_green(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTGREEN_EX, text)

def bright_yellow(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTYELLOW_EX, text)

def bright_blue(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTBLUE_EX, text)

def bright_magenta(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTMAGENTA_EX, text)

def bright_cyan(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTCYAN_EX, text)

def bright_white(text: str | int) -> str:
    return coloured_text_func_builder(Fore.LIGHTWHITE_EX, text)
