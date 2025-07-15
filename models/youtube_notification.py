# models/youtube_notification.py
from sqlalchemy import Column, String
from models.notification import Base

class YouTubeNotification(Base):
    __tablename__ = "youtube_notifications"
    youtube_channel_id = Column(String, primary_key=True)
    text_channel_id = Column(String, primary_key=True)
