from requests import Session
session = Session()

def makePostRequest(url, bodyObject, queryObject = None, headers = None):
    sp = session.post(url, data = bodyObject)
    return sp

def proxyRequest(baseUrl, proxyUrl, body, query, header):
    # baseUrl: original url
    # proxyUrl: proxy url
    
    # Under Construction
    return None