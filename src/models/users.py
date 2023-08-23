
from uuid import uuid1
from pydantic import UUID1
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType
from secrets import token_urlsafe

from db import Base
from .mixins import Timestamp

class User(Timestamp, Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uid: Mapped[UUID1] = mapped_column(
        index=True,
        unique=True,
        default=uuid1
    )
    token: Mapped[str] = mapped_column(default=token_urlsafe)
    email: Mapped[str] = mapped_column(
        type_=EmailType,
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
