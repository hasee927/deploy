from sqlalchemy.orm import  Mapped, mapped_column


from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer




class ChannelDataList(BaseModel):
    __tablename__ = "yg_channel_list"
    __table_args__ = ({'comment': '通道列表'})

    pay_company: Mapped[str] = mapped_column(String(64), index=True, comment="支付公司")
    name: Mapped[str | None] = mapped_column(String(64), index=True, comment="公司名称")
    channel_code: Mapped[str] = mapped_column(String(24), comment="通道code")
    channel_name: Mapped[str] = mapped_column(String(24), comment="通道名称")
    channel_type: Mapped[int] = mapped_column(Integer, comment="通道类型; 1:代收通道, 2:代付通道")
    channel_status: Mapped[int] = mapped_column(Integer, comment="通道状态; 1:正常,2:异常")
    pay_gw_addr: Mapped[str | None] = mapped_column(String(128), comment="代付网关地址")
    pay_gw_check_status_addr: Mapped[str | None] = mapped_column(String(128), comment="代付网关状态检查地址")
    pay_gw_merchant_id: Mapped[str | None] = mapped_column(String(64), comment="代付网关商户名称(ID)")
    pay_gw_id: Mapped[str | None] = mapped_column(String(64), comment="代付网关Id(key)")
    pay_gw_token: Mapped[str | None] = mapped_column(String(64), comment="代付网关token(Secret)")
    pay_gw_callback_id: Mapped[str | None] = mapped_column(String(64), comment="代付网关回调地址id")
    pay_gw_spare: Mapped[str | None] = mapped_column(String(64), comment="代付网关备用字段")
    # disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注")


    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, channel_code: {self.channel_code}, \
                channel_name: {self.channel_name}"
