"""
Model for nodes.
"""

from datetime import datetime, timezone
from functools import partial
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.sql.schema import Column as SqlaColumn
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from datajunction.models.column import Column
    from datajunction.models.representation import Representation


class Node(SQLModel, table=True):  # type: ignore
    """
    A node.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=SqlaColumn("name", String, unique=True))
    description: str = ""

    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))

    expression: Optional[str] = None

    # schema
    columns: List["Column"] = Relationship(
        back_populates="node",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )

    # storages
    representations: List["Representation"] = Relationship(
        back_populates="node",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
