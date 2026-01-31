from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Cluster(Base):
    __tablename__ = "cluster"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")
    summary: Mapped[str] = mapped_column(String, default="")
    is_relevant: Mapped[bool] = mapped_column(Boolean, default=False)
    featured_image_url: Mapped[str] = mapped_column(String)

    articles: Mapped[list["Article"]] = relationship(back_populates="cluster")

    def __repr__(self):
        return "<Cluster %r>" % self.name