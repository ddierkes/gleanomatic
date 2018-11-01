import gleanomatic.Utils as Utils
from gleanomatic.configure import appConfig

#log = { "LEVEL": "WARN", "MSG": "This is a new message" }

#content = Utils.postToLog(log)

content = Utils.getContent("http://resourcesync/resource")

print(content)

