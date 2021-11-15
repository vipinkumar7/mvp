from dataclasses import dataclass


@dataclass()
class YoutubeStart:
    video_id: str
    trending_date: str
    title: str
    channel_title: str
    category_id: str
    publish_time: str
    tags: str
    views: int
    likes: int
    dislikes: int
    comment_count: int
    thumbnail_link: str
    comments_disabled: bool
    ratings_disabled: bool
    video_error_or_removed: bool
    description: str
