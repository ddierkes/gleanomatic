from gleanomatic.configure import appConfig
from gleanomatic.RSReader import RSReader
from gleanomatic.RSLoader import RSLoader
import gleanomatic.Utils as Utils


class Transformer():
    
    transformURI = None
    transformName = None
    targetSet = None
    targetSourceNS = None
    targetSetNS = None
    reader = None
    loader = None
    logger = None
    
    def __init__(self,sourceNamespace,setNamespace,opts,mode='latest'):
        self.transformURI = appConfig.transformURI
        for key, value in opts.items():
            setattr(self, key, value)
        Utils.validateRequired(opts,['transformName','targetSet'])
        #parse target namespaces out of targetSet
        parts = self.targetSet.split('/')
        self.targetSourceNS = parts[0]
        self.targetSetNS = parts[1]
        self.loader = RSLoader(self.targetSourceNS,self.targetSetNS)
        self.reader = RSReader(sourceNamespace,setNamespace,{"batchTag":self.loader.batchTag},mode)
        self.logger = self.loader.logger
        self.logger.info("initializing Transformer")
  
    def run(self):
        self.reader.loadIDs()
        offset = 0
        while True:
            #batch by 1000
            try:
                batchIDs = self.reader.resourceIDs[offset:1000]
            except IndexError as e:
                break
            uris = map(lambda resID: str(self.transformURI) + str(self.transformName) + "/" + resID,batchIDs)
            uris = list(uris)
            self.loader.addBatch(uris)
            offset = offset + 1000
        self.loader.makeDump()
        return True
   
if __name__ == "__main__":
    pass
