import validators
# pip3 install validators

from .lookup import extension


def preprocess_url(input_url):
    output_url=input_url
    has_cleaned="0"
    
    if(output_url[-1]!="/"):
        output_url+="/"
        has_cleaned="1"

    if("?" in output_url):
        output_url=output_url[:output_url.index("?")]
        has_cleaned="1"

    if("//" in output_url):
        output_url=output_url.replace("//", "/")
        has_cleaned="1"

    while(output_url[-2:]=="//"):
        # output_url=output_url.replace("//","/")
        output_url=output_url[:-1]
        has_cleaned="1"

    return output_url,has_cleaned


class urlClass:
    def __init__(self, url=None, protocol=None, hostname=None, 
    pathname=None, url_valid=None, hostname_valid=None,
    url_extension=None, url_type=None):
        self.url=url
        self.protocol=protocol
        self.hostname=hostname
        self.pathname=pathname
        self.url_valid=url_valid
        self.hostname_valid=hostname_valid
        self.url_extension=url_extension
        self.url_type=url_type


def preprocessUrl(url):
    
    while(True):
        if(url[0]=="/"):
            url=url[1:]
            continue
        else:
            break

    if("?" in url):
        qindex=url.index("?")
        url=url[:qindex]
    
    if("#" in url):
        hindex=url.index("#")
        url=url[:hindex]

    if("://" not in url and "//" not in url):
        url="http://"+url

    return url


def validateUrl(url):
    
    valid=validators.url(url)
    
    if(valid==True):
        valid=True
    else:
        valid=False

    return valid


def validateHostName(hostname):
    
    hostname = hostname.lower()
    valid_chars = ".abcdefghijklmnopqrstuvwxyz0123456789"
    hostname_valid = True

    # this is a very loose hostname invalidation
    if(len(hostname)>63):
        hostname_valid=False
        return hostname_valid

    for hn in hostname:
        if(hn in valid_chars):
            continue
        else:
            hostname_valid=False
            return hostname_valid

    return hostname_valid


def getUrlExtension(pathname):
    
    if("." in pathname):
        dindex=pathname.index(".")
        extension=pathname[dindex+1:]
    else:
        extension="None"
    
    return extension


def objectifyUrl(url):
    
    # This objectification is not 100% definate
    # Will be 100% definate very sooon
    url=preprocessUrl(url)
    url_valid=validateUrl(url)
    
    stripped_url=url

    if(url[:7]=="http://"):
        protocol="http"
        stripped_url=stripped_url.replace(url[:7], "")
    elif(url[:8]=="https://"):
        protocol="https"
        stripped_url=stripped_url.replace(url[:8], "")
    elif("://" in url):
        lindex=url.index("://")
        protocol=url[:lindex]
        stripped_url=url[lindex+3:]
    elif("//" in url and "://" not in url):
        lindex=url.index("//")
        protocol=url[:lindex]
        stripped_url=url[lindex+2:]
    else:
        protocol="http"
        stripped_url=stripped_url.replace(url[:7], "")

    if("/" in stripped_url):
        sindex=stripped_url.index("/")
        hostname=stripped_url[:sindex]
        pathname=stripped_url[sindex+1:]
        if(pathname=="/"):
            pathname=""

    else:
        hostname=stripped_url
        pathname=""
    
    hostname_valid=validateHostName(hostname)
    url_extension=getUrlExtension(pathname)    

    if(url_extension in extension.file_extensions):
        url_type = extension.file_extensions[url_extension]
    else:
        url_type = "UNKNOWN"


    urlObject=urlClass(url, protocol, hostname, pathname, url_valid, hostname_valid, url_extension, url_type)
    return urlObject