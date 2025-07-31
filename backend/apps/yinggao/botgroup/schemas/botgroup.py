from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class BotGroupSchemasIn(BaseModel):
    name: str | None = None  # 群名称
    chat_id: str | None = None  # 群聊ID
    type: int  #群分类; 1:商户,2:渠道"
    disabled: bool | None = False  # comment="是否禁用"
    remark: str | None = None #"备注"

class BotGroupSchemasOut(BotGroupSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
