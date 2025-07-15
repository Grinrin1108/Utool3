import feedparser

def get_latest_video(channel_id):
    """
    指定した YouTube チャンネルID から最新動画を取得
    """
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return None

    entry = feed.entries[0]
    return {
        "title": entry.title,
        "link": entry.link,
        "author": entry.author,
        "published": entry.published,
        "summary": entry.summary,
        "thumbnail": entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None
    }
