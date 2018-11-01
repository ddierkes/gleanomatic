import logging, sys
logger = logging.getLogger(__name__)

from gleanomatic.configure import appConfig

# ALL THIS JUST FOR LOGGING
formatter = logging.Formatter("%(asctime)s -- LEVEL:%(levelname)s -- FILE:%(filename)s -- LINE:%(lineno)s -- FUNCTION:%(funcName)s -- \n \t MESSAGE:%(message)s")
file_handler = logging.FileHandler(appConfig.logDir + "/" + appConfig.logFile )
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
logLevel = str(appConfig.logLevel).lower()

if logLevel is "critical":
	logger.setLevel(logging.CRITICAL)
if logLevel is "error":
	logger.setLevel(logging.ERROR)
if logLevel is "warning":
	logger.setLevel(logging.WARNING)
if logLevel is "info":
    logger.setLevel(logging.INFO)
if logLevel is "debug":
	logger.setLevel(logging.DEBUG)
if logLevel is "notset":
    logger.setLevel(logging.NOTSET)

