import sys
import logging

from configure import sources
from gleanomatic import OAILoader as ol

def oaiIngest(sourceNamespace,setNamespace):
    try:
        sourceConfig = sources[sourceNamespace]
        setConfig = sourceConfig['sets'][setNamespace]
    except AttributeError:
        raise ValueError("No config found for given namespaces")
    oaiLoader = ol.OAILoader(sourceNamespace,setNamespace,setConfig)
    oaiLoader.run()
    return oaiLoader.getSummary()
    

if __name__ == "__main__":
    sourceID = sys.argv[1]
    if not "." in sourceID:
        raise Exception("Incorrect identifier format")
    parts = sourceID.split(".")
    sourceNamespace = parts[0]
    setNamespace = parts[1]
    result = oaiIngest(sourceNamespace,setNamespace)
    logging.info(result)
    

