from flask import Flask
from flask import g
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ConsistencyLevel, SimpleStatement
import pandas as pd

app = Flask(__name__)


def get_db():
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db


def connect_to_database():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('youtube_videos')
    return session


def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


def compute_percentage(views, likes):
    h = int((likes / views) * 100)
    return h


@app.route("/top_likes/<country>/<date>")
def get_top_likes(country, date):
    session = get_db()
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    query = "select  video_id, likes  from stats_data where country='" + country + "' and " \
                                                                                   "trending_date = '" + date + "'"
    print(query)
    result = session.execute(query)
    df = result._current_rows
    df1 = df.sort_values(by=['likes'], ascending=False)
    return "<p>" + str(df1.iloc[0]) + "</p>"


@app.route("/top_per/<country>/<date>")
def get_top_liked_percentage(country, date):
    session = get_db()
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    query = "select  video_id, views,likes  from stats_data where country='" + \
            country + "' and trending_date = '" + date + "'"
    print(query)
    result = session.execute(query)
    df = result._current_rows
    df['percent'] = df.apply(lambda x: compute_percentage(x['views'], x['likes']), axis=1)
    print(df)
    df1 = df.sort_values(by=['percent'], ascending=False)
    return "<p>" + str(df1.iloc[0]) + "</p>"

