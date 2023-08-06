from . import file
from . import string

def searchFileContent(folder_path, search_string_list, isPrint=True, ignoring_extensions = []):
    def controlledPrint(input_stream, isPrint):
        if(isPrint==True):print(input_stream)

    tfft = file.FolderTraversal(folder_path)

    for search_string in search_string_list:        
        controlledPrint("<start> for: "+search_string, isPrint)
        find_dict={}
        temp_list=[]
            
        for itfft in tfft:
            if(string.stringMatchFromList(itfft, ignoring_extensions)==True):
                continue

            else:
                try:
                    if((".html") in itfft):
                        content = file.readFileHtml(itfft)

                    else:
                        content = file.readFile(itfft)

                    contentBig=content.upper()
                    contentSmall=content.lower()
                    contentShredded=contentSmall.replace(" ","").replace("\n","").replace("\t","")
                    search_string_small=search_string.lower()
                    
                    if(search_string in content):
                        input_stream=search_string + " : Organic exists in: " + itfft
                        controlledPrint(input_stream, isPrint)
                        temp_list.append((itfft,"Organic"))

                    if(search_string in contentBig):
                        input_stream= search_string + " : Big exists in: " + itfft
                        controlledPrint(input_stream, isPrint)
                        temp_list.append((itfft,"Big"))

                    if(search_string in contentSmall):
                        input_stream=search_string + " : Small exists in: " + itfft
                        controlledPrint(input_stream, isPrint)
                        temp_list.append((itfft,"Small"))

                    
                    if(search_string_small in contentSmall):
                        input_stream=search_string + " : Flattened exists in: " + itfft
                        controlledPrint(input_stream, isPrint)
                        temp_list.append((itfft,"Flattened"))

                    
                    if(search_string_small in contentShredded):
                        input_stream=search_string + " : Shredded exists in: " + itfft
                        controlledPrint(input_stream, isPrint)
                        temp_list.append((itfft,"Shredded"))

                except:
                    print("Soft Error: ", itfft," :was not read")

        if(len(temp_list)>0):
            find_dict[search_string]=temp_list


        controlledPrint("<end> for: " + search_string + "\n\n", isPrint)
    return find_dict


def vanishPyCache(folder_path):
    vanishing_extension=".pyc"

    tfft = file.FolderTraversal(folder_path)
    pycache_file_count=0
    
    for itfft in tfft:
        input_string=itfft
        if(vanishing_extension==input_string[-4:]):
            pycache_file_count+=1
            file.removeFile(input_string)

    print("Total: {} pycache files deleted from {}".fromat(pycache_file_count, folder_path))
    return None


def vanishPyCacheFolder(folder_path):
    vanishing_extension_file=".pyc"
    vanishing_extension_folder="__pycache__"

    tfft = file.FolderTraversal(folder_path)
    pycache_file_count=0
    
    for itfft in tfft:
        input_string=itfft
        if(vanishing_extension_folder in input_string):
            pycache_folder_path=input_string[:input_string.rindex("/")]
            pycache_file_count+=1

            file.deleteFolder(pycache_folder_path)

    print("Total: {} pycache folders deleted from {}".fromat(pycache_file_count, folder_path))
    return None