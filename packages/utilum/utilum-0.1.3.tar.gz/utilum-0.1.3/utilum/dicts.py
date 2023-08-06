def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def mergeMultiple(dictList):
    res={}
    for dl in dictList:
        res=merge(res, dl)
    return res