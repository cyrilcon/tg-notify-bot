from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Text, BIGINT, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin

if TYPE_CHECKING:
    from .document import Document


class Notification(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, index=True)
    message: Mapped[str] = mapped_column(Text())
    button_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        index=True,
    )

    documents: Mapped[List["Document"]] = relationship(
        secondary="notification_document",
        back_populates="notifications",
        lazy="selectin",
        cascade="save-update",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"chat_id={self.chat_id}, "
            f"message={self.message!r}, "
            f"button_url={self.button_url!r}, "
            f"created_at={self.created_at!r})"
        )

    def __repr__(self):
        return str(self)
