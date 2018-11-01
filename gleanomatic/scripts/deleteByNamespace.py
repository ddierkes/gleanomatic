import sys
import json
from datetime import datetime

from gleanomatic import Utils
import gleanomatic.gleanomaticLogger as gl
from gleanomatic.RSRestClient import RSRestClient

if len(sys.argv) < 2:
    print("USAGE: deleteByNamespace.py {sourceNamespace}/{setNamespace}\n")
    exit()

localhost = "http://localhost:81/"
argParts = sys.argv[1].split("/")
sourceNamespace = argParts[0]
setNamespace = argParts[1]

now = datetime.now()
batchTag = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+ "_deletion"
        
logger = gl.gleanomaticLogger(sourceNamespace,setNamespace,batchTag)
rc = RSRestClient('http://resourcesync',logger)

ResURL = 'http://resourcesync/RS/' + str(sourceNamespace) + "/" + str(setNamespace) + "/resourcelistindex.json"

ResListContents = Utils.getContent(ResURL)

resList = json.loads(ResListContents)

for res in resList['sitemapindex']['sitemap']:
    if 'rs:ln' in res:
        if '@type' in res['rs:ln']:
            if str(res['rs:ln']['@type']).lower() == 'application/json':
                subResListURL = res['rs:ln']['@href']
                subResListURL = subResListURL.replace(localhost,'http://resourcesync/')
                subResContents = Utils.getContent(subResListURL)
                subResList = json.loads(subResContents)
                for url in subResList['urlset']['url']:
                    if 'rs:ln' in url:
                        if '/resource/' in url['rs:ln']['href']:
                            resPath = url['rs:ln']['href']
                            uri = 'http://resourcesync' + str(resPath)
                            rc.deleteResource(uri)
                            print("deleted: " + str(uri))
