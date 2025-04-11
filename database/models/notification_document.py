from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base, TableNameMixin


class NotificationDocument(Base, TableNameMixin):
    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notification.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    document_id: Mapped[int] = mapped_column(
        ForeignKey("document.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(notification_id={self.notification_id}, "
            f"document_id={self.document_id})"
        )

    def __repr__(self):
        return str(self)
