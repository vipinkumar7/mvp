import logging
from os import listdir
from os.path import isfile, join
import pandas as pd
from cassandra.cluster import Cluster
from streamer.BlockingQueue import BlockingQueue
from streamer.pojo import YoutubeStart


class StreamUtil:

    def __init__(self, interval, location):
        self._interval = interval
        self._location = location
        # self.cluster = Cluster(['127.0.0.1'])
        # self.cluster.connect('youtube_videos')
        self._queue = BlockingQueue(200)

    def load_data(self):
        logging.info('draining queue ')
        item = self._queue.dequeue()
        print(item)
        logging.info("item drained" )

    def start(self):
        logging.info('Starting data generator')
        onlyfiles = [f for f in listdir(self._location) if isfile(join(self._location, f)) and f.endswith(".csv")]
        for csv in onlyfiles:
            print(csv)
            df = pd.read_csv(join(self._location, csv), encoding='utf-8', sep=',', quotechar='"', error_bad_lines=False)
            for index, row in df.iterrows():
                obj = YoutubeStart(row['video_id'],
                                   row['trending_date'],
                                   row['title'],
                                   row['channel_title'],
                                   row['category_id'],
                                   row['publish_time'],
                                   row['tags'],
                                   row['views'],
                                   row['likes'],
                                   row['dislikes'],
                                   row['comment_count'],
                                   row['thumbnail_link'],
                                   row['comments_disabled'],
                                   row['ratings_disabled'],
                                   row['video_error_or_removed'],
                                   row['description'])
                self._queue.enqueue(obj)
