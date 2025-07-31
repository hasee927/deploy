from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class Bank(BaseModel):
    __tablename__ = "bank"
    __table_args__ = ({'comment': '所有银行'})

    name: Mapped[str] = mapped_column(String(64), index=True, comment="银行名称")
    addr: Mapped[str] = mapped_column(String(128), comment="银行地址")
    phone: Mapped[str] = mapped_column(String(24), comment="银行电话")
    desc: Mapped[str | None] = mapped_column(String(255), comment="银行描述")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, addr: {self.addr}, phone: {self.phone}， desc: {self.desc}"
