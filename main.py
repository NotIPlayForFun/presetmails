import smtpconnect as smtp
import my_error as mye
import argparse
import sys
import os
import data
import config as cfg
import re
#print(cfg.abs_basedir)
#print(cfg.MAIL_PRESET_FILE)
#document mails sent in docs file with datetime
#multiple presets
#variables can be determined either via commandline or input()
#file prompt for data storage using tkinter
#check if vars in preset actually have a name, currently only detects if they have a name aka var != {}
#support variables inside variables like so {var1 {var2 is here} is here} etc.
#max mail text length is old idea
#change find_body_from_preset so that it does it with regex
#can send mail with empty subject?
#maybe add _from to changable metadata options but have a reminder that
#it only works with the registered userdata if the email has the same provider/username/password
#and to change userdata using --setup if thats not the case
#add header like subject header for receivers to automatically include in receivers list
#add ascii support in variables f.e. \n etc.
class PresetMail():
    '''PresetMail class containing relevant data aswell as the configure_mail_data method that handles configuration until ready to send
     
     metadata (from_, to, subject)all defaults to emtpy objects if not given

     from_ is mail address of sender

     to is a list of receiving addresses

     subject is subject of the email
     if no subject is given at init, defaults to subject from SUBJECT header in preset OR empty string if no such header is found

     preset is the preset string
     can contain subject in first line like so:
      ^SUBJECT=<subject here>$ (where ^=start of line, $=end of line)
      everything after SUBJECT header (OR from line 0 if no such header is present) will become the preset_body
       preset_body can contain variables denoted like so: {name of variable} (soon to be implemented: \{ and \} for raw brackets)

     variable_defs is a list of sublists, each sublist must contain a string with the variable name and a string with the variable value
      f.e.: variable_defs = [["my name", "Dr Jones"], ["your name", "Jones Senior"], [...]] 

     formatted will default to the preset_body with all variables given through variable_defs filled in'''
    def __init__(self, from_="", to =[], subject="", preset="", variable_defs=list(), formatted = ""):#variable defs: list of sublists of length 2 with varname[0] and vardef[1]
        self.from_=from_
        self.to = to
        self.subject = subject
        self.preset = preset
        self.variable_defs = variable_defs
        self.preset_body = find_body_from_preset(self.preset)
        if self.subject == "":
            print("finding subject from preset")
            self.subject = find_subject_from_preset(self.preset)
            if not self.subject:
                print("nah man that aint it")
                self.subject = ""
        if not formatted:
            self.formatted = format_preset(self.preset, self.variable_defs)
        else:
            self.formatted = formatted
    #__str__, mostly unused right now
    def __str__(self):
        s = ""
        s += f">From: {self.from_}\n"
        s += f">To: {self.to}\n"
        s += f">Subject: {self.subject}\n"
        s += f">Preset body:\n"
        s += f"{self.preset_body}\n"
        '''if self.formatted:
            s += f"{self.formatted}"
        else:
            s += f"{self.preset}"'''
        s += f">Defined variables:\n"
        for varname in self.get_preset_varnames():
            for vardef in self.variable_defs:
                if varname == vardef[0]:
                    s += f"{{{varname}}}: '{vardef[1]}'\n"
                    break
                s += f"{{{varname}}}: UNDEFINED\n"
        return s
    def get_preset_varnames(self):
        varname_list = find_preset_vars(self.preset)
        return varname_list
    def get_metadata(self):
        return self.from_, self.to, self.subject
    def configure_mail_data(self):
        _inLoop = True
        #changable metadata options and their respective position in get_metadata(self)
        metadata_options = [["Receiving addresses", 1], ["Subject", 2]] #IMPORTANT: When inserting/removing metadata_options,
                                                                        #the input handling (case matching) further down in the loop
                                                                        #MUST be changed accordingly
        relevant_vardefs = list()   #variables and their definition for display and selection, -1 will be displayed as UNDEFINED
                                    #this is done for convenience and because variable_defs could very well include variable names that are not found in the preset
                                    #and thus can be ignored
        for varname in self.get_preset_varnames():
            relevant_vardefs.append([varname, -1])
            for vardef in self.variable_defs:
                if varname == vardef[0]:
                    relevant_vardefs[len(relevant_vardefs) - 1][1] = vardef[1]
                    break
        while _inLoop:
            print("\n================================Configuration================================")
            s = str()
            s += f"-> From: {self.from_}\n"
            s += f"-> Preset body:\n\n"
            #display preset body
            mybody = str()
            for line in self.preset_body.splitlines():
                print(f"line:{line}")
                mybody = mybody + " >|" + line + "\n"
            s += f"{mybody}\n"
            print(s)
            #display changable values to select from
            print(f"Values:")
            i = 0   #i counts number of changable values (options presented to user without Finishing option)
            print(f"{i:2}.\tReady to send") #finishing option
            #display changable metadata options first
            for option in metadata_options:
                i += 1
                v = self.get_metadata()
                val = v[option[1]]
                if type(val) == list:
                    value = val
                else:
                    value = f"'{val}'"
                print(f"{i:2}.\t{option[0]}: {value}")
            #display all variables detected in the preset and their corresponding value from variable_defs, if defined
            for vardef in relevant_vardefs:
                i += 1
                if vardef[1] != -1:
                    print(f"{i:2}.\t{vardef[0]}: '{vardef[1]}'")        #already defined
                else:
                    print(f"{i:2}.\t{vardef[0]}:'' (empty)")            #value of -1 means undefined
            '''for varname in self.get_preset_varnames():
                printed = False
                for vardef in self.variable_defs:
                    print(f"{varname} == {vardef[0]}")
                    if varname == vardef[0]:
                        print(f"{i:2}.\t{{{varname}}}: '{vardef[1]}'")      #defined vars; we use '' here for clarity
                                                                    #and to avoid possible collision with vars defined as 'UNDEFINED'
                        printed = True
                        break
                if not printed:
                    print(f"{i:2}.\t{{{varname}}}: UNDEFINED")          #undefined vars
                i += 1'''
            #handle input to select which value the user wants to change
            try:
                inp = int(input(f"\nSelect a value to change [0-{i}]:"))
            except ValueError as e:
                print(f"--> Please enter a number in range 0-{i}")
                continue
            if inp not in range(0, i + 1):
                print(f"--> Please select option in range 0-{i}")
                continue
            match inp:
                case 0: #handle finishing option
                    for vardef in relevant_vardefs:
                        if vardef[1] == -1:
                            vardef[1] = ""
                    self.formatted = format_preset(self.preset, relevant_vardefs)
                    _inLoop = False
                case 1: #handle self.to
                    ninp = input(f"Please enter receiving mail addresses (can be multiple seperated by commas): ")
                    _tos = ninp.split(",")
                    ninp_valid = True
                    for j, _to in enumerate(_tos):
                        _to = _to.strip()
                        _tos[j] = _to
                        if len(_to) == 0:
                            print("--> Invalid input")
                            ninp_valid = False
                    if not ninp_valid:
                        continue
                    print(_tos)
                    self.to = _tos
                case 2: #handle self.subject
                    ninp = input(f"Please enter email subject: ")
                    print(ninp)
                    self.subject = ninp.strip()
                case other: #handle variables
                    print(inp - len(metadata_options))
                    vardef = relevant_vardefs[inp - len(metadata_options) - 1]
                    ninp = input(f"Please enter definition for {{{vardef[0]}}}: ")
                    if ninp == "":
                        ninp = -1
                    vardef[1] = ninp
                    print(vardef[1])
                    print(relevant_vardefs)
        return 0

def text_with_line_prefix(text, prefix):
    prefix_text = str()
    for line in text.splitlines():
        prefix_text = prefix_text + prefix + line + "\n"
    return prefix_text

def find_body_from_preset(preset):
    #if preset.endswith("\n"):
    #    print("it does!!!!")
    #else:
    #    print("IT DOESNT!!")
    len_firstline = 0
    for char in preset:
        if char == "\n":
            break
        len_firstline += 1
    firstline = preset.split("\n", 1)[0]
    print(firstline)
    rex = "^SUBJECT\s*=\s*(.+)$"
    _subject = re.findall(rex, firstline)
    if len(_subject) > 0:
        return preset.split("\n", 1)[1]
    return preset
def find_subject_from_preset(preset):
    firstline = preset.split("\n", 1)[0]
    rex = "^SUBJECT\s*=\s*(.+)$"
    _subject = re.findall(rex, firstline)
    if len(_subject) > 0:
        return _subject[0]
    return None
def find_preset_vars(preset):
    rex = "{(.+)}"
    varname_list = re.findall(rex, preset)
    return varname_list

def format_preset(preset, variable_defs):
    for var in variable_defs:
        parts = preset.split(f"{{{var[0]}}}")
        preset = f"{var[1]}".join(parts)
    return preset

def print_readme():
    print(
            '''\
Package for quickly sending custom emails via the commandline using a pre-written template.
The template can contain variables that will be filled in at execution.
'''+f"The preset is stored in \"{cfg.ABS_MAIL_PRESET_FILE}\"."+'''

'''+f"<-----------Example of a {cfg.MAIL_PRESET_FILE}:----------->"+'''
SUBJECT=This is an example preset   ##optional subject header
Hello {person1},

I am writing to you because of {reason}.
Also, did you hear about {thing}?

With kind regards,
{person2}
---------------------------------------------------------
BASIC USAGE:
1!  First, setup your email account using the --setup option.\n'''+
f"2!  Then, write a preset in {cfg.MAIL_PRESET_FILE}"+'''
Variables:
    Write the parts that should differ from mail to mail, aka your variables, like so: {name of variable}
    If you wish to use curly braces elsewhere in your email, mark them with a preceding \"\\\".
    You can then specify these variables when calling the program on the command line.
    If left unspecified, the program will ask for the missing variables.
Subject:
    Optionally, you can declare the subject of your email in your preset like shown in the example.(You can also do this using a variable if u wish)
    Firse choice for subject is always the optional argument [--subject] on the command line
    '''+f"Second choice will be {cfg.MAIL_PRESET_FILE}\n"
+f"    If neither is given, defaults to \"{cfg.DEFAULT_MAIL_SUBJECT}\"\n"+
f"3!  Run {sys.argv[0]}. The easiest way to do this is to simply run the program with no arguments.\n"
"\nHOWEVER, if you DO wish to specify some things already from the program call, you can do this like follows:\n"
"Specifying the receiving_addresses argument (1 or more mail addresses seperated by commas, ignores whitspaces):\n"+
f"\t>{sys.argv[0]} -to receiver1@example.com, receiver2@example.com\n"+ 
"Specifying the subject argument:\n"+
f"\t>{sys.argv[0]} -s Email subject here\n"+
"Specifying the variables argument (variable definitions seperated by commas, does NOT ignore leading or trailing whitespaces on the values assigned to the variables.\n"+
#"If you're feeling advanced, you can use ascii stuff like \n here but not yet lmao"+
f"\t>{sys.argv[0]} -v person1=Mr Fring, person2=Walter, reason=a Business inquiery, thing=the thing that happened\n"+
"Such a program call could look something like this:\n"+
f"\t>{sys.argv[0]} -to receiver1@example.com --vars person1=Mr Fring, "+
            "person2=Walter, reason=a Business inquiery, thing=the thing that happened --subject This is my subject\n"+
f"If you want to "+
"\n(Make sure to scroll up for the entire readme)"
        )

def eval_mail_preset(filepath, *vars):
    try:
        f = open(filepath, 'r')
    except Exception as e:
        raise
    mail = f.read()
    f.close()
    print(mail)

def get_variables_from_cli(argparse_variables):
    '''Return list of variable_defs [ [var_name, var_def], [...] ]
    
    'argparse_variables' is the list of strings given to the '--variables' option as interpreted by argparse.

    Fails program if some variable couldn't be resolved '''

    variable_defs = list()
    v = ("").join(argparse_variables)
    v = v.split(",")

    for arg in v:
        if arg: #if is not '' (this would happen if command ended with comma)
            if "=" not in arg:
                print(f"{__file__}: Couldn't assign \"{arg}\" a value: None given")
                exit(1)
            var_def = arg.split("=")
            variable_defs.append(var_def)
    print("VARS" + f"variable_defs")
    for x in variable_defs:
        if len(x) != 2:
            print(f"Something went wrong while getting variables, {x} is not of length 2")
            exit(1)
    return variable_defs


def main():
    #print(sys.argv)

    #Argparse
    
    parser = argparse.ArgumentParser(description="Package for quickly sending different emails via the commandline using a pre-written template."
                                                    " Use --readme for detailed usage.")
    parser.add_argument("--README", help="Detailed usage and setup description",
                            action="store_true")
    parser.add_argument("--setup", help="Set up or change the mail provider and account the program should use",
                            action="store_true")     #(outdated comment)however, setup and readme will still show up in usage and help
    parser.add_argument("-to", "--receiving_addresses", nargs='+',
                        
                        help="[optional] Mail addresses of receivers, can be multiple seperated by commas, like so:"
                                " -to address1@example.com, address2@example.com, ... If unused, you will be prompted")
    parser.add_argument("-s", "--subject", nargs='+', help=f"[optional] Subject of the email, if none given will default to subject from \"{cfg.MAIL_PRESET_FILE}\","
                                                    f" then you will be prompted")
    parser.add_argument("-v", "--variables", nargs='+', help="[optional] Define the variables you have set in your preset like so: -v var1=peter, var2=some other name, ..."
                                                        " If unused, you will be prompted")
    args = parser.parse_args()
    #print(f"args:{args}")

    #read argparse

    #check if readme or setup
    for arg in sys.argv:    #(outdated comment, only if this check is before parser)so that other args can be optional when using setup or readme
        if arg.lower() == '--readme':
            print_readme()
            exit(0)
        if arg.lower() == '--setup':
            data.setup_userdata()
            exit(0)
    
    #check if userdata is set correctly, if not ask for it
    missing_userdata_list = data.find_missing_userdata()
    if missing_userdata_list:
        print("You seem to be missing some userdata. \nThis is necessary to connect to the mailing server and log into the account you wish to send the emails from."
                "\nRun --setup to register data."
                "\nRun --readme for detailed usage description"
                "\nRun --help for list of commands.")
        exit(1)

    _userdata = data.get_appdata("userdata")
    
    #start defining everything needed for smtp.sendmail_simple

    #get any definitions given in program call
    _to = args.receiving_addresses
    _subject = args.subject
    _variables = args.variables
    if _variables:
        variable_defs = get_variables_from_cli(_variables)  #list of var defs
    else:
        variable_defs = list()
    if _subject:
        subject = " ".join(_subject)
    else:
        subject = str()
    if _to:
        to = _to
    else:
        to = []
        
    #initialize PresetMail object
    try:
        print("Loading in preset...")
        f = open(cfg.ABS_MAIL_PRESET_FILE, 'r')
        preset = f.read()
        f.close()
    except Exception as e:
        mye.eprint(e, f"Failed to open \"{cfg.ABS_MAIL_PRESET_FILE}\", likely missing file")
        exit(1)
    if not preset:
        print(f"Empty preset at {cfg.ABS_MAIL_PRESET_FILE}")
        exit(1)
    mail = PresetMail(from_=_userdata["mail_address"], to=to, subject=subject, preset=preset, variable_defs=variable_defs)
    
    #make PresetMail ask user for configuration
    data_incomplete = True
    while data_incomplete:
        if mail.configure_mail_data() != 0:
            mye.eprint(None, "Something went wrong during email configuration", ("Mail object", mail))
            exit(1)
        if not mail.from_:
            print(f"-->Bad From: Something went wrong with your registered email address. Use --setup to register your email account")
            exit(1)
        if not mail.to:
            print(f"-->Bad receivers list: Please enter one or more receiving mail addresses")
            continue
        if not mail.subject:
            print("Warning: no subject")
            pass
        if not mail.formatted:
            print("Warning: no formatted mail text, something probably went wrong")
            pass
        data_incomplete = False
    
    errs = smtp.sendmail_simple(
        FROM=mail.from_, TO=mail.to,
        SUBJECT=mail.subject,
        TEXT=mail.formatted,
        USERNAME=_userdata["username"],
        PASSWORD=_userdata["password"],
        SMTP_SERVER=_userdata["smtp_server"],
        PORT=587
        #PORT=_userdata["port"]
        )
    #errs = smtp.sendmail_simple('mysmithtest123@gmail.com', 'mysmithtest123@gmail.com', 'TESTSUBJECT NEW', 'THIS IS EXAMPLE TEXT', 'mysmithtest123@gmail.com', 'njwpejtgwypowkib',
    #                                'smtp.gmail.com', 587)
        

    #confirm configuration
    #send mail


    #NEED: FROM, TO, SUBJECT, TEXT, USERNAME, PASSWORD, SMTP_SERVER, PORT = DEFAULT_PORT
    #errs = smtp.sendmail_simple('mysmithtest123@gmail.com', 'mysmithtest123@gmail.com', 'TESTSUBJECT NEW', 'THIS IS EXAMPLE TEXT', 'mysmithtest123@gmail.com', 'njwpejtgwypowkib',
     #                       'smtp.gmail.com', 587)

    #print(errs)

if __name__ == "__main__":
    phrase = f"Now running {os.path.basename(cfg.PROJECT_NAME)}..."
    width = 90
    l_width = (90 - len(phrase)) // 2
    mod = l_width % 2
    r_width = l_width
    buf = "|" + "".join([" " for i in range(l_width - 1)]) + " " * mod + phrase + "".join([" " for i in range(r_width - 1)]) + "|"
    print()
    print("|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|")
    print(f"|::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::|")
    print("|                                                                                        |")
    #print(f"|                               Now running {os.path.basename(cfg.PROJECT_NAME)}...                              |")
    print(buf)
    print("|                                                                                        |")
    print(f"|::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::|")
    print("|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|")
    print()
    print()
    #print(len("|                               Now running Pythonmailer...                              |"))
    #print(len(buf))
    main()
