#from gleanomatic import Utils
from gleanomatic.configure import appConfig

class Service():

    def _init_(self):
        pass

    # should be overridden in a subclass
    def run(self,resPath):
        pass

    def loadContent(self,resPath):
        return {"id":1,"body": "This is some content"}
