import sys
from gleanomatic.RSLoader import RSLoader


if __name__ == "__main__":
    """   
    try:
        rl = RSLoader('mhs','library')
        rl.addResource('http://mohistory.org/research/photographs-prints/')
    except:
        e = sys.exc_info()[1]
        print(str(e))
    """
    try:
        rl = RSLoader('umsl','dl')
    except:
        e = sys.exc_info()[1]
        print(str(e))
    urls = ["http://dl.mospace.umsystem.edu/umsl/oai2?verb=GetRecord&metadataPrefix=mods&identifier=oai:dl.mospace.umsystem.edu/umsl/:umsl_189792",
    "http://dl.mospace.umsystem.edu/umsl/oai2?verb=GetRecord&metadataPrefix=mods&identifier=oai:dl.mospace.umsystem.edu/umsl/:umsl_216457",
    "http://dl.mospace.umsystem.edu/umsl/oai2?verb=GetRecord&metadataPrefix=mods&identifier=oai:dl.mospace.umsystem.edu/umsl/:umsl_47309"]
    rl.addBatch(urls)
    #for url in urls:
     #   rl.addResource("http://climate-walker.org/the-walk")
     #   exit()
    rl.makeDump()
    summary = rl.getSummary()
    print(summary)
    exit()
