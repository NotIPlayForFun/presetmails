import json
import my_error as mye
import getpass
import config as cfg
#can eventually use this to read and write other data like env variables etc

'''#returns data from json as python object
def get_data_from_json(abs_jsonfile):
    pass

def dump_data_to_json(abs_jsonfile, data):
    json_str = json.dumps(data)
    dump_data_to_json
def dumps_data_to_json(abs_jsonfile, datastring):
    json.dump()'''


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
def get_appdata(*object_chain):
    print("Loading userdata..")
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
    mail_address = str()
    username = str()
    password = str()
    while smtp_server == '':
        smtp_server = input(">Your mail-providers smtp-server(You can find this domain via google): ")
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