from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, String, DateTime

from bot.database.models import BaseModel


class User(BaseModel):
    """
    Represents a user in the database.
    Attributes:
        id (int): The unique identifier for the user. Primary key.
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        language_code (str): The language code representing the user's preferred language.
        sub_end_date (datetime): The subscription end date for the user.
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    language_code: Mapped[str] = mapped_column(String, nullable=False)
    sub_end_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
