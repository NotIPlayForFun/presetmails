from termcolor import colored
import config as cfg

def checkprint(text):
    print(colored(
        text
        ,color=cfg.CHECK_COLOR
    ))

def loadprint(text):
    print(colored(
        text
        ,color=cfg.LOAD_COLOR
    ))