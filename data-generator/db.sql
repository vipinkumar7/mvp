CREATE KEYSPACE youtube_videos
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};


CREATE TABLE youtube_videos.stats_data (
    video_id  text,
    trending_date  date,
    title  text,
    channel_title text,
    category_id text,
    publish_time timestamp,
    tags text,
    views int,
    likes int,
    dislikes int,
    comment_count int,
    thumbnail_link text,
    comments_disabled boolean,
    ratings_disabled boolean,
    video_error_or_removed boolean,
    description text,
    country text,
    PRIMARY KEY ( (trending_date,country), publish_time)
) WITH CLUSTERING ORDER BY (publish_time DESC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy', 'compaction_window_size': '1', 'compaction_window_unit': 'DAYS', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';