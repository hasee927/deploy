from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Integer



class FundWater(BaseModel):
    __tablename__ = "yg_fundwater"
    __table_args__ = ({'comment': '资金流水'})

    merchant_id: Mapped[str | None] = mapped_column(String(16), index=True, comment="商户ID")
    water_type: Mapped[int | None] = mapped_column(Integer, comment="流水类型; 0:划扣, 1:上分, 2:可用转代付 ,3:代付转可用, 4:支付成功, 5:订单冲正, 6:代付pending, 7:代付成功, 8:代付失败", default=0)
    bill_no: Mapped[str | None] = mapped_column(String(24), comment="所属单号")
    change_amount: Mapped[str | None] = mapped_column(String(16), comment="变动余额", default=0)
    pending_amount: Mapped[str | None] = mapped_column(String(24), comment="在途金额变动", default=0)
    pay_amount: Mapped[str | None] = mapped_column(String(24), comment="代付金额变动", default=0)
    change_total_amount: Mapped[str | None] = mapped_column(String(24), comment="变动后总金额", default=0)
    change_pending_amount: Mapped[str | None] = mapped_column(String(24), comment="变动后在途金额", default=0)
    change_pay_amount: Mapped[str | None] = mapped_column(String(24), comment="变动后代付金额", default=0)
    change_fund: Mapped[str | None] = mapped_column(String(24), comment="变动后可转换金额", default=0)
    optime: Mapped[str | None] = mapped_column(String(24), comment="操作时间")
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注")


    def __repr__(self):
        return f"id: {self.id}, change_total_amount: {self.change_total_amount}"
