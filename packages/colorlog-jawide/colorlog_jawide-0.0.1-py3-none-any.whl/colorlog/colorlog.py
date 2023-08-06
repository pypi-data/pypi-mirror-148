import os
from typing import Dict
from types import ModuleType


if os.name == "nt":
    os.system("")

class Fore:
    NORMAL          = 0
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37

class Back:
    NORMAL          = 0
    BLACK           = 40
    RED             = 41
    GREEN           = 42
    YELLOW          = 43
    BLUE            = 44
    MAGENTA         = 45
    CYAN            = 46
    WHITE           = 47

class Style:
    NORMAL    = 0
    BRIGHT    = 1
    FORCE     = 4
    BLINK     = 5
    REVERSE   = 7
    INVISIBLE = 8

class Color:
    def __init__(self, fore:Fore=Fore.NORMAL, back:Back=Back.NORMAL, style:Style=Style.NORMAL) -> None:
        self.fore = fore
        self.back = back
        self.style = style

class LogLevel:
    NOTSET   = 0
    DEBUG    = 10
    INFO     = 20
    WARNING  = 30
    ERROR    = 40
    CRITICAL = 50

default_level_colors = {}
default_level_colors[LogLevel.NOTSET]   = Color()
default_level_colors[LogLevel.DEBUG]    = Color(Fore.BLUE, Style.BRIGHT)
default_level_colors[LogLevel.INFO]     = Color()
default_level_colors[LogLevel.WARNING]  = Color(Fore.YELLOW)
default_level_colors[LogLevel.ERROR]    = Color(Fore.RED)
default_level_colors[LogLevel.CRITICAL] = Color(Fore.RED, Back.YELLOW, Style.BRIGHT)

class Config:
    def __init__(self, level_colors:Dict[LogLevel, Color]={}) -> None:
        self.level_colors = {}
        for level, color in default_level_colors.items():
            self.level_colors[level] = level_colors.get(level) or color
        
    def set_color(self, log_level:LogLevel, color:Color):
        self.level_colors[log_level] = color

DEFAULT_CONFIG = Config()

def init(logging:ModuleType, config:Config=DEFAULT_CONFIG):
    def emit(self, record):
        try:
            levelno = record.levelno
            color = config.level_colors[levelno]
            preffix = "\033["
            preffix += str(color.style)
            if color.fore != Fore.NORMAL:
                preffix += ";"
                preffix += str(color.fore)
            if color.back != Back.NORMAL:
                preffix += ";"
                preffix += str(color.back)
            preffix += "m"
            suffix = "\033[0m"
            msg = self.format(record)
            stream = self.stream
            stream.write(preffix + msg + self.terminator + suffix)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

    setattr(logging.StreamHandler, "emit", emit)