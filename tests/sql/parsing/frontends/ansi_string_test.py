"""
tests for DJ ast representation as sql string
"""
import pytest

from dj.sql.parsing.ast import Column, From, Name, Namespace, Query, Select, Table
from dj.sql.parsing.frontends.string import sql
from tests.sql.utils import TPCDS_QUERY_SET, compare_query_strings, read_query


def test_case_when_null_sql_string(case_when_null):
    """
    test converting a case_when_null query to sql string
    """
    assert compare_query_strings(
        sql(case_when_null).strip(),
        read_query("case_when_null.sql"),
    )


def test_trivial_sql_string(trivial_query):
    """
    test converting a trivial query to sql string
    """
    assert compare_query_strings(
        sql(trivial_query).strip(),
        read_query("trivial_query.sql"),
    )


@pytest.mark.parametrize("query_name", TPCDS_QUERY_SET)
def test_sql_string_tpcds(request, query_name):
    """
    test turning sql queries into strings via the string frontend
    """
    query = read_query(f"{query_name}.sql")
    gen_sql = sql(request.getfixturevalue(query_name))
    assert compare_query_strings(gen_sql, query)


def test_column_table_eq_compound_ident():
    """tests to see if marking a column as belonging to a table
    returns the same thing as a column with a compound identifier
    """
    assert sql(
        Query(
            select=Select(
                distinct=False,
                from_=From(
                    table=Table(
                        Name(name="a", quote_style=""),
                    ),
                    joins=[],
                ),
                group_by=[],
                having=None,
                projection=[
                    Column(
                        Name(name="x", quote_style=""),
                    ).add_namespace(Namespace([Name("a")])),
                ],
                where=None,
                limit=None,
            ),
            ctes=[],
        ),
    ) == sql(
        Query(
            select=Select(
                distinct=False,
                from_=From(
                    table=Table(
                        Name(name="a", quote_style=""),
                    ),
                    joins=[],
                ),
                group_by=[],
                having=None,
                projection=[
                    Column(Name(name="x", quote_style="")).add_table(
                        Table(
                            Name(name="a", quote_style=""),
                        ),
                    ),
                ],
                where=None,
                limit=None,
            ),
            ctes=[],
        ),
    )


def test_column_already_has_table():
    """
    tests that adding a table to a column a second time does not change the table
    """
    col = Column(
        Name(name="x", quote_style=""),
    ).add_table(Table(Name(name="a", quote_style="")))
    col.add_table(Table(Name(name="b", quote_style="")))
    assert col.table.name == Name("a")
