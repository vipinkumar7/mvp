CREATE KEYSPACE youtube_videos
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
