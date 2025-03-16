from langchain_community.chat_message_histories import SQLChatMessageHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
import uuid

# 定义基础模型
Base = declarative_base()

# 自定义消息表模型
class CustomMessageHistory(Base):
    __tablename__ = "message_history"
    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)  # 添加 user_id 字段
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# 自定义 SQLChatMessageHistory
class CustomSQLChatMessageHistory(SQLChatMessageHistory):
    def __init__(self, session_id: str, user_id: str, connection):
        super().__init__(session_id, connection)
        self.user_id = user_id
        self.Base = Base
        self.Base.metadata.create_all(self.engine)  # 创建表结构

    def add_message(self, message):
        # 添加消息时，同时存储 user_id
        Session = sessionmaker(bind=self.engine)  # 使用 session_maker
        with Session() as session:
            session.add(CustomMessageHistory(
                id=str(uuid.uuid4()),
                session_id=self.session_id,
                user_id=self.user_id,
                message=message.content,
                type=message.type
            ))
            session.commit()

# 创建 SQLAlchemy 引擎
engine = create_engine("sqlite:///chat_history.db")

# 使用自定义类
chat_history = CustomSQLChatMessageHistory(
    session_id="session_1",
    user_id="user_123",  # 添加 user_id
    connection="sqlite:///chat_history.db"  # 使用 connection 参数
)

# 添加消息
chat_history.add_user_message("Hello, how are you?")
chat_history.add_ai_message("I'm fine, thank you!")