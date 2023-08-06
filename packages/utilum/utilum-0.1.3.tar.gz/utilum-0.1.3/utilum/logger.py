import re
import traceback

from .attribute import Text


def getPrevVariableName(var):
    stack = traceback.extract_stack()
    _,_,_, code = stack[-3]
    vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
    return vars_name


def debug(*args):
    var_names=getPrevVariableName(args).replace(" ","").split(",")
    streamValue = ""
    for index,val in enumerate(args):
        streamValue += f'''{Text.Color.fg.cyan}{var_names[index]}{Text.Color.fg.endc}''' + ": " + str(val)
        if(index != len(args)-1):
            streamValue += "\n"

    print(streamValue)
    return streamValue