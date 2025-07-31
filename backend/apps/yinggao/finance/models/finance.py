from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Integer



class Finance(BaseModel):
    __tablename__ = "yg_finance"
    __table_args__ = ({'comment': '商户资金'})

    merchant_id: Mapped[str | None] = mapped_column(String(16), index=True, comment="后台账号/商户ID", unique=True)
    total_amount: Mapped[str | None] = mapped_column(String(24), comment="总金额", default=0)
    change_fund: Mapped[str | None] = mapped_column(String(24), comment="可转换资金", default=0)
    pay_amount: Mapped[str | None] = mapped_column(String(24), comment="可用代付金额", default=0)
    pending_amount: Mapped[str | None] = mapped_column(String(24), comment="在途金额pending", default=0)
    change_type: Mapped[int | None] = mapped_column(Integer, comment="更改金额类型; 0:划扣, 1:上分, 2:可用转代付 ,3:代付转可用", default=0)
    change_amount: Mapped[str | None] = mapped_column(String(16),comment="变动金额", default=0)
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注")


    def __repr__(self):
        return f"id: {self.id}, total_amount: {self.total_amount}"
