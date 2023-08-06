import duckdb
from typing import Any, Generic, Iterator, Optional, TypeVar, cast


Schema = TypeVar("Schema")


class Engine:
    def __init__(self) -> None:
        self._con = duckdb.connect(database=":memory:")
        self._counter = 0

    def get_and_increment_counter(self) -> int:
        result = self._counter
        self._counter += 1
        return result

    def empty(self, table_name: str, column_def: str) -> "DataFrame[Schema]":
        pass

    def read_csv(self, table_name: str, column_def: str, csv: str) -> "DataFrame[Schema]":
        self._con.execute(f"CREATE TABLE {table_name} ({column_def})")
        self._con.execute(f"COPY {table_name} FROM '{csv}' (AUTO_DETECT TRUE);")

        return DataFrame(self, table_name)

    def query(self, sql: str, **kwargs: "DataFrame[Any]") -> "DataFrame[Schema]":
        output: DataFrame[Schema] = DataFrame(self)

        full_query = f"""
        CREATE VIEW {output._table_or_view_name} AS {sql}
        """
        self._con.execute(full_query)
        return output


class DataFrame(Generic[Schema]):
    def __init__(self, engine: Engine, table_name: Optional[str] = None) -> None:
        if table_name is not None:
            self._table_or_view_name = table_name
        else:
            self._table_or_view_name = f"view_{engine.get_and_increment_counter()}"
        self._engine = engine

    @property
    def schema(self) -> Schema:
        self._engine._con.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{self._table_or_view_name}' ORDER BY ordinal_position"
        )

        return cast(Schema, tuple(self._engine._con.fetchall()))

    def fetchall(self) -> Iterator[Any]:
        yield from self._engine._con.execute(f"SELECT * FROM {self._table_or_view_name}").fetchall()

    def __str__(self) -> str:
        return self._table_or_view_name

    def materialize(self) -> "DataFrame[Schema]":
        table_name = f"table_{self._engine.get_and_increment_counter()}"
        self._engine._con.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM {self._table_or_view_name}"
        )
        return DataFrame(self._engine, table_name)

    def index(self, columns: str) -> "DataFrame[Schema]":
        index_name = f"ix_{self._engine.get_and_increment_counter()}"
        self._engine._con.execute(
            f"CREATE INDEX {index_name} ON {self._table_or_view_name} ({columns})"
        )
        return self
