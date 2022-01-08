"""
Model for queries.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy.sql.schema import Column as SqlaColumn
from sqlalchemy_utils import UUIDType
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from datajunction.models.database import Database


class QueryState(str, Enum):
    """
    Different states of a query.
    """

    UNKNOWN = "UNKNOWN"
    ACCEPTED = "ACCEPTED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"


class BaseQuery(SQLModel):
    """
    Base class for query models.
    """

    database_id: int = Field(foreign_key="database.id")
    catalog: Optional[str] = None
    schema_: Optional[str] = None  # XXX use alias  # pylint: disable=fixme


class Query(BaseQuery, table=True):  # type: ignore
    """
    A query.
    """

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=SqlaColumn(UUIDType(), primary_key=True),
    )
    database: "Database" = Relationship(back_populates="queries")

    submitted_query: str
    executed_query: Optional[str] = None

    scheduled: Optional[datetime] = None
    started: Optional[datetime] = None
    finished: Optional[datetime] = None

    state: QueryState = QueryState.UNKNOWN
    progress: float = 0.0
