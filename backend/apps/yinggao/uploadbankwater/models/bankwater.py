from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String

class BankWater(BaseModel):
    __tablename__ = "yg_bankwater_button"
    __table_args__ = ({'comment': '上传银行流水按钮列表'})


    name: Mapped[str | None] = mapped_column(String(16), comment="银行名称")
    desc: Mapped[str | None] = mapped_column(String(64), comment="描述")
    image: Mapped[str | None] = mapped_column(String(128), comment="图标地址")


    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
