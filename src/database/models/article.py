from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector, SPARSEVEC

from datetime import datetime

from .base import Base

DENSE_DIM = 1024
VOCAB_SIZE = 250002


class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id", ondelete="RESTRICT"),
        nullable=False
    )
    link: Mapped[str] = mapped_column(String, primary_key=True)
    featured_image_url: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(String)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    cluster_id: Mapped[int] = mapped_column(
        ForeignKey("cluster.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_relevant: Mapped[bool] = mapped_column(Boolean, default=True)

    dense_embedding: Mapped[list] = mapped_column(Vector(DENSE_DIM), nullable=True)
    sparse_embedding: Mapped[list] = mapped_column(SPARSEVEC(VOCAB_SIZE), nullable=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=True)

    cluster: Mapped["Cluster"] = relationship(back_populates="articles")
    media: Mapped["Media"] = relationship(back_populates="articles")
    event: Mapped["Event"] = relationship(back_populates="articles")

    def __repr__(self):
        return "<Article %r, %r>" % (self.title, self.link)