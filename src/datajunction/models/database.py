"""
Model for databases.
"""

from datetime import datetime, timezone
from functools import partial
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from datajunction.models.query import Query
    from datajunction.models.representation import Representation


class Database(SQLModel, table=True):  # type: ignore
    """
    A database.

    A simple example:

        name: druid
        description: An Apache Druid database
        URI: druid://localhost:8082/druid/v2/sql/
        read-only: true

    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    name: str
    description: str = ""
    URI: str
    read_only: bool = True
    async_: bool = Field(default=False, sa_column_kwargs={"name": "async"})

    representations: List["Representation"] = Relationship(
        back_populates="database",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )

    queries: List["Query"] = Relationship(
        back_populates="database",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
