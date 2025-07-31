from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer

class Bank_Iob(BaseModel):
    __tablename__ = "bank_iob"
    __table_args__ = ({'comment': 'IOB银行'})

    name: Mapped[str] = mapped_column(String(50), index=True, comment="用户名")
    accountNo: Mapped[str] = mapped_column(String(50), comment="账号")
    desc: Mapped[str | None] = mapped_column(String(255), comment="描述")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, accountNo: {self.accountNo}, desc: {self.desc}"
