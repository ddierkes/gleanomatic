# Common Utils
import urllib
from datetime import datetime
import certifi
from urllib3 import PoolManager
import json
from xmltodict import parse
from gleanomatic.GleanomaticErrors import URIException, PostDataException
from gleanomatic.configure import appConfig

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

def getCurrentBatchTimestamp():
    return getBatchTimestamp()
    
    
def getBatchTimestamp(isoDate=None):
    if not isoDate:
        date = datetime.now()
    else:
        date = datetime.strptime(isoDate,'%Y-%m-%dT%H:%M:%S')
    return str(date.year)+str(date.month).zfill(2)+str(date.day).zfill(2)+str(date.hour).zfill(2)+str(date.minute).zfill(2)

def validateRequired(opts,required):
    for key in required:
        if key not in opts:
            raise ValueError(str(key) + " is required!")
    return True
    
def postToLog(log):
    print(log)
    encoded_body = json.dumps(log)
    response = None
    try:
        response = manager.request('POST', appConfig.logURL,
                 headers={'Content-Type': 'application/json'},
                 body=encoded_body,timeout=10)
    except Exception as e:
        print(str(e))
    return True


def postRSData(url,params):
     response = None
     try:
         response = manager.request('POST',url,fields=params,headers=hdrs,timeout=30)
     except ValueError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.HTTPError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.URLError as e:
         raise PostDataException("Could not post data for url: " + str(url) + " ERROR: " + str(e))
     except Exception as e:
         print(str(e))
         return True
     if not response:
         return True
     return response
     
def deleteContent(url):
     response = None
     try:
         response = manager.request('DELETE',url,headers=hdrs,timeout=10.0)
     except ValueError as e:
         raise PostDataException("Could not delete url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.HTTPError as e:
         raise PostDataException("Could not delete url: " + str(url) + " ERROR: " + str(e))   
     except urllib.error.URLError as e:
         raise PostDataException("Could not delete url: " + str(url) + " ERROR: " + str(e))
     if not response:
         return False
     return response

def getEncoding(response):
    encoding = 'utf-8'
    if hasattr(response,'info'):
        contentType = response.info()['Content-Type']
        if '=' in contentType:
            encoding = contentType.split('=')[1]
    return encoding

def getResponse(url):
    response = None
    try:
        response = manager.request('GET',url,headers=hdrs)
    except:
        raise ValueError("Could not load url: " + str(url))
    if not response:
        return False
    return response

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
    content = False
    if hasattr(response,'data'):
        try:
            content = json.loads(response.data.decode(encoding))
        except json.decoder.JSONDecodeError as e:
            print(str(e))
        return content
    return False
    
def getRecordAttr(record,attr_name):
    if isinstance(record,dict):
        if attr_name in record:
            return record[attr_name]
    try:
        result = getattr(record,attr_name)
    except AttributeError:
        return None
    return result

def jsonToDict(jsonStr):
    return json.loads(jsonStr)
    
    
def getStaticPath(resource):
    batchPath = "/static/" + str(resource.sourceNamespace) + "/" + str(resource.setNamespace) + "/" + str(resource.batchTag)
    IDName = np.base_repr(resource.ID, 36)
    IDPath = IDName.zfill(4)
    relativeDir = "/" + str(IDPath[0]) + "/" + str(IDPath[1]) + "/" + str(IDPath[2]) + "/" + str(IDPath[3])
    fullpath = batchPath + relativeDir + "/" + IDName
    return fullpath
    
def getDictFromXML(xml,namespaces=[]):
    try:
        result = parse(xml)
    except Exception as e:
        raise Exception("Could not parse XML to dictionary. ERROR: " + str(e))
    return result
          
 
