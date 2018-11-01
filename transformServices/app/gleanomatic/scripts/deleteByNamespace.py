import sys
import json
from gleanomatic.RSRestClient import RSRestClient

if len(sys.argv) < 2:
    print("USAGE: deleteByNamespace.py {sourceNamespace}/{setNamespace}\n")
    exit()

argParts = sys.argv[1].split("/")
sourceNamespace = argParts[0]
setNamespace = argParts[1]

rc = RSRestClient('http://resourcesync')

offset = 0
count = 20
while(True):
    resultsJ = rc.getResources(offset,count)
    results = json.loads(resultsJ)
    for result in results:
        if result['sourceNamespace'] == sourceNamespace and result['setNamespace'] == setNamespace:
            uri = "http://resourcesync/resource/" + str(result['ID'])
            rc.deleteResource(uri)                                          
            print("deleted: " + str(uri))
    if len(results) < count:
        break
    else:
        offset = offset + count
                                                               
                                                               




