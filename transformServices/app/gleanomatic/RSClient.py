# RSClient - client to interact with a ResourceSyn endpoint


class RSClient:

    endpointURI = None   

    def __init__(self,endpointURI):
        self.endpointURI = endpointURI

    def getSourceDescription(self):
        pass

    def getResponse(self,uri):
        pass
