import os.path
import re
from configparser import ConfigParser
from datetime import datetime


def get_all_sections(filepath):
    cfg = ConfigParser()
    cfg.read(filepath, encoding="utf-8")

    return cfg.sections()

def get_items(filepath,section):
    cfg = ConfigParser()
    cfg.read(filepath, encoding="utf-8")

    list=[]
    if cfg.has_section(section):
       list.extend( cfg.items(section))

    return dict(list)

def get_item_int(filepath,section,itemkey):
    if not os.path.exists(filepath):
        return -1

    cfg = ConfigParser()
    cfg.read(filepath,encoding="utf-8")

    if cfg.has_section(section) and cfg.has_option(section,itemkey):
       return cfg.getint(section,itemkey)
    else:
        return -1

def get_item_float(filepath,section,itemkey):
    if not os.path.exists(filepath):
        return -1.0

    cfg = ConfigParser()
    cfg.read(filepath,encoding="utf-8")

    if cfg.has_section(section) and cfg.has_option(section,itemkey):
        return cfg.getfloat(section, itemkey)
    else:
        return -1.0

def get_item_boolean(filepath,section,itemkey):
    if not os.path.exists(filepath):
        return False

    cfg = ConfigParser()
    cfg.read(filepath, encoding="utf-8")

    if cfg.has_section(section) and cfg.has_option(section,itemkey):
        return cfg.getboolean(section, itemkey)
    else:
        return False

def get_item_string(filepath,section,itemkey):
    if not os.path.exists(filepath):
        return ""

    cfg = ConfigParser()
    cfg.read(filepath, encoding="utf-8")

    if cfg.has_section(section) and cfg.has_option(section,itemkey):
        return cfg.get(section, itemkey)
    else:
        return ""

def validate_time_format(time_str: str, format_str: str) -> bool:
    try:
        datetime.strptime(time_str, format_str)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    # list = get_all_sections("config.ini")
    # print(list)
    #
    # list = get_items("config.ini","settings")
    # print(list)

    # tmp = get_item_boolean("config.ini","settings","fullscreen")
    # print(f"fullscreen:{tmp}")
    #
    # tmp =get_item_int("config.ini", "settings", "fontsize")
    # print(f"fontsize:{tmp}")
    #
    # tmp=get_item_float("config.ini", "settings", "compression")
    # print(f"compression:{tmp}")
    #
    # tmp = get_item_string("config.ini", "settings", "font")
    # print(f"font:{tmp}")

    clear_timer = get_item_string("D:\Python\Python312\config.ini", "settings", "clear_time" )
    print(clear_timer)
    clear_timer_list = [t.strip() for t in clear_timer.split("|") if t.strip()]
    for i in clear_timer_list:
        if validate_time_format(i, "%H:%M"):
            print(i,True)
        else:
            print(i,"时间格式不正确")

