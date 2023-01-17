import json
import my_error as mye
import getpass
import config as cfg
import os
import getpass
import keyring
import copy
from termcolor import colored
from  cryptography.fernet import Fernet
import utility as util
#can eventually use this to read and write other data like env variables etc

#There's alot of duplicate code in here but I cant be bothered,
#just make sure to use the proper generic functions from now on

def restore_datafile_default_template(filename, template):
    f = open(filename, 'w')
    json.dump(template, f, indent=4)
    f.close()

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
        while len(data["previous_presets_list"]) >= cfg.MAX_PREV_PRESET_LIST_LEN:
            data["previous_presets_list"].pop(0)
        data["previous_presets_list"].append(preset)
    except Exception as e:
        mye.eprint(e, f"Could not append preset to \"previous_presets_list\" in {cfg.PREV_MAILDATA_PRESETS_FILE}", [["data", data], ["preset", preset]])
        exit(1)
    #write back to file with appended preset at end of list
    try:
        f = open(cfg.ABS_PREV_MAILDATA_PRESETS_FILE, 'w')
    except Exception as e:
        mye.eprint(e, f"Could not open file \"{cfg.ABS_PREV_MAILDATA_PRESETS_FILE}\"")
        exit(1)
    json.dump(data, f, indent=4)
    return data
    


def get_data(filepath, *object_chain, create=False):
    util.loadprint(f"Loading data from {os.path.basename(filepath)}..")
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
    util.loadprint("Loading maildata presets.. unfinished")
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
        util.loadprint(f"Loading {object_chain[len(object_chain) - 1]}...")
    else:
        util.loadprint(f"Loading appdata...")
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

def find_missing_data_in_json_dict(*object_chain, abs_filename, template, ):
    util.checkprint(f"Checking for any missing/corrupt data in {os.path.basename(abs_filename)}...")
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
def find_missing_userdata(del_extra = False):
    util.checkprint("Checking for any missing/corrupt userdata...")
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
        restore_datafile_default_template(cfg.ABS_APPDATA_FILE, cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT)
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
            print(f"type(ud[{defkey}]) != type(default_ud[{defkey}])")
            missing_userdata_list.append(defkey)
            data["userdata"][defkey] = default_ud[defkey]
        elif ud[defkey] == default_ud[defkey]:
            #print(f"ud[{defkey}] == default_ud[{defkey}]")
            if ud[defkey] == False:
                #print("ignoring")
                None
            else:
                missing_userdata_list.append(defkey)
    if del_extra:
        del_list = list()
        for udkey in ud.keys():
            if udkey not in default_ud.keys():
                print("popped")
                print(udkey)
                del_list.append(udkey)
        for delkey in del_list:
            ud.pop(delkey)

    #write back to file with any missing datafields replaced by default datafield or entire file replaced by default file if corrupt
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'w')
    except Exception as e:
        mye.eprint(e, f"Could not open file \"{cfg.ABS_APPDATA_FILE}\"")
        exit(1)
    json.dump(data, f, indent=4)
    return missing_userdata_list

def encrypt(string: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(string)

def decrypt(token: bytes, key: bytes) -> bytes:
    try:
        f = Fernet(key).decrypt(token)
    except Exception as e:
        mye.eprint(None, "Exception while trying decrypt password")
        print(type(e))
        raise e
    return f

def set_password(pw, pw_username=cfg.KR_GENERIC_USERNAME):
    prev_pw = keyring.get_password(cfg.KR_NAMESPACE, pw_username)
    if prev_pw:
        keyring.delete_password(cfg.KR_NAMESPACE, pw_username)
    del prev_pw
    pw = pw.encode()
    #key = Fernet.generate_key()
    key = "f1PNwvNecfAGjsawLEvPF_WBUxRuDpmfB60LQd-08JI=".encode()
    #print("set password")
    #enc = encrypt(string=pw, key=key)
    #print(enc)
    #print(type(enc))
    keyring.set_password(
        service_name=cfg.KR_NAMESPACE, #namespace of the app in the keyring
        username=pw_username, #username associated with the password, currently generic appname as only 1 password is stored at any time
        password=encrypt(string=pw, key=key).decode()   #encrypts password to a bytes type token, then saves this as a utf-8 string
                                                        #in keyring (due to compatibility (me thinks)) 
        )
                                                                                            
    del pw 
    del key
    return 0

def get_password(pw_username=cfg.KR_GENERIC_USERNAME):
    token = keyring.get_password(cfg.KR_NAMESPACE, pw_username).encode()    #gets the utf-8 token string from keyring,
                                                                            #then encodes back to bytes type
    if token == None:
        mye.eprint("Tried to get password from keyring, no password found")
        exit(1)
    #print("token")
    #print(token)
    #print(token.decode())
    #print(type(token))
    key = "f1PNwvNecfAGjsawLEvPF_WBUxRuDpmfB60LQd-08JI=".encode()
    return decrypt(token, key).decode() #returns decrypted bytes token (password) decoded back to utf-8 string

def delete_password(pw_username=cfg.KR_GENERIC_USERNAME, debug=True):
    try:
        keyring.delete_password(cfg.KR_NAMESPACE, pw_username)
        print(colored(
            "Password deleted"
            ,color="green"
        ))
        return 0
    except Exception as e:
        print(colored(
            "Tried to delete password, but password not found"
            ,color="light_yellow"
        ))
        if debug:
            mye.eprint(e, "Tried to delete password, but password not found")
        return 1

def setup_userdata():
    try:
        userdata = get_data(cfg.ABS_APPDATA_FILE, "userdata", create=True)
    except Exception as e:
        mye.eprint(e, "Error getting userdata")
    #get userdata
    smtp_server = userdata["smtp_server"]
    port = userdata["port"]
    mail_address = userdata["mail_address"]
    username = userdata["username"]
    store_pw = userdata["store_pw"]
    password = str()
    port_inp = str()
    options = [[None, "Save data"], [smtp_server, "smtp_server"], [port, "port"], [mail_address, "mail_address"], [None, "login options"]]
    while True:
        print("\n================================Setup================================")
        print("Options:")
        i = 0
        print(f"{i:2}.\t{options[i][1]}")
        for option in options[1:]:
            i += 1
            if option[1] == "login options":
                current = ""
            else:
                if option[0] == cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT["userdata"][option[1]]:
                    current = f" > undefined"
                else:
                    current = f" > '{option[0]}'"
                    
            print(f"{i:2}.\t{option[1]}" + current)
        #handle input to select which value the user wants to change
        try:
            inp = int(input(colored(
                f"\nSelect the data you wish to set/change [0-{i}]:"
                ,color="light_cyan"
                )))
        except ValueError as e:
            print(f"--> Please enter a number in range 0-{i}")
            continue
        if inp not in range(0, i + 1):
            print(f"--> Please select option in range 0-{i}")
            continue
        match inp:
            case 0:
                break
            case 1:
                smtp_server = input(colored(
                    ">Your mail-providers smtp-server(You can find this domain via google): "
                    ,color="light_cyan"
                ))
                while smtp_server == '':
                    smtp_server = input(colored(
                        ">Your mail-providers smtp-server(You can find this domain via google): "
                        ,color="light_cyan"
                        ))
                options[1][0] = smtp_server
            case 2:
                while True:
                    port_inp = input(colored(
                        ">Your mail-providers smtp-servers port (You can find this via google): "
                        ,color="light_cyan"
                        ))
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
                    options[2][0] = port
                    break
            case 3:
                mail_address = input(colored(
                    ">Your mail-address: "
                    ,color="light_cyan"
                    ))
                while mail_address == '':
                    mail_address = input(colored(
                        ">Your mail-address: "
                        ,color="light_cyan"
                        ))
                options[3][0] = mail_address
            case 4:
                login_options = ["Save data", "Toggle password storage", "username", "password"]
                while True:
                    print("\n================================Login setup================================")
                    print("Login options:")
                    j = 0
                    print(f"{j:2}.\t{login_options[j]}")
                    for l_o in login_options[1:]:
                        if l_o == "Toggle password storage":
                            current = f" > {store_pw}"
                        elif l_o == "username":
                            if username != "":
                                current = f" > '{username}'"
                            else:
                                current = " > undefined"
                        else:
                            current = ""
                        j += 1
                        print(f"{j:2}.\t{l_o}" + current)
                    try:
                        inp = int(input(colored(
                            f"\nSelect the data you wish to set/change [0-{j}]:"
                            ,color="light_cyan"
                            )))
                    except ValueError as e:
                        print(f"--> Please enter a number in range 0-{j}")
                        continue
                    if inp not in range(0, i + 1):
                        print(f"--> Please select option in range 0-{j}")
                    match inp:
                        case 0: #save
                            break
                        case 1: #store_pw
                            while True:
                                print(colored(
                                "Note: This option controls wether the program stores your password between program execution calls."+
                                "\n If set to True, the program will store your mail password"+
                                " (using basic encryption and your operating systems keyring backend)."+
                                "\n If set to False, you will have to re-enter your password everytime you execute the program.",
                                color="yellow"))
                                s_pw_inp = input(colored(
                                    "Do you want the password stored? [y/n]: "
                                    ,color="light_cyan"
                                    ))
                                match s_pw_inp.lower():
                                    case "y":
                                        store_pw = True
                                    case "n":
                                        store_pw = False
                                    case other:
                                        print(f"--> Please choose from [y/n]")
                                        continue
                                break
                        case 2: #username
                            username = input(colored(
                                ">Your mail-provider username: "
                                ,color="light_cyan"
                                ))
                            while username == '':
                                username = input(colored(
                                    ">Your mail-provider username: "
                                    ,color="light_cyan"
                                    ))
                        case 3: #password
                            if store_pw == False:
                                print(colored(f"--> You don't currently have password storage enabled", color="red"))
                                continue
                            if username == '':
                                print(colored(f"--> You need to set a username before you can set a password", color = "red"))
                                continue
                            password = getpass.getpass(prompt=">Your mail-provider password: ")
                            while password == '':
                                password = getpass.getpass(prompt=">Your mail-provider password: ")
                            set_password(password)
                            del password

    if store_pw == False:
        delete_password(debug=False)

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
        restore_datafile_default_template(cfg.ABS_APPDATA_FILE, cfg.APPDATA_FILE_STRUCTURE_TEMPLATE_DICT)
        #restore_appdata_default_template()
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
    data["userdata"]["store_pw"] = store_pw
    #write modified data back into datafile
    try:
        f = open(cfg.ABS_APPDATA_FILE, 'w')
        json.dump(data, f, indent=4)
        f.close()
    except Exception as e:
        mye.eprint(e, f"Write data to \"{cfg.ABS_APPDATA_FILE}\". Something went wrong.\n")
        exit(1)

    print(colored("Userdata setup successfull. Run setup again to change data.", color="green"))
    f = open(cfg.ABS_APPDATA_FILE, 'r')
    #print(json.dumps(json.load(f), indent=4))
    f.close()

    return 0