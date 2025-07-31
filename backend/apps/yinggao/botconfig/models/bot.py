from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class BotConfig(BaseModel):
    __tablename__ = "yg_bot_list"
    __table_args__ = ({'comment': '机器人列表'})


    chat_id: Mapped[str | None] = mapped_column(String(24), comment="群聊ID")
    name: Mapped[str | None] = mapped_column(String(24), comment="群名称")
    token: Mapped[str | None] = mapped_column(String(64), comment="机器人token")
    user_to: Mapped[str | None] = mapped_column(String(128), comment="机器人用途")
    command: Mapped[str | None] = mapped_column(String(256), comment="使用命令")
    bot_sign: Mapped[str | None] = mapped_column(String(24), comment="机器人标识")
    remark: Mapped[str | None] = mapped_column(String(256), comment="备注")
    sign: Mapped[str | None] = mapped_column(String(24), comment="接口签名")


    def __repr__(self):
        return f"id: {self.id}, chat_id: {self.chat_id}"
