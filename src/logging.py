from datetime import date
import logging
from src.globalVariables import GlobalVariables


class InitialiseLogging:

    @classmethod
    def setupLogging(cls):
        logging.basicConfig(
            level=logging.DEBUG, format=GlobalVariables.LOG_FORMAT, datefmt=GlobalVariables.DATE_FORMAT)
        GlobalVariables.LOGGER = logging.getLogger()
