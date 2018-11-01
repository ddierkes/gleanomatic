# Common Utils
import urllib
import certifi
from urllib3 import PoolManager
import json
from gleanomatic.GleanomaticErrors import URIException, PostDataException
from gleanomatic.configure import appConfig
import gleanomatic.gleanomaticLogger as gl

logger = gl.logger
userAgent = appConfig.userAgent
hdrs = {"User-Agent": userAgent}

manager = PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

def checkURI(uri):
    response = None
    try:
        response = manager.request('GET',uri,headers=hdrs)
    except urllib.error.HTTPError as e:
        raise URIException("HTTPError for uri: " + str(uri),e)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as e:
        raise URIException(uri,e)
    finally:
        if not response:
            return False
        return True

def validateRequired(opts,required):
    for key in required:
        if key not in opts:
            raise ValueError(str(key) + " is required!")
    return True

def postRSData(url,params):
     response = None
     try:
         response = manager.request('POST',url,fields=params,headers=hdrs,timeout=4.0)
     except ValueError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.HTTPError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.URLError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))
     if not response:
         return False
     return response

def getEncoding(response):
    encoding = 'utf-8'
    contentType = response.info()['Content-Type']
    if '=' in contentType:
        encoding = contentType.split('=')[1]
    return encoding

def getContent(url):
    response = None
    try:
        response = manager.request('GET',url,headers=hdrs)
    except:
        raise ValueError("Could not load content from url: " + str(url))
    if not response:
        return False
    encoding = getEncoding(response)
    return response.data.decode(encoding)
    
def getJSONFromResponse(response):
    encoding = getEncoding(response)
    return json.loads(response.data.decode(encoding))
    
def getRecordAttr(record,attr_name):
    if isinstance(record,dict):
        if attr_name in record:
            return record[attr_name]
    try:
        result = getattr(record,attr_name)
    except AttributeError:
        return None
    return result
 
