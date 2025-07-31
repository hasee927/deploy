from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class FundWaterSchemasIn(BaseModel):
    merchant_id: str | None = None #"商户ID"
    water_type: int | None = None #"流水类型; 0:划扣, 1:上分, 2:可用转代付 ,3:代付转可用, 4:支付成功, 5:订单冲正, 6:转账成功, 7:转账失败, 8:转账申请"
    bill_no: str | None = None # 所属单号
    change_amount: str | None = None #变动余额
    pending_amount: str | None = None #在途金额变动
    pay_amount: str | None = None #代付金额变动
    change_total_amount: str | None = None #变动后总金额
    change_pending_amount: str | None = None #变动后在途金额
    change_pay_amount: str | None = None #变动后代付金额
    change_fund: str | None = None #变动后可转换金额
    optime: str | None = None #操作时间
    remark: str | None = None #备注

class FundWaterSchemasOut(FundWaterSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

