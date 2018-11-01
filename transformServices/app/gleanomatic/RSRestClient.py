# RSRestClient - client to interact with a RSEngine REST endpoint
import urllib.request
import urllib.parse
import json

import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, AddResourceError, AddDumpException
import gleanomatic.gleanomaticLogger as gl

logger = gl.logger

class RSRestClient:

    endpointURI = None
    resourceURI = None
    capabilityURI = None 

    def __init__(self,endpointURI):
        logger.info("Initializing RSRestClient")
        #ensure that there is a trailing slash on the endpoint
        if endpointURI[-1] != "/":
            endpointURI = str(endpointURI) + "/" 
        self.endpointURI = endpointURI
        self.resourceURI = str(self.endpointURI) + "resource"
        logger.info("Checking resourceURI: " + str(self.resourceURI))
        try:
            Utils.checkURI(self.resourceURI)
        except Exception as e:
            logger.critical("ResourceURI did not validate: " + str(self.resourceURI) + " ERROR:" + str(e))
            raise TargetURIException("ResourceURI did not validate: " + str(self.resourceURI) ,e)
        self.capabilityURI = str(self.endpointURI) + "capability"

        
    def getMessage(self,record):
        message = Utils.getRecordAttr(record,'message')
        msg = Utils.getRecordAttr(record,'msg')
        if message:
            return message
        if msg:
            return msg
        return None
   
    def addResource(self,uri,sourceNamespace,setNamespace,batchTag=None):
        logger.info("Adding resource with uri: " + str(uri))
        record = None
        message = None
        try:
            Utils.checkURI(uri)
        except URIException as e:
            raise Exception("Resource uri did not validate. uri: " + str(uri))
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': uri}
        if batchTag:
            params['batchTag'] = batchTag
        try:
            response = Utils.postRSData(self.resourceURI,params)
        except Exception as e:
            raise BadResourceURL("Could not add resource. resourceURI: " + str(self.resourceURI), e)
        record = Utils.getJSONFromResponse(response)
        message = self.getMessage(record) 
        if message:
            logger.warning(message)
        return record, message
        
    def addDump(self,batchTag,sourceNamespace,setNamespace):
        response = None
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'batchTag': batchTag}
        try:
            response = Utils.postRSData(self.capabilityURI,params)
        except Exception as e:
            raise AddDumpException("Could not post dump.",e)
        d = Utils.getJSONFromResponse(response)
        d = self.convertToRSDomain(d)
        return d
 
    def convertToRSDomain(self,url):
        if '/static/' in str(url):
            parts = str(url).split('/static/')
            url = 'http://resourcesync/static/' + parts[1]
        return url
        
    def deleteResource(self,uri):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        try:
            req = urllib.request.Request(
                uri,
                headers=headers,
                method='DELETE'
            )
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            raise BadResourceURL(uri,e)
        d = response.read()
        return d

    def getResources(self,offset=0,count=20):
        url = self.endpointURI + str("resource")
        url = str(url) + "?offset=" + str(offset) + "&count=" + str(count)
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        f = urllib.request.urlopen(url)
        contents = Utils.getContent(url)
        return contents
        
    def getManifest(self,batchTag,sourceNamespace,setNamespace):
        url = self.endpointURI + "/static/" + str(sourceNamespace) + "/" + str(setNamespace) + "/" + str(batchTag) + "/manifest"
        urlCheck = Utils.checkURI(url)
        if not urlCheck:
            return False
        contents = Utils.getContent(url)
        return contents

    def addCapability(self,capURL,sourceNamespace,setNamespace,capType):
        logger.info("Adding capability with url:" + str(capURL))
        record = None
        message = None
        try:
            Utils.checkURI(capURL)
        except Exception as e:
            logger.warning("Capability URL did not validate. url: " + str(capURL) + " ERROR: "  + str(e))
            raise Exception("Capability URL did not validate. url: " + str(capURL) + " ERROR: "  + str(e))
        params = {'sourceNamespace' : sourceNamespace, 'setNamespace' : setNamespace, 'uri': capURL, 'capabilityType':capType}
        try:
            response = Utils.postRSData(self.capabilityURI,params)
        except Exception as e:
            logger.critical("Could not add capability. capabiltyURI: " + str(self.capabilityURI) + " ERROR: " + str(e))
            raise BadResourceURL(str(e))
        record = Utils.getJSONFromResponse(response)
        message = self.getMessage(record) 
        if message:
            logger.warning(message)
        return record, message

    def deleteCapability(self,capURL,sourceNamespace,setNamespace):
        pass

    def getCapabilities(self,**kwargs):
        pass

    def what(self):
        print("This is a RSRestClient.")

