"""
Tests for the catalog API.
"""

from fastapi.testclient import TestClient


def test_catalog_adding_a_new_catalog(
    client: TestClient,
) -> None:
    """
    Test adding a catalog
    """
    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data == {"name": "dev", "engines": []}


def test_catalog_list(
    client: TestClient,
) -> None:
    """
    Test listing catalogs
    """
    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "version": "3.3.1",
            "dialect": "spark",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
            "engines": [
                {
                    "name": "spark",
                    "version": "3.3.1",
                    "dialect": "spark",
                },
            ],
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "test",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "prod",
        },
    )
    assert response.status_code == 201

    response = client.get("/catalogs/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "dev",
            "engines": [
                {"name": "spark", "version": "3.3.1", "uri": None, "dialect": "spark"},
            ],
        },
        {"name": "test", "engines": []},
        {"name": "prod", "engines": []},
    ]


def test_catalog_get_catalog(
    client: TestClient,
) -> None:
    """
    Test getting a catalog
    """
    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "version": "3.3.1",
            "dialect": "spark",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
            "engines": [
                {
                    "name": "spark",
                    "version": "3.3.1",
                    "dialect": "spark",
                },
            ],
        },
    )
    assert response.status_code == 201

    response = client.get(
        "/catalogs/dev",
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "name": "dev",
        "engines": [
            {"name": "spark", "uri": None, "version": "3.3.1", "dialect": "spark"},
        ],
    }


def test_catalog_adding_a_new_catalog_with_engines(
    client: TestClient,
) -> None:
    """
    Test adding a catalog with engines
    """
    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "uri": None,
            "version": "3.3.1",
            "dialect": "spark",
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
            "engines": [
                {
                    "name": "spark",
                    "version": "3.3.1",
                    "dialect": "spark",
                },
            ],
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data == {
        "name": "dev",
        "engines": [
            {
                "name": "spark",
                "uri": None,
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    }


def test_catalog_adding_a_new_catalog_then_attaching_engines(
    client: TestClient,
) -> None:
    """
    Test adding a catalog then attaching a catalog
    """
    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "uri": None,
            "version": "3.3.1",
            "dialect": "spark",
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
        },
    )
    assert response.status_code == 201

    client.post(
        "/catalogs/dev/engines/",
        json=[
            {
                "name": "spark",
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    )

    response = client.get("/catalogs/dev/")
    data = response.json()
    assert data == {
        "name": "dev",
        "engines": [
            {
                "name": "spark",
                "uri": None,
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    }


def test_catalog_adding_without_duplicating(
    client: TestClient,
) -> None:
    """
    Test adding a catalog and having existing catalogs not re-added
    """
    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "uri": None,
            "version": "2.4.4",
            "dialect": "spark",
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "version": "3.3.0",
            "dialect": "spark",
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = client.post(
        "/engines/",
        json={
            "name": "spark",
            "version": "3.3.1",
            "dialect": "spark",
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
            "dialect": "spark",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/dev/engines/",
        json=[
            {
                "name": "spark",
                "version": "2.4.4",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "version": "3.3.0",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/dev/engines/",
        json=[
            {
                "name": "spark",
                "version": "2.4.4",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "version": "3.3.0",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    )
    assert response.status_code == 201
    data = response.json()
    assert data == {
        "name": "dev",
        "engines": [
            {
                "name": "spark",
                "uri": None,
                "version": "2.4.4",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "uri": None,
                "version": "3.3.0",
                "dialect": "spark",
            },
            {
                "name": "spark",
                "uri": None,
                "version": "3.3.1",
                "dialect": "spark",
            },
        ],
    }


def test_catalog_raise_on_adding_a_new_catalog_with_nonexistent_engines(
    client: TestClient,
) -> None:
    """
    Test raising an error when adding a catalog with engines that do not exist
    """
    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
            "engines": [
                {
                    "name": "spark",
                    "version": "4.0.0",
                    "dialect": "spark",
                },
            ],
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data == {"detail": "Engine not found: `spark` version `4.0.0`"}


def test_catalog_raise_on_catalog_already_exists(
    client: TestClient,
) -> None:
    """
    Test raise on catalog already exists
    """
    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/catalogs/",
        json={
            "name": "dev",
        },
    )
    data = response.json()
    assert response.status_code == 409
    assert data == {"detail": "Catalog already exists: `dev`"}
