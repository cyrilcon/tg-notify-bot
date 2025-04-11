from typing import List

from sqlalchemy import Text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin
from .notification import Notification


class Document(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    buffer: Mapped[bytes] = mapped_column(LargeBinary, index=True)
    name: Mapped[str] = mapped_column(Text(), index=True)

    notifications: Mapped[List["Notification"]] = relationship(
        secondary="notification_document",
        back_populates="documents",
        lazy="joined",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"buffer={self.buffer!r}, "
            f"name={self.name!r})"
        )

    def __repr__(self):
        return str(self)
