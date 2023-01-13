import json
import my_error as mye
import getpass
import config as cfg
import os
#can eventually use this to read and write other data like env variables etc

'''#returns data from json as python object
def get_data_from_json(abs_jsonfile):
    pass

def dump_data_to_json(abs_jsonfile, data):
    json_str = json.dumps(data)
    dump_data_to_json
def dumps_data_to_json(abs_jsonfile, datastring):
    json.dump()'''

def restore_datafile_default_template(filename, template):
    f = open(filename, 'w')
    json.dump(template, f, indent=4)
    f.close()

def restore_appdata_default_template():
    f = open(cfg.ABS_APPDATA_FILE, 'w')
    json.dump(cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT, f, indent=4)
    f.close()

#try to get dict from userdata, raises error with a mye.MyE object in error.args if failed
#if data is corruped, resets data
'''def get_userdata_dict():
    #check if file already exists, if not, create it with template dict
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'x')
        #json_str = json.dumps(dict())
        #f.write(json_str)
        #OR
        #json.dump(json.load(json_str), f)
        #OR
        json.dump(cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT, f, indent=4)
        f.close()
    except FileExistsError as e:
        pass

    #open the file in read mode
    try:
        f = open("cfg.ABS_APPDATA_FILE", 'r')
    except Exception as e:
        err = mye.MyE(e, f"Could not open and read file \"{cfg.ABS_APPDATA_FILE}\"")
        e.args = e.args + (err, )
        print("err")
        print(e)
        raise e
        #raise e(f"Could not open and read file \"{cfg.ABS_APPDATA_FILE}\"")
        #err = mye.new_e(e, f"Could not open and read file \"{cfg.ABS_APPDATA_FILE}\"")
        #wrapped_e = mye.MyError(e, f"Could not open and read file \"{cfg.ABS_APPDATA_FILE}\"", ("var1", testvar), ("var2", testvar2))
        #raise err

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    except json.JSONDecodeError as e:
        mye.eprint(e, f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
                            f"Overwriting \"{cfg.ABS_APPDATA_FILE}\" and filling with userdata from setup.")
        f.close()
        restore_appdata_default_template()
        print("RESTORING")
        data = cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT
    except Exception as e:
        mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    print(data)
    return data'''

def add_prev_maildata_preset(preset):
    #open the file in read mode
    try:
        f = open(cfg.ABS_PREV_MAILDATA_PRESETS_FILE, 'r')
    except json.JSONDecodeError as e:
        raise e
    except Exception as e:
        raise e

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    except Exception:
        #mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        #exit(1)
        raise

    try:
        data["previous_presets_list"].append(preset)
    except Exception as e:
        mye.eprint(e, f"Could not append preset to \"previous_presets_list\" in {cfg.PREV_MAILDATA_PRESETS_FILE}", [["data", data], ["preset", preset]])
        exit(1)
    #write back to file with appended preset at end of list
    try:
        f = open(cfg.ABS_PREV_MAILDATA_PRESETS_FILE, 'r+')
    except Exception as e:
        mye.eprint(e, f"Could not open file \"{cfg.ABS_PREV_MAILDATA_PRESETS_FILE}\"")
        exit(1)
    json.dump(data, f, indent=4)
    return data
    


def get_data(filepath, *object_chain, create=False):
    print(f"Loading data from {os.path.basename(filepath)}..")
    if create:
        #check if file already exists, if not, create it with template dict
        try:
            f = open(cfg.ABS_APPDATA_FILE, 'x')
            #json_str = json.dumps(dict())
            #f.write(json_str)
            #OR
            #json.dump(json.load(json_str), f)
            #OR
            f.close()
        except FileExistsError as e:
            pass
    else:
        if not os.path.isfile(filepath):
            raise Exception

    #open the file in read mode
    try:
        f = open(filepath, 'r')
    except json.JSONDecodeError as e:
        raise e
    except Exception as e:
        raise e

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    except Exception:
        #mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        #exit(1)
        raise
    #print(object_chain)
    if object_chain:
        out = data
        for obj in object_chain:
            try:
                out = out[obj]
            except Exception:
                raise
    else:
        out = data
    return out
def get_maildata_presets(*object_chain):
    #if from_py_obj:
    #    appdata = from_py_obj
    #else:
    print("Loading maildata presets.. unfinished")
    #open the file in read mode
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'r')
    except Exception:
        #mye.eprint(e, f"Could not find file \"{cfg.ABS_APPDATA_FILE}\"")
        #exit(1)
        raise

    #load the json into a python dict data
    try:
        appdata = json.load(f)
        f.close()
    except Exception:
        #mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        #exit(1)
        raise
    print(object_chain)
    if object_chain:
        out = appdata
        for obj in object_chain:
            try:
                out = out[obj]
            except Exception:
                raise
    else:
        out = appdata
    return out
def get_appdata(*object_chain, from_py_obj=None):
    if object_chain:
        print(f"Loading {object_chain[len(object_chain) - 1]}...")
    else:
        print(f"Loading appdata...")
    if from_py_obj:
        appdata = from_py_obj
    else:
        #open the file in read mode
        try:
            f = open(cfg.ABS_APPDATA_FILE, 'r')
        except Exception:
            #mye.eprint(e, f"Could not find file \"{cfg.ABS_APPDATA_FILE}\"")
            #exit(1)
            raise

        #load the json into a python dict data
        try:
            appdata = json.load(f)
            f.close()
        except Exception:
            #mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
            #exit(1)
            raise
    #print(object_chain)
    if object_chain:
        out = appdata
        for obj in object_chain:
            try:
                out = out[obj]
            except Exception:
                raise
    else:
        out = appdata
    return out

'''def find_missing_appdata_rec(*appdata_object_chain, return_list=list()):
    None'''

#could make this function generic with appdata_objectname=None and then if none is given check everything based off the preset
'''def find_missing_appdata(*appdata_object_chain, return_list=list()):
    returns list of lists, each containing the object chain and name of the missing item (missing meaning not found or of incorrect type)
    
    lists are treated as ordinary items and wont be iterated over
    
    only accepts dicts as target (last item) of appdata_object_chain
    
    
    if not appdata_object_chain:
        try:
            item = get_appdata()
        except Exception as e:
            raise e
        try:
            item_default = get_appdata(from_py_obj=cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT)
        except Exception as e:
            raise e
    else:
        try:
            item = get_appdata(o for o in appdata_object_chain)
        except Exception as e:
            raise e
        try:
            item_default = get_appdata((o for o in appdata_object_chain), from_py_obj=cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT)
        except Exception as e:
            raise e
  
    if type(item_default) != dict:
        raise Exception

    if type(item_default) != type(item_default):
        None
    print(item)
    print(item_default)'''

def find_missing_data_in_json_dict(*object_chain, abs_filename, template, ):
    print(f"Checking for any missing/corrupt data in {os.path.basename(abs_filename)}...")
    #check if file already exists, if not, create it with template dict
    try:
        f = open(abs_filename, 'x')
        #json_str = json.dumps(dict())
        #f.write(json_str)
        #OR
        #json.dump(json.load(json_str), f)
        #OR
        json.dump(template, f, indent=4)
        f.close()
    except FileExistsError as e:
        pass

    #open the file in read mode
    try:
        f = open(abs_filename, 'r')
    except Exception as e:
        mye.eprint(e, f"Could not find file \"{abs_filename}\"")
        exit(1)

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    #reset to default if corrupt
    except json.JSONDecodeError as e:
        #mye.eprint(e, f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
        #                    f"Resetting \"{cfg.ABS_APPDATA_FILE}\".")
        print(f"Could not load data from \"{abs_filename}\". Likely corrupt file.\n"
                            f"Resetting \"{abs_filename}\" to default...")
        f.close()
        restore_datafile_default_template(abs_filename, template)
        data = cfg.PREV_MAILDATA_PRESETS_TEMPLATE
    except Exception as e:
        mye.eprint(e, f"Could not load data from file \"{abs_filename}\"")
        exit(1)
    if type(data) != dict:
        print(f"Could not load data from \"{abs_filename}\": type is not dict. Likely corrupt file.\n"
                            f"Resetting \"{abs_filename}\" to default...")
        f.close()
        restore_datafile_default_template(abs_filename, template)
        data = cfg.PREV_MAILDATA_PRESETS_TEMPLATE

    #determine any wrong/missing data
    missing_data_list = list()
    for defkey in template:
        if defkey not in data.keys():
            missing_data_list.append(defkey)
            print(f"Could not load some data from \"{abs_filename}: Value not found.\n"
                            f"Writing empty {defkey} into \"{abs_filename}\"...")
            data[defkey] = template[defkey]
        elif type(data[defkey]) != type(template[defkey]):
            missing_data_list.append(defkey)
        elif data[defkey] == template[defkey]:
            missing_data_list.append(defkey)

    #write back to file with any missing datafields replaced by default datafield or entire file replaced by default file if corrupt
    try:
        f = open(abs_filename, 'r+')
    except Exception as e:
        mye.eprint(e, f"Could not open file \"{abs_filename}\"")
        exit(1)
    json.dump(data, f, indent=4)
    return missing_data_list

#could just try: get_appdata("userdata") except Exception as e: mye.printe(e, etc. etc.) here instead
#of doing it manually again, but who cares
#also could make this function generic for missing_anything, buuuuut you know
def find_missing_userdata():
    print("Checking for any missing/corrupt userdata...")
    #check if file already exists, if not, create it with template dict
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'x')
        #json_str = json.dumps(dict())
        #f.write(json_str)
        #OR
        #json.dump(json.load(json_str), f)
        #OR
        json.dump(cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT, f, indent=4)
        f.close()
    except FileExistsError as e:
        pass

    #open the file in read mode
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'r')
    except Exception as e:
        mye.eprint(e, f"Could not find file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    #reset to default if corrupt
    except json.JSONDecodeError as e:
        #mye.eprint(e, f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
        #                    f"Resetting \"{cfg.ABS_APPDATA_FILE}\".")
        print(f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
                            f"Resetting \"{cfg.ABS_APPDATA_FILE}\" to default...")
        f.close()
        restore_appdata_default_template()
        data = cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT
    except Exception as e:
        mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)
    
    #determine any wrong/missing data
    missing_userdata_list = list()
    ud = data["userdata"]
    default_ud = cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT["userdata"]
    for defkey in default_ud:
        if defkey not in ud.keys():
            missing_userdata_list.append(defkey)
            print(f"Could not load some data from \"{cfg.ABS_APPDATA_FILE}[\"userdata\"]: Value not found.\n"
                            f"Writing empty {defkey} into \"{cfg.ABS_APPDATA_FILE}\"...")
            data["userdata"][defkey] = default_ud[defkey]
        elif type(ud[defkey]) != type(default_ud[defkey]):
            missing_userdata_list.append(defkey)
        elif ud[defkey] == default_ud[defkey]:
            missing_userdata_list.append(defkey)

    #write back to file with any missing datafields replaced by default datafield or entire file replaced by default file if corrupt
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'r+')
    except Exception as e:
        mye.eprint(e, f"Could not open file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)
    json.dump(data, f, indent=4)
    return missing_userdata_list

def setup_userdata():
    #get userdata
    smtp_server = str()
    port = int()
    mail_address = str()
    username = str()
    password = str()
    port_inp = str()
    while smtp_server == '':
        smtp_server = input(">Your mail-providers smtp-server(You can find this domain via google): ")
    while True:
        port_inp = input(">Your mail-providers smtp-servers port (You can find this via google): ")
        if port_inp == "":
            continue
        try:
            port = int(port_inp)
        except ValueError as e:
            print(f"--> Please enter a number >= 0")
            continue
        if port < 0:
            print(f"--> Please enter a number >= 0")
            continue
        break
    while mail_address == '':
        mail_address = input(">Your mail-address: ")
    while username == '':
        username = input(">Your mail-provider username: ")
    while password == '':
        password = getpass.getpass(prompt=">Your mail-provider password: ")

    #write to json

    #check if file already exists, if not, create it with template dict
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'x')
        #json_str = json.dumps(dict())
        #f.write(json_str)
        #OR
        #json.dump(json.load(json_str), f)
        #OR
        json.dump(cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT, f, indent=4)
        f.close()
    except FileExistsError as e:
        pass

    #open the file in read mode
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'r')
    except Exception as e:
        mye.eprint(e, f"Could not open/create file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    except json.JSONDecodeError as e:
        mye.eprint(e, f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
                            f"Overwriting \"{cfg.ABS_APPDATA_FILE}\" and filling with userdata from setup.")
        f.close()
        restore_appdata_default_template()
        print("RESTORING")
        data = cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT
    except Exception as e:
        mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    #write new userdata into data
    data["userdata"]["smtp_server"] = smtp_server
    data["userdata"]["port"] = port
    data["userdata"]["mail_address"] = mail_address
    data["userdata"]["username"] = username
    data["userdata"]["password"] = password

    #write modified data back into datafile
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'w')
        json.dump(data, f, indent=4)
        f.close()
    except Exception as e:
        mye.eprint(e, f"Write data to \"{cfg.ABS_APPDATA_FILE}\". Something went wrong.\n")
        exit(1)

    print("Userdata setup successfull. Run setup again to change data.")
    f = open(cfg.ABS_APPDATA_FILE, 'r')
    #print(json.dumps(json.load(f), indent=4))
    f.close()

    return 0


'''def setup_userdata():
    #get userdata
    smtp_server = str()
    mail_address = str()
    username = str()
    password = str()
    while smtp_server == '':
        smtp_server = input("Your mail-providers smtp-server(You can find this domain via google): ")
    while mail_address == '':
        mail_address = input("Your mail-address: ")
    while username == '':
        username = input("Your mail-provider username: ")
    while password == '':
        password = getpass.getpass(prompt="Your mail-provider password: ")

    #write to json

    #check if file already exists, if not, create it with template dict
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'x')
        #json_str = json.dumps(dict())
        #f.write(json_str)
        #OR
        #json.dump(json.load(json_str), f)
        #OR
        json.dump(cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT, f, indent=4)
        f.close()
    except FileExistsError as e:
        pass

    #open the file in read mode
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'r')
    except Exception as e:
        mye.eprint(e, f"Could not open/create file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    #load the json into a python dict data
    try:
        data = json.load(f)
        f.close()
    except json.JSONDecodeError as e:
        mye.eprint(e, f"Could not load data from \"{cfg.ABS_APPDATA_FILE}\". Likely corrupt file.\n"
                            f"Overwriting \"{cfg.ABS_APPDATA_FILE}\" and filling with userdata from setup.")
        f.close()
        restore_appdata_default_template()
        print("RESTORING")
        data = cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT
    except Exception as e:
        mye.eprint(e, f"Could not load data from file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)

    print(data)
    #write new userdata into data
    data["userdata"]["smtp_server"] = smtp_server
    data["userdata"]["mail_address"] = mail_address
    data["userdata"]["username"] = username
    data["userdata"]["password"] = password

    #write modified data back into datafile
    f = open(cfg.ABS_APPDATA_FILE, 'w')
    json.dump(data, f, indent=4)
    f.close()

    f = open(cfg.ABS_APPDATA_FILE, 'r')
    print(json.dumps(json.load(f), indent=4))
    f.close()

    return 0'''