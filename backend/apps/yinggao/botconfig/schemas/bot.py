from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class BotSchemasIn(BaseModel):
    chat_id: str | None = None  #群聊ID
    name: str | None = None #群名称
    token: str | None = None #机器人token
    user_to: str | None = None #机器人用途
    command: str | None = None #使用命令
    bot_sign: str | None = None #机器人标识
    remark: str | None = None #备注
    sign: str | None = None #接口签名


class BotSchemasOut(BotSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
