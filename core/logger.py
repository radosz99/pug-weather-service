import logging

logger_name = "weather-service"
log_file = "debug.log"
logging.basicConfig(filename=logger_name + '-debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Urban Planning")

logger = logging.getLogger(logger_name)

filehandler_dbg = logging.FileHandler(
   logger_name+ '-debug.log',
   mode='w')


def get_logger():
    return logger
