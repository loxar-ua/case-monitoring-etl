from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

association_table = Table(
    'cluster_category',
    Base.metadata,
    Column('cluster_id', Integer, ForeignKey('cluster.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")

    clusters: Mapped[list['Cluster']] = relationship(
        secondary=association_table,
        back_populates="categories"
    )


