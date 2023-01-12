import os

PROJECT_NAME = "Presetmails"

#datafiles
abs_basedir = os.path.dirname(__file__)
abs_datadir = abs_basedir
#abs_datadir = os.path.join(abs_basedir, "data")
MAIL_PRESET_FILE = "MAIL_PRESET.txt"
ABS_MAIL_PRESET_FILE = os.path.join(abs_basedir, MAIL_PRESET_FILE)
REL_MAIL_PRESET_FILE = ""
APPDATA_FILE = "appdata.json"
ABS_APPDATA_FILE = os.path.join(abs_datadir, APPDATA_FILE)
REL_APPDATA_FILE= ""


DEFAULT_MAIL_SUBJECT = "Sent using presetmails.py"
APPDATA_FILE_STRUCTURE_TEMPLATE_DICT = {
    "userdata": {
        "smtp_server": str(),
        "mail_address": str(),
        "username": str(),
        "password": str(),
    }
}