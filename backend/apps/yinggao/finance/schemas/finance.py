from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class FinanaceSchemasIn(BaseModel):
    merchant_id: str | None = None #"商户ID"
    total_amount: str | None = None #"总金额"
    change_fund: str | None = None #"转换资金"
    pay_amount: str | None = None #"可用代付金额"
    pending_amount: str | None = None #"在途金额pending"
    change_type: int | None = None #"更改金额类型; 0:划扣, 1:上分, 2:可用转代付 ,3:代付转可用")
    change_amount: str | None = None #"变动金额"
    remark: str | None = None # 备注

class FinanaceSchemasOut(FinanaceSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr