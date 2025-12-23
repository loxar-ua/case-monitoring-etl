from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from datetime import datetime

from .base import Base
from .media import Media
from .cluster import Cluster

class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    featured_image_url: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(String)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    dense_embedding: Mapped[list] = mapped_column(Vector(1), default=None, nullable=True) #TODO: change dimension size and list type
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    sparse_embedding: Mapped[list] = mapped_column(Vector(1), default=None, nullable=True)

    cluster_id: Mapped[int] = mapped_column(ForeignKey("cluster.id"), nullable=True)
    cluster: Mapped["Cluster"] = relationship(back_populates="articles")

    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), nullable=True)
    media: Mapped["Media"] = relationship(back_populates="articles")

    def __repr__(self):
        return "<Article %r, %r>" % (self.title, self.link)

