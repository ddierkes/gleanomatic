import os
import json
from multiprocessing import Pool 
from datetime import datetime
import time

from gleanomatic.configure import appConfig
import gleanomatic.RSRestClient as rc
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, RSPathException, TargetURIException, AddDumpException, AddCapabilityException
import gleanomatic.gleanomaticLogger as gl

logger = gl.logger

# RSLoader - add external resources and capabilities to an ResourceSync endpoint


class RSLoader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    setNamespace = None
    client = None
    createDump = False
    batchTag = None

    def __init__(self,sourceNamespace,setNamespace,opts={}):
        logger.info("Initializing RSLoader")
        self.targetURI = appConfig.targetURI
        self.targetEndpoint = rc.RSRestClient(self.targetURI)
        self.sourceNamespace = sourceNamespace
        self.setNamespace = setNamespace
        self.createDump = appConfig.createDump
        now = datetime.now()
        self.batchTag = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)+str(now.minute).zfill(2)
        for key, value in opts.items():
            setattr(self, key, value)

    def run(self):
        pass

    def msg(self,message):
        return "[batchTag:" + str(self.batchTag) + "] " + str(message)

    def addResource(self,uri):
        contents = None
        try:
            contents, message = self.targetEndpoint.addResource(uri,self.sourceNamespace,self.setNamespace,self.batchTag)
        except Exception as e:
            logger.warning(self.msg("Could not add resource uri: " + str(uri)) + " ERROR: " + str(e))
        if not contents:
            logger.warning(self.msg("No contents returned for uri: " + str(uri)))
        return contents
        
    def addBatch(self, uris):
        pool = Pool()
        pool.map(self.addResource, uris)
        pool.close() 
        pool.join()
        
    def deleteResource(self,uri):
        pass

    def addCapability(self,url,capType):
        contents = None
        try:
            contents, message = self.targetEndpoint.addCapability(url,self.sourceNamespace,self.setNamespace,capType)
        except Exception as e:
            logger.critical(self.msg("Could not add capability."))
            raise AddCapabilityException("Could not add capability",e)
        return contents
    
    def makeDump(self):
        if self.createDump:
            try:
                contents = self.targetEndpoint.addDump(self.batchTag,self.sourceNamespace,self.setNamespace)
            except Exception as e:
                logger.critical(self.msg("Could not add dump."))
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
                        logger.critical(self.msg("Too many retries waiting for " + str(zipURI)))
                        raise AddDumpException("Too many retries waiting for " + str(zipURI))
                    continue
                if uriResponse:
                    logger.info("Found zipURI.")
                    break
            result = self.addCapability(zipURI,'dump')    
            return result
        return False
        
    def getSummary(self):
        manifest = self.targetEndpoint.getManifest(self.batchTag,self.sourceNamespace,self.setNamespace)
        return manifest

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

