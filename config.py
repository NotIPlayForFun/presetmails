import os

PROJECT_NAME = "Presetmails"
KR_NAMESPACE = "Presetmails"
KR_GENERIC_USERNAME = "PresetmailsUsername"
DEFAULT_PORT = 0
MAX_PREV_PRESET_LIST_LEN = 10

#DATAFILES
abs_basedir = os.path.dirname(__file__)
abs_datadir = abs_basedir#
#abs_datadir = os.path.join(abs_basedir, "data")

MAIL_PRESET_FILE = "MAIL_PRESET.txt"
ABS_MAIL_PRESET_FILE = os.path.join(abs_basedir, MAIL_PRESET_FILE)
REL_MAIL_PRESET_FILE = ""

APPDATA_FILE = "appdata.json"
ABS_APPDATA_FILE = os.path.join(abs_datadir, APPDATA_FILE)
REL_APPDATA_FILE= ""

PREV_MAILDATA_PRESETS_FILE = "prev_maildata_presets.json"
ABS_PREV_MAILDATA_PRESETS_FILE = os.path.join(abs_datadir, PREV_MAILDATA_PRESETS_FILE)
REL_MAILDATA_PRESETS_FILE = ""

REQUIREMENTS_FILE = "requirements.txt"
ABS_REQUIREMENTS_FILE = os.path.join(abs_datadir, REQUIREMENTS_FILE)
REL_REQIREMENTS_FILE = ""


#TEMPLATES
DEFAULT_MAIL_SUBJECT = "Sent using presetmails.py"
APPDATA_FILE_STRUCTURE_TEMPLATE_DICT = {
    "userdata": {
        "smtp_server": str(),
        "port": -1,
        "mail_address": str(),
        "username": str(),
        "store_pw": False
    }
}
PREV_MAILDATA_PRESETS_TEMPLATE = {
    "previous_presets_list": list()
}
MAILDATA_PRESET_TEMPLATE = {
    "preset_name": str(),
    "from": str(),
    "to": str(),
    "subject": str(),
    "variable_defs": list()
}

#Colors
CHECK_COLOR = "magenta"
LOAD_COLOR = "light_magenta"