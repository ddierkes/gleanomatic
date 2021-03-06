import os
import json
from multiprocessing import Pool, cpu_count
from datetime import datetime
import time

from gleanomatic.configure import appConfig
import gleanomatic.RSRestClient as rc
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, RSPathException, TargetURIException, AddDumpException, AddCapabilityException
import gleanomatic.gleanomaticLogger as gl

def addFromBatch(datum):
    parts = datum.split("||")
    params = {'uri': parts[0], 'sourceNamespace' : parts[1], 'setNamespace' : parts[2], 'batchTag': parts[3]}
    resourceURI = str(appConfig.targetURI) + "/resource"
    namespace = str(parts[1]) + "/" + str(parts[2])
    response = Utils.postRSData(resourceURI,params)
    respJ = Utils.getJSONFromResponse(response)
    if not respJ:
        print("Failed to post " + str(parts[0]))
        Utils.postToLog({"LEVEL":"WARNING",
                         "MSG": "Failed to post " + str(parts[0]), 
                         "NAMESPACE": namespace,
                         "BATCHTAG": str(parts[3])})
        return True
    if 'ID' in respJ:
        print("Posted " + str(parts[0]))
        Utils.postToLog({"LEVEL":"INFO",
                         "MSG": "Posted " + str(parts[0]) + " to resource/" + str(respJ['ID']), 
                         "NAMESPACE": namespace,
                         "BATCHTAG": str(parts[3])})
    else:
        print("Failed to post " + str(parts[0]))
        Utils.postToLog({"LEVEL":"WARNING",
                         "MSG": "Failed to post " + str(parts[0]), 
                         "NAMESPACE": namespace,
                         "BATCHTAG": str(parts[3])})
    return True

# RSLoader - add external resources and capabilities to an ResourceSync endpoint

class RSLoader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    setNamespace = None
    client = None
    createDump = False
    batchTag = None
    logger = None

    def __init__(self,sourceNamespace,setNamespace,opts={}):
        self.batchTag = Utils.getCurrentBatchTimestamp()
        self.logger = gl.gleanomaticLogger(sourceNamespace,setNamespace,self.batchTag)
        self.logger.info("Initializing RSLoader")
        self.targetURI = appConfig.targetURI
        self.targetEndpoint = rc.RSRestClient(self.targetURI,self.logger)
        self.sourceNamespace = sourceNamespace
        self.setNamespace = setNamespace
        self.createDump = appConfig.createDump
       
        for key, value in opts.items():
            setattr(self, key, value)

    def run(self):
        pass

    def addResource(self,uri):
        contents = None
        try:
            contents, message = self.targetEndpoint.addResource(uri,self.sourceNamespace,self.setNamespace,self.batchTag)
        except Exception as e:
            self.logger.warning("Could not add resource uri: " + str(uri) + " ERROR: " + str(e))
        if not contents:
            self.logger.warning("No contents returned for uri: " + str(uri))
        return contents
        
    def addBatch(self, uris):
        data = []
        for uri in uris:
            data.append(str(uri) + "||" + str(self.sourceNamespace) + "||" + str(self.setNamespace) + "||" + str(self.batchTag))
        psize = cpu_count()*1
        pool = Pool(psize)
        pool.map(addFromBatch,data)
        pool.close() 
        pool.join()
        
    def deleteResource(self,uri):
        pass

    def addCapability(self,url,capType):
        contents = None
        try:
            contents, message = self.targetEndpoint.addCapability(url,self.sourceNamespace,self.setNamespace,capType)
        except Exception as e:
            self.logger.critical("Could not add capability.")
            raise AddCapabilityException("Could not add capability",e)
        return contents
    
    def makeDump(self):
        if self.createDump:
            try:
                contents = self.targetEndpoint.addDump(self.batchTag,self.sourceNamespace,self.setNamespace)
            except Exception as e:
                self.logger.critical("Could not add dump.")
                raise AddDumpException("Could not add dump.",e)
            zipURI = contents
            while True:
                retries = 0
                try:
                    uriResponse = Utils.checkURI(zipURI)
                except Exception as e:
                    #allow up to 1 hour for zip creation - sleep 60 seconds and try 60 times
                    time.sleep(60)
                    retries = retries + 1
                    if retries > 60:
                        self.logger.critical("Too many retries waiting for " + str(zipURI))
                        raise AddDumpException("Too many retries waiting for " + str(zipURI))
                    continue
                if uriResponse:
                    self.logger.info("Found zipURI.")
                    break
            result = self.addCapability(zipURI,'dump')    
            return result
        return False
        
    def getSummary(self):
        manifest = self.targetEndpoint.getManifest(self.batchTag,self.sourceNamespace,self.setNamespace)
        return manifest

if __name__ == "__main__":
    pass
