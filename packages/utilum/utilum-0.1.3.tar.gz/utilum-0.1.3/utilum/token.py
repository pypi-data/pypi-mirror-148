import random
import datetime


def generateRandomStream(moreLen = 16, date = False, allowed = ['l','u','n','s']):
    chars = ""
    output = ""

    lowers = "abcdefghijklmnopqrstuvwxyz"
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    specials = '''~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/'''

    for a in allowed:
        a = a.lower()
        if(a == 'l'): chars += lowers
        if(a == 'u'): chars += uppers
        if(a == 'n'): chars += numbers
        if(a == 's'): chars += specials
    
    if(type(moreLen) == type(1)):
        if((moreLen > 0) == False):
            moreLen = 16
        else:
            pass
    else: moreLen = 16      
    
    for _ in range(moreLen):
        output += chars[random.randint(0,len(chars)-1)]
    
    if(date == True):
        ddns = str(datetime.datetime.now()).replace("-","").replace(" ","").replace(":","").replace(".","")
        output += ddns
    
    return output