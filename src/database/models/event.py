from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    cluster_id: Mapped[int] = mapped_column(
        ForeignKey("cluster.id", ondelete="CASCADE"),
        nullable=True
    )
    cluster: Mapped["Cluster"] = relationship(back_populates="events")

    articles: Mapped[list["Article"]] = relationship(back_populates="event")