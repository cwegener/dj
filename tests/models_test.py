"""
Tests for ``datajunction.models``.
"""

# pylint: disable=use-implicit-booleaness-not-comparison

from sqlmodel import Session

from datajunction.models import Column, Database, Node, Table


def test_node_relationship(session: Session) -> None:
    """
    Test the n:n self-referential relationships.
    """
    node_a = Node(name="A")
    node_b = Node(name="B")
    node_c = Node(name="C", parents=[node_a, node_b])

    session.add(node_c)

    assert node_a.children == [node_c]
    assert node_b.children == [node_c]
    assert node_c.children == []

    assert node_a.parents == []
    assert node_b.parents == []
    assert node_c.parents == [node_a, node_b]


def test_node_columns(session: Session) -> None:
    """
    Test that the node schema is derived from its tables.
    """
    database = Database(name="test", URI="sqlite://")

    table_a = Table(
        database_id=database.id,
        table="A",
        columns=[
            Column(name="ds", type="str"),
            Column(name="user_id", type="int"),
        ],
    )

    table_b = Table(
        database_id=database.id,
        table="B",
        columns=[Column(name="ds", type="datetime")],
    )

    node = Node(name="C", tables=[table_a, table_b])

    session.add(node)

    assert node.columns == [
        Column(name="ds", type="datetime"),
        Column(name="user_id", type="int"),
    ]
