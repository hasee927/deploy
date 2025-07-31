from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class BotGroup(BaseModel):
    __tablename__ = "yg_botgroup_list"
    __table_args__ = ({'comment': '机器人群列表'})

    name: Mapped[str | None] = mapped_column(String(24), comment="群名称")
    chat_id: Mapped[str | None] = mapped_column(String(24), comment="群聊ID")
    type: Mapped[int | None] = mapped_column(Integer, comment="群分类; 1:商户,2:渠道")
    disabled: Mapped[bool | None] = mapped_column(Boolean, default=False, comment="是否禁用")
    remark: Mapped[str | None] = mapped_column(String(256), comment="备注")

    def __repr__(self):
        return f"id: {self.id}, chat_id: {self.chat_id}, name: {self.name}"
