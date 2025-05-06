from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, DateTime

from bot.database.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    language_code: Mapped[str] = mapped_column(String)
    sub_end_date: Mapped[datetime] = mapped_column(DateTime)
