from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector, SparseVector

from datetime import datetime

from .base import Base
from .media import Media
from .cluster import Cluster

SPARSE_EMBEDDING_SIZE = 250002 # TODO: after implementing vector creation in demployment, change it to be dynamic
DENSE_EMBEDDING_SIZE = 1024

class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    featured_image_url: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(String)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    dense_embedding: Mapped[list] = mapped_column(Vector(DENSE_EMBEDDING_SIZE), default=None, nullable=True)
    sparse_embedding: Mapped[dict] = mapped_column(SparseVector(SPARSE_EMBEDDING_SIZE), default=None, nullable=True)
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_relevant: Mapped[bool] = mapped_column(Boolean, default=False)

    cluster_id: Mapped[int] = mapped_column(ForeignKey("cluster.id"), nullable=True)
    cluster: Mapped["Cluster"] = relationship(back_populates="articles")

    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), nullable=True)
    media: Mapped["Media"] = relationship(back_populates="articles")

    def __repr__(self):
        return "<Article %r, %r>" % (self.title, self.link)

