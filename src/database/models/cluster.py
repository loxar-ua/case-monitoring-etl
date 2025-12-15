from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .category import association_table


class Cluster(Base):
    __tablename__ = "cluster"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")
    is_relevant: Mapped[bool] = mapped_column(Boolean, default=False)
    summary: Mapped[str] = mapped_column(String, default="")

    categories: Mapped[list['Category']] = relationship(
        secondary=association_table,
        back_populates="clusters"
    )

    articles: Mapped[list['Article']] = relationship(back_populates="cluster")

    def __repr__(self):
        return "<Cluster %r>" % self.name