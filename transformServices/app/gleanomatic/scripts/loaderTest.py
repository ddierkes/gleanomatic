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
        rl = RSLoader('activism','ccl')
    except:
        e = sys.exc_info()[1]
        print(str(e))
    urls = ["https://citizensclimatelobby.org/","https://citizensclimatelobby.org/about-ccl/","https://citizensclimatelobby.org/basics-carbon-fee-dividend/","https://citizensclimatelobby.org/write-congress-about-climate-change/#/7/"]
    rl.addBatch(urls)
    #for url in urls:
     #   rl.addResource("http://climate-walker.org/the-walk")
     #   exit()
    rl.makeDump()
    summary = rl.getSummary()
    print(summary)
    exit()
