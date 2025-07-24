import os
import glob
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread
import discord
from discord.ext import commands

from models.youtube_db import Base, engine, Session
from models.youtube_notification import YouTubeNotification
from models.notification import Notification

from models.youtube import get_latest_video
from utils.youtube_checker import start_youtube_check
from datetime import datetime


# ====== 環境変数読み込み ======
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Discord Bot の設定 ======
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== Flask サーバー設定 ======
app = Flask(__name__)
post_count = 0

@app.route("/", methods=["GET"])
def home():
    return '<a href="https://note.com/exteoi/n/n0ea64e258797">解説はこちら</a> にあります。'

@app.route("/", methods=["POST"])
def webhook():
    global post_count
    print("📩 Received POST request.")
    post_count += 1

    if post_count == 10:
        asyncio.run(trigger())
        post_count = 0

    return "POST response by Railway"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

# ====== 起動時処理 ======
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    activity = discord.CustomActivity(name="いたずら中😈")
    await bot.change_presence(activity=activity)
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")
    start_youtube_check(bot)

# ====== Nerf処理用メモリ保持 ======
nerfed_users = set()

# ====== メッセージ投稿防止 ======
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in nerfed_users:
        try:
            await message.delete()
            print(f"🛑 Nerfed user {message.author} のメッセージを削除しました。")
        except discord.Forbidden:
            print("⚠️ メッセージ削除できません（パーミッション不足）")
        return
    await bot.process_commands(message)

# ====== メッセージ編集防止 ======
@bot.event
async def on_message_edit(before, after):
    if after.author.id in nerfed_users:
        try:
            await after.delete()
            print(f"✏️ Nerfed user {after.author} の編集済メッセージを削除しました。")
        except discord.Forbidden:
            print("⚠️ 編集済みメッセージ削除できません")
            
# ====== リアクション禁止（追加） ======
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id in nerfed_users:
        channel = bot.get_channel(payload.channel_id)
        if channel:
            try:
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, discord.Object(id=payload.user_id))
                print(f"⛔ Nerfed user のリアクションを削除")
            except Exception as e:
                print("⚠️ リアクション削除失敗", e)

# ====== リアクション禁止（削除） ======
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id in nerfed_users:
        print("⛔ Nerfed user のリアクション削除もブロック対象（ただし無視するだけ）")

# ====== コマンドハンドラ読み込み ======
async def load_commands():
    for filepath in glob.glob("commands/*.py"):
        name = os.path.splitext(os.path.basename(filepath))[0]
        if name == "__init__":
            continue
        print(f"🔄 Loading command: {name}")
        await bot.load_extension(f"commands.{name}")

# ====== YouTube更新トリガー処理（10回Webhookで呼ばれた時用） ======
async def trigger():
    print("🔔 Trigger called! (10 POSTs received)")
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    video = get_latest_video(channel_id)
    if video:
        print("📹 最新動画:")
        print("タイトル:", video['title'])
        print("URL:", video['link'])
    else:
        print("❌ 動画が取得できませんでした。")

# ====== VC参加通知 ======
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel or not after.channel:
        return

    session = Session()
    notifs = session.query(Notification).filter_by(
        guild_id=str(member.guild.id),
        voice_channel_id=str(after.channel.id)
    ).all()
    session.close()

    for notif in notifs:
        text_channel = member.guild.get_channel(int(notif.text_channel_id))
        if text_channel:
            await text_channel.send(f"🔔 {member.display_name} さんが <#{after.channel.id}> に入りました！")

# ====== YouTube通知チェックループ ======
last_published_dict = {}

async def check_youtube_updates():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now().hour
        if 0 <= now < 7:
            print("🌙 深夜時間帯（0〜7時）なのでスキップ中...")
            await asyncio.sleep(300)
            continue

        print("🔁 Checking YouTube updates...")
        session = Session()
        notifs = session.query(YouTubeNotification).all()
        session.close()

        for notif in notifs:
            video = get_latest_video(notif.youtube_channel_id)
            if not video:
                continue

            last_time = last_published_dict.get(notif.youtube_channel_id)
            if last_time == video["published"]:
                continue

            last_published_dict[notif.youtube_channel_id] = video["published"]
            text_channel = bot.get_channel(int(notif.text_channel_id))
            if text_channel:
                await text_channel.send(
                    f"📢 新しい動画が投稿されました！\n"
                    f"**{video['title']}**\n{video['link']}"
                )

        await asyncio.sleep(300)

# ====== 起動処理 ======
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    keep_alive()

    async def start_bot():
        await load_commands()
        asyncio.create_task(check_youtube_updates())
        await bot.start(TOKEN)

    asyncio.run(start_bot())
