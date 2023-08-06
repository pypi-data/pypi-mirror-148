from . import system
import io
import os
from os import path

def removeFile(file_path):
    os.remove(file_path)
    return None

def readFile(file_name):
    with open(file_name, "r", encoding='latin-1') as f:
        text = f.read()
        f.close()
    return text   

def writeFile(file_name,content):
    with open(file_name,'a') as f:
        f.write(content)
        f.close()
    return None

def clearFile(file_name):
    with open(file_name,'w') as f:
        f.close()
    return None

def createFile(file_name):
    with open(file_name,'w') as f:#overrite   
        f.write("")
        f.close()
    return None  

def getSize(inputPath):
    return os.path.getsize(inputPath)

def createFolder(folder_path):
    os.mkdir(folder_path)
    
def deleteFolder(folderPath):
    system.shell('rm -rf {}'.format(folderPath))

def isPathExist(path_name):
    if(path.exists(path_name)):
        return True
    return False

def slashMatch(path,startslash,endslash):
    slashCount=1
    start_index=0
    end_index=len(path)

    for ip,p in enumerate(path):
        if(p=="/"):
            if(endslash!=-1):
                if(slashCount==startslash):
                    start_index=ip+1
                if(slashCount== endslash):
                    end_index=ip
                slashCount+=1
            else:
                if(slashCount==startslash):
                    start_index=ip+1
                slashCount+=1

    return path[start_index:end_index]

def slashMatchSlash(path, startslash,endslash):
    slashCount=1
    start_index=0
    end_index=len(path)

    for ip,p in enumerate(path):
        if(p=="/"):
            if(endslash!=-1):
                if(slashCount==startslash):
                    start_index=ip+1
                if(slashCount== endslash):
                    end_index=ip
                slashCount+=1
            else:
                if(slashCount==startslash):
                    start_index=ip+1
                slashCount+=1
    return path[start_index:end_index]+"/"

def createPath(path):
    path=path.replace('\\',"/")
    slash_count=path.count("/")

    for sc in range(slash_count):
        smp=slashMatchSlash(path, 0,sc+1)
        
        if(isPathExist(smp)==False and isPathExist(smp[:-1])==False):
            if(smp[-1]=="/"):os.mkdir(smp)

    if(isPathExist(path)==False):
        if(path[-1]!="/"):createFile(path)

    return None

def extractFileName(path):
    ind=-1
    while(True):
        p=path[ind]
        if(p=="/"):
            break
        ind-=1

    return path[ind+1:]


def listDirPath(input_path):
    return [input_path+f for f in os.listdir(input_path)]

def listDirPathSlash(input_path):
    return [input_path+f+"/" for f in os.listdir(input_path)]

def isFileEmpty(input_path):
    if(getSize(input_path)==0):return True
    else:return False
    

def folderTraversal(start_path):
    file_list_path=[]
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            fp=fp.replace("\\","/")
            file_list_path.append(fp)
    return file_list_path



# WebPage Handlings

def writeWebPage(fname,html):
    with io.open(fname, "a", encoding="utf-8") as f:
        f.write(html)

def readWebPage(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()
        f.close()
    return text