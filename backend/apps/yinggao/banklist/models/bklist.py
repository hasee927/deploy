from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer, UniqueConstraint


class Banklist(BaseModel):
    __tablename__ = "yg_bank_list"
    __table_args__ = (
        {'comment': '银行列表'}
        # UniqueConstraint('bank_utr', name='银行列表'),
    )


    bank_name: Mapped[str | None] = mapped_column(String(16), index=True, comment="银行名称")
    channel_code: Mapped[str | None] = mapped_column(String(24), comment="通道code")
    bank_account: Mapped[str | None] = mapped_column(String(16), comment="银行账号")
    bank_utr: Mapped[str | None] = mapped_column(String(16), comment="银行UTR", unique=True)
    random_number: Mapped[str | None] = mapped_column(String(16), comment="随机数")
    amount: Mapped[str | None] = mapped_column(String(16), comment="金额")
    account_balance: Mapped[str | None] = mapped_column(String(16), comment="账号余额")
    # order_id: Mapped[str | None] = mapped_column(String(16), comment="订单ID")
    trading_time: Mapped[str | None] = mapped_column(String(24), comment="交易时间")
    trading_info: Mapped[str | None] = mapped_column(String(256), comment="交易信息")
    info_sources: Mapped[str | None] = mapped_column(String(24), comment="信息来源: sms:短信上传, crawler:爬虫, backend: 后台上传")
    match_type: Mapped[str | None] = mapped_column(String(24),
                            comment="匹配类型: auto:自动撞库, manual:手动补单,unmatch:未匹配,robot:机器人补单,active: 主动填写")
    collection_type: Mapped[str | None] = mapped_column(String(24), comment="收款类型: entry:入账，extract:提取")
    file_name: Mapped[str | None] = mapped_column(String(128), comment="上传文件名称")


    def __repr__(self):
        return f"id: {self.id}, bank_name: {self.bank_name}, channel_code: {self.channel_code}, \
                bank_account: {self.bank_account}， bank_utr: {self.bank_utr}"
