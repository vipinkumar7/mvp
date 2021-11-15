import logging
from configparser import ConfigParser
from streamer.StreamUtil import StreamUtil
import schedule
from threading import Thread

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s : %(process)d : %(levelname)s : %(module)s : %(lineno)d : %(message)s')

config_object = ConfigParser()
config_object.read("config/config.ini")
stream_config = config_object["STREAM_CONFIG"]

app = StreamUtil(stream_config["interval"], stream_config["location"])


def drain_thread():
    schedule.every(1).minutes.do(app.load_data)


def data_reader():
    while 1:
        schedule.run_pending()


thread1 = Thread(target=drain_thread, name="thread-1", daemon=True)
thread2 = Thread(target=data_reader, name="thread-2", daemon=True)

thread1.start()
thread2.start()
app.start()