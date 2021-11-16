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


@app.route("/top_likes/<date>")
def get_top_likes(date):
    session = get_db()
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    query = "select  video_id, likes  from stats_data where country='MX' and " \
            "trending_date = " + "'" + date + "'"
    print(query)
    result = session.execute(query)
    df = result._current_rows
    df1 = df.sort_values(by=['likes'], ascending=False)
    return "<p>" + str(df1.iloc[0]) + "</p>"
