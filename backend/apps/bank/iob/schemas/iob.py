from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class IobSchemasIn(BaseModel):
    name: str
    accountNo: str | None = None
    desc: str | None = None


class IobSchemasOut(IobSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr