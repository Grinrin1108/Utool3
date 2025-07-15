import feedparser
import discord
import json
import os

CONFIG_FILE = "channel_config.json"

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

async def send_video_notification(bot: discord.Client, guild_id: int, video_info: dict):
    """
    指定したサーバー（guild_id）に、最新動画を通知として送信します
    """
    if not os.path.exists(CONFIG_FILE):
        print("⚠ channel_config.json が存在しません。")
        return

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    channel_id = config.get(str(guild_id))
    if not channel_id:
        print(f"⚠ 通知チャンネル未設定: Guild ID {guild_id}")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"⚠ 通知チャンネルが見つかりません: Channel ID {channel_id}")
        return

    embed = discord.Embed(
        title="📢 新しい動画が公開されました！",
        description=f"[{video_info['title']}]({video_info['link']})",
        color=discord.Color.red()
    )
    embed.set_author(name=video_info["author"])
    embed.set_footer(text=video_info["published"])
    if video_info.get("thumbnail"):
        embed.set_thumbnail(url=video_info["thumbnail"])

    await channel.send(embed=embed)
    print(f"✅ 通知を送信しました: {video_info['title']}")
