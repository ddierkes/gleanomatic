
class URIException(Exception):
    
    def __init__(self,msg,error):
        message  = str(msg) + " " + str(error)
        super().__init__(message)

class PostDataException(Exception):
	pass

class RSPathException(Exception):
	pass

class TargetURIException(URIException):
    pass
        
        
class BadResourceURL(URIException):
    pass
   

class AddResourceError(Exception):
    pass
    
class AddDumpException(Exception):
    pass

class AddCapabilityException(Exception):
    pass

