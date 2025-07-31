from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class SmsList(BaseModel):
    __tablename__ = "yg_sms_list"
    __table_args__ = ({'comment': '短信列表'})


    channel_code: Mapped[str | None] = mapped_column(String(24), comment="通道code")
    sender_addr: Mapped[str | None] = mapped_column(String(32), comment="发送地址")
    sms_id: Mapped[str | None] = mapped_column(String(24), comment="短信ID")
    sms_time: Mapped[str | None] = mapped_column(String(24), comment="短信时间")
    sms_utc_time: Mapped[str | None] = mapped_column(String(24), comment="短信utc时间")
    sms_type: Mapped[str | None] = mapped_column(String(16), comment="短信类型: 1:其他短信, 2:otp短信", default='1')
    code: Mapped[str | None] = mapped_column(String(10), comment="OTP验证码")
    context: Mapped[str | None] = mapped_column(String(512), comment="短信内容")

    def __repr__(self):
        return f"id: {self.id}, context: {self.context}"
