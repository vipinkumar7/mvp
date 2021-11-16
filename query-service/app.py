import logging
from configparser import ConfigParser
import schedule
from threading import Thread

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s : %(process)d : %(levelname)s : %(module)s : %(lineno)d : %(message)s')

config_object = ConfigParser()
config_object.read("config/config.ini")
stream_config = config_object["SERVICE_CONFIG"]



