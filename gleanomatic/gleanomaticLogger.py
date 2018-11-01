import logging, sys

from gleanomatic.configure import appConfig
from gleanomatic import Utils

class gleanomaticLogger():
    
    logger = None
    sourceNamespace = None
    setNamespace = None
    batchTag = None

    def __init__(self,sourceNamespace,setNamespace,batchTag):
        self.logger = logging.getLogger(__name__)
        self.sourceNamespace = sourceNamespace
        self.setNamespace = setNamespace
        self.batchTag = batchTag
        formatter = logging.Formatter("%(asctime)s -- LEVEL:%(levelname)s -- FILE:%(filename)s -- LINE:%(lineno)s -- FUNCTION:%(funcName)s -- \n \t MESSAGE:%(message)s")
        file_handler = logging.FileHandler(appConfig.logDir + "/" + appConfig.logFile )
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)
        logLevel = str(appConfig.logLevel).lower()

        if logLevel is "critical":
            self.logger.setLevel(logging.CRITICAL)
        if logLevel is "error":
            self.logger.setLevel(logging.ERROR)
        if logLevel is "warning":
            self.logger.setLevel(logging.WARNING)
        if logLevel is "info":
            self.logger.setLevel(logging.INFO)
        if logLevel is "debug":
            self.logger.setLevel(logging.DEBUG)
        if logLevel is "notset":
            logger.setLevel(logging.NOTSET)
            
    def postLog(self,level,msg):
        fullNamespace = self.sourceNamespace + "/" + self.setNamespace
        log = {
            "MSG": msg,
            "LEVEL": level,
            "NAMESPACE": fullNamespace,
            "BATCHTAG": self.batchTag
        }
        Utils.postToLog(log)

    def notset(self,msg):
        if self.logger.isEnabledFor(logging.NOTSET):
            self.postLog("notset",msg)
            self.logger.notset(msg)

    def info(self,msg):
        if self.logger.isEnabledFor(logging.INFO):
            self.postLog("info",msg)
            self.logger.info(msg)
            
    def debug(self,msg):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.postLog("debug",msg)
            self.logger.debug(msg)
        
    def warning(self,msg):
        if self.logger.isEnabledFor(logging.WARNING):
            self.postLog("warning",msg)
            self.logger.warning(msg)
     
    def error(self,msg):
        if self.logger.isEnabledFor(logging.ERROR):
            self.postLog("error",msg)
            self.logger.error(msg)
            
    def critical(self,msg):
        if self.logger.isEnabledFor(logging.CRITICAL):
            self.postLog("critical",msg)
            self.logger.critical(msg)
