"""
Model for columns.
"""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from datajunction.models.node import Node


class Column(SQLModel, table=True):  # type: ignore
    """
    A column.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str

    node_id: int = Field(foreign_key="node.id")
    node: Node = Relationship(back_populates="columns")
