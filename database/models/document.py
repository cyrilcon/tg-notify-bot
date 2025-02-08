from sqlalchemy import Text, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base, TableNameMixin
from .notification import Notification


class Document(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notification.id", ondelete="CASCADE"),
    )
    buffer: Mapped[bytes] = mapped_column(LargeBinary)
    name: Mapped[str] = mapped_column(Text(), index=True)

    notification: Mapped["Notification"] = relationship(
        back_populates="documents",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"notification_id={self.notification_id}, "
            f"buffer={self.buffer!r}, "
            f"name={self.name!r})"
        )

    def __repr__(self):
        return str(self)
