import re
import traceback
import json


class DictToObject:
    def __init__(self, **entries):
        self.dictionary=entries
        self.__dict__.update(entries)
    def __repr__(self):
        return repr(self.dictionary)


def getPrevVariableName(var):
    stack = traceback.extract_stack()
    # filename, lineno, function_name, code = stack[-3]
    _,_,_, code = stack[-3]
    vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
    return vars_name


def jsObject(*args):
    dictObject={}
    var_names=getPrevVariableName(args).replace(" ","").split(",")
    for index,val in enumerate(args):
        dictObject[var_names[index]]=val
        # The below formula needs serious rectification
        # if(type(val)==type(dict())):
        #     dictObject[var_names[index]] = jsObject(val)
        # else:
        #     dictObject[var_names[index]]=val
    dictObject=DictToObject(**dictObject)
    return dictObject


def jsObjectToDict(jsObject):
    dictNew = {}
    for key, val in jsObject.dictionary.items():
        if(type(val)==type(DictToObject())):
            dictNew[key] = jsObjectToDict(val)
        else:
            dictNew[key] = val
    return dictNew


def jsDictToObject(dictionaryHere):
    dictNew = {}
    for key, val in dictionaryHere.items():
        if(type(val)==type(dict())):
            dictNew[key] = jsDictToObject(val)
        else:
            dictNew[key] = val
    return DictToObject(**dictNew)


def parseQueryStringParamsToJson(full_path):
    qs={}
    if("?" in full_path):
        query=full_path[full_path.index("?")+1:]
        query_tups=query.split("&")
        for qrt in query_tups:
            key,val=qrt.split("=")
            qs[key]=val
    return json.dumps(qs)