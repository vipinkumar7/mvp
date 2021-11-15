import logging
from os import listdir
from os.path import isfile, join
import pandas as pd
from cassandra.cluster import Cluster
from streamer.BlockingQueue import BlockingQueue
from streamer.pojo import YoutubeStart
from datetime import datetime


class StreamUtil:

    def __init__(self, interval, location):
        self._interval = interval
        self._location = location
        self.cluster = Cluster(['127.0.0.1'])
        self.session = self.cluster.connect('youtube_videos')
        self._queue = BlockingQueue(200)

    def load_data(self):
        logging.info('draining queue ')
        item = self._queue.dequeue()
        self.session.execute(
            """
            INSERT INTO users (video_id, trending_date, title, channel_title, category_id, publish_time, tags, views, 
            likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, 
            video_error_or_removed, description, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s , %d, %d, %d, %d ,%s, %s, %s, %s, %s ,%s )
            """,
            (item.video_id, datetime.strptime(item.trending_date, '%y.%d.%m'), item.title, item.channel_title,
             item.category_id, datetime.strptime(item.publish_time, '%Y-%m-%dT%H:%M:%S.%fZ'),
             item.tags, int(item.views),
             int(item.likes), int(item.dislikes), int(item.comment_count), item.thumbnail_link, item.comments_disabled,
             item.ratings_disabled,
             item.video_error_or_removed, item.description, item.country)
        )
        print(item)
        logging.info("item drained")

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
                                   row['description'],
                                   csv[:2])
                self._queue.enqueue(obj)
