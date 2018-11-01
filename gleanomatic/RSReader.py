from gleanomatic.configure import appConfig
import gleanomatic.RSRestClient as rc
import gleanomatic.Utils as Utils
from gleanomatic.GleanomaticErrors import BadResourceURL, RSPathException, TargetURIException, AddDumpException, AddCapabilityException
import gleanomatic.gleanomaticLogger as gl

# RSReader - get RS resources and capabilities from a ResourceSync endpoint

class RSReader:

    targetURI = None   
    targetEndpoint = None
    sourceNamespace = None
    setNamespace = None
    logger = None
    mode = 'latest'
    resourceIDs = []
    index = []
    currentIndexKey = 0

    def __init__(self,sourceNamespace,setNamespace,opts={},mode='latest'):
        for key, value in opts.items():
            setattr(self, key, value)
        if not self.batchTag:
            self.batchTag = Utils.getCurrentBatchTimestamp()
        self.logger = gl.gleanomaticLogger(sourceNamespace,setNamespace,self.batchTag)
        self.logger.info("Initializing RSReader")
        self.targetURI = appConfig.targetURI
        self.targetEndpoint = rc.RSRestClient(self.targetURI,self.logger)
        self.sourceNamespace = sourceNamespace
        self.setNamespace = setNamespace
        self.mode = mode
        
    def loadIDs(self):
        if self.mode == 'all':
            self.index = self.targetEndpoint.loadResourceListIndex(self.sourceNamespace,self.setNamespace)
            while True:
                ids = self.getNextIDs()
                if not ids:
                    break
                else:
                    for resourceID in ids:
                        self.resourceIDs.append(resourceID)    
        elif self.mode == 'latest':
            latestTag = None
            batchTags = []
            capURLs = self.targetEndpoint.loadCapabilityList(self.sourceNamespace,self.setNamespace)
            if capURLs:
                for record in capURLs:
                    thisTag = None
                    if 'rs:md' in record:
                        if '@until' in record['rs:md']:
                            thisTag = Utils.getBatchTimestamp(record['rs:md']['@until'])
                    else:
                        #is it a zip file named by batchtag?
                        if '.zip' in record['loc']:
                            parts = record['loc'].split('/')
                            filename = parts[-1]
                            thisTag = filename.replace('.zip','') 
                    if thisTag:
                        numTag = int(thisTag)
                        batchTags.append(numTag)
                batchTags.sort()
                latestTag = batchTags[-1]
            ids = self.targetEndpoint.loadManifestIDs(self.sourceNamespace,self.setNamespace,latestTag)
            for resourceID in ids:
                self.resourceIDs.append(resourceID)    
        else:
            print("Unknown mode: " + str(mode))
        return True
        
    def getNextIDs(self):
        resourceIDs = None
        try:
            itemsURL = self.index[self.currentIndexKey]
        except IndexError as e:
            return False
        resourceIDs = self.targetEndpoint.loadResourceListIDs(itemsURL)
        self.currentIndexKey = self.currentIndexKey + 1
        return resourceIDs

    

if __name__ == "__main__":
    pass
