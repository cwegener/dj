"""
Model for representations (tables).
"""

from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from datajunction.models.database import Database
    from datajunction.models.node import Node


class Representation(SQLModel, table=True):  # type: ignore
    """
    A representation of data.

    Nodes can have multiple representations of data, in different databases.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    node_id: int = Field(foreign_key="node.id")
    node: "Node" = Relationship(back_populates="representations")

    database_id: int = Field(foreign_key="database.id")
    database: "Database" = Relationship(back_populates="representations")
    catalog: Optional[str] = None
    schema_: Optional[str] = Field(None, alias="schema")
    table: str

    cost: float = 1.0
