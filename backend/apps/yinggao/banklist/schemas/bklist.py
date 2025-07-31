from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class BKListSchemasIn(BaseModel):
    bank_name: str | None = None
    channel_code: str | None = None
    bank_account: str | None = None
    bank_utr: str | None = None
    random_number: str | None = None
    amount: str | None = None
    account_balance: str | None = None
    # order_id: str | None = None
    trading_time: str | None = None
    trading_info: str | None = None
    info_sources: str | None = None
    match_type: str | None = None
    collection_type: str | None = None
    file_name: str | None = None


class BKListSchemasOut(BKListSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr