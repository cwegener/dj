"""
Fixtures for testing DJ client.
"""
# pylint: disable=redefined-outer-name, invalid-name, W0611

from http.client import HTTPException
from typing import Iterator
from unittest.mock import MagicMock

import pytest
from cachelib import SimpleCache
from dj.api.main import app
from dj.config import Settings
from dj.models.query import QueryCreate, QueryWithResults
from dj.service_clients import QueryServiceClient
from dj.typing import QueryState
from dj.utils import get_query_service_client, get_session, get_settings
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel
from starlette.testclient import TestClient

from tests.examples import EXAMPLES, QUERY_DATA_MAPPINGS


@pytest.fixture
def settings(mocker: MockerFixture) -> Iterator[Settings]:
    """
    Custom settings for unit tests.
    """
    settings = Settings(
        index="sqlite://",
        repository="/path/to/repository",
        results_backend=SimpleCache(default_timeout=0),
        celery_broker=None,
        redis_cache=None,
        query_service=None,
    )

    mocker.patch(
        "dj.utils.get_settings",
        return_value=settings,
    )

    yield settings


@pytest.fixture
def session() -> Iterator[Session]:
    """
    Create an in-memory SQLite session to test models.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine, autoflush=False) as session:
        yield session


@pytest.fixture
def query_service_client(mocker: MockerFixture) -> Iterator[QueryServiceClient]:
    """
    Custom settings for unit tests.
    """
    qs_client = QueryServiceClient(uri="query_service:8001")
    qs_client.query_state = QueryState.RUNNING  # type: ignore

    def mock_submit_query(
        query_create: QueryCreate,
    ) -> QueryWithResults:
        results = QUERY_DATA_MAPPINGS[
            query_create.submitted_query.strip()
            .replace('"', "")
            .replace("\n", "")
            .replace(" ", "")
        ]
        if isinstance(results, Exception):
            raise results

        if results.state not in (QueryState.FAILED,):
            results.state = qs_client.query_state  # type: ignore
            qs_client.query_state = QueryState.FINISHED  # type: ignore
        return results

    mocker.patch.object(
        qs_client,
        "submit_query",
        mock_submit_query,
    )

    mocker.patch.object(
        qs_client,
        "materialize",
        MagicMock(),
    )
    yield qs_client


@pytest.fixture
def server(  # pylint: disable=too-many-statements
    session: Session,
    settings: Settings,
    query_service_client: QueryServiceClient,
) -> TestClient:
    """
    Create a mock server for testing APIs that contains a mock query service.
    """

    def get_query_service_client_override() -> QueryServiceClient:
        return query_service_client

    def get_session_override() -> Session:
        return session

    def get_settings_override() -> Settings:
        return settings

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[
        get_query_service_client
    ] = get_query_service_client_override

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def post_and_raise_if_error(server: TestClient, endpoint: str, json: dict):
    """
    Post the payload to the client and raise if there's an error
    """
    response = server.post(endpoint, json=json)
    if not response.ok:
        raise HTTPException(response.text)


@pytest.fixture
def session_with_examples(server: TestClient) -> TestClient:
    """
    load examples
    """
    for endpoint, json in EXAMPLES:
        post_and_raise_if_error(server=server, endpoint=endpoint, json=json)  # type: ignore
    return server
