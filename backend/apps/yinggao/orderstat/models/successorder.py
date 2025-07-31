from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class Order_Success(BaseModel):
    __tablename__ = "yg_order_success"
    __table_args__ = ({'comment': '成功订单'})

    bank_name: Mapped[str | None] = mapped_column(String(16), index=True, comment="银行名称")
    channel_code: Mapped[str | None] = mapped_column(String(24), index=True, comment="通道code")
    success_order: Mapped[int | None] = mapped_column(String(11), comment="成功订单数", default=0)
    fail_order: Mapped[int | None] = mapped_column(String(11), comment="失败订单数", default=0)
    total_order: Mapped[int | None] = mapped_column(String(11), comment="总订单数", default=0)
    success_rate: Mapped[str | None] = mapped_column(String(11), comment="成功率", default=0)
    success_amount: Mapped[str | None] = mapped_column(String(24), index=True, comment="成功订单金额")
    total_amount: Mapped[str | None] = mapped_column(String(24), index=True, comment="订单总金额")


    def __repr__(self):
        return f"id: {self.id}, success_order: {self.success_order}"
