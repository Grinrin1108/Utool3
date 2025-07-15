from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# SQLiteを使う場合のDB URL。適宜変更してください
DATABASE_URL = "sqlite:///database.sqlite3"

engine = create_engine(DATABASE_URL, echo=False, future=True)

Session = sessionmaker(bind=engine)

class YouTubeChannel(Base):
    __tablename__ = "youtube_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(String, nullable=False)
    channel_id = Column(String, nullable=False, unique=True)  # YouTubeチャンネルID
    text_channel_id = Column(String, nullable=False)          # Discord通知用テキストチャンネルID

# 初回実行時にテーブルを作成
def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
