import sys
import traceback

def eprint(e, custom_e, vars = list()):
    sys.stderr.write("--------------------------------ERROR--------------------------------\n")
    sys.stderr.write(f'{custom_e}\n')
    print(vars)
    for var in vars:
        sys.stderr.write(f'{var[0]}: {var[1]}\n')
    sys.stderr.write(f"--------------------------------Traceback:--------------------------------\n")
    sys.stderr.write(traceback.format_exc())
    sys.stderr.write(f"--------------------------------Exception raised:--------------------------------\n")
    print(type(e))
    print(e)

class MyE(Exception):
    def __init__(self, e, my_e_string, relevant_vars = list()):
        self.e = e
        self.my_e_string = my_e_string
        self.relevant_vars = list()
        for var in relevant_vars:
            self.relevant_vars.append(var)
class MyError(Exception):
    def __init__(self, e=None, my_error_str="", relevant_vars=list(), tb=None):   #custom error message, tuples of varname string and value, printable error
        self.tb = tb
        self.e = e
        if not my_error_str:
            my_error_str = "No details"
        self.my_error_str = "[MyError]: " + my_error_str
        self.relevant_vars = list()
        for var in relevant_vars:
            self.relevant_vars.append(var)
    def __str__(self):
        #e_str = eprint(self.e, self.my_error_str, ret=True)
        e_str = self.my_error_str
        return e_str


def eprint2(e, custom_e="No custom error given", *vars, ret=False):
    if type(e) == MyError:
        custom_e = e.my_error_str
        vars = e.relevant_vars
        original_e = e.e
        tb = e.tb
    else:
        original_e = e
        tb = True
    out = str()
    out += ("\n\n\n")
    out += ("--------------------------------ERROR--------------------------------\n")
    out += (f'{custom_e}\n')
    for var in vars:
        out += (f'{var[0]}: {var[1]}\n')
    out += (f"--------------------------------Traceback:--------------------------------\n")
    if tb:
        out += tb
    else:
        out += (traceback.format_exc())
    out += (f"--------------------------------Exception raised:--------------------------------\n")
    out += f"{type(e)}\n"
    out += f"{original_e}\n"
    if ret:
        return out
    sys.stderr.write(out)
    '''sys.stderr.write("--------------------------------ERROR--------------------------------\n")
    sys.stderr.write(f'{custom_e}\n')
    for var in vars:
        sys.stderr.write(f'{var[0]}: {var[1]}\n')
    sys.stderr.write(f"--------------------------------Traceback:--------------------------------\n")
    sys.stderr.write(traceback.format_exc())
    sys.stderr.write(f"--------------------------------Exception raised:--------------------------------\n")
    print(type(e))
    print(e)'''

def eprint3(e, custom_e="No custom error given", *vars, ret=False):
    if type(e) == MyError:
        custom_e = e.my_error_str
        vars = e.relevant_vars
        original_e = e.e
        tb = e.tb
    else:
        original_e = e
        tb = None
    out = str()
    out += ("\n\n\n")
    out += ("--------------------------------ERROR--------------------------------\n")
    out += (f'{custom_e}\n')
    for var in vars:
        out += (f'{var[0]}: {var[1]}\n')
    out += (f"--------------------------------Traceback:--------------------------------\n")
    if tb:
        out += tb
    else:
        out += (traceback.format_exc())
    out += (f"--------------------------------Exception raised:--------------------------------\n")
    out += f"{type(e)}\n"
    out += f"{original_e}\n"
    if ret:
        return out
    sys.stderr.write(out)

def new_e(original_e=None, my_error_str="", *relevant_vars, tb=True):
    if tb:
        tb = traceback.format_exc()
    new_mye = MyError(e=original_e, my_error_str=my_error_str, relevant_vars=relevant_vars, tb=tb)
    return new_mye