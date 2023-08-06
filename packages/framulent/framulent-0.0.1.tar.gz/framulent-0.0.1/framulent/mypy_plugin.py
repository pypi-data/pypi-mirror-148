import duckdb

import typing
import mypy.nodes as n
import mypy.types as mt
from mypy.plugin import MethodContext, Options, Plugin, Type


class CustomPlugin(Plugin):
    """
    TODO: This is extremely messy, and there are some rough edges. But it works.
    """
    def __init__(self, options: Options) -> None:
        self._con = duckdb.connect(database=':memory:')
        super().__init__(options)

    def get_method_hook(self, fullname: str) -> typing.Optional[typing.Callable[[MethodContext], Type]]:
        # NEW CODE
        if fullname in ("framulent.engine.Engine.read_csv", "framulent.engine.Engine.empty"):
            return self._analyze_method_context_create_table
        if fullname == "framulent.engine.Engine.query":
            return self._analyze_method_context_query
        if fullname == "framulent.engine.DataFrame.__iter__":
            return self._analyze_method_context_iter
        return None

    def _analyze_method_context_iter(self, method_ctx: MethodContext) -> Type:
        # TODO: Finish this. We can insert a single row containing dummy values
        # that conform to the schema. Then we can select that single row and
        # return the Python types of the items that we get back.
        return method_ctx.default_return_type

    def _analyze_method_context_query(self, method_ctx: MethodContext) -> Type:
        try:
            # There should be (at least) two kinds of things in the list here:
            # - mypy.nodes.StrExpr instances. These are the SQL string fragments.
            # - (at position n): mypy.nodes.CallExpr nodes, where guts[n].args[0].node.type
            #   is a BippyTable. We can hoover the schema of the table out of here. These are of type mypy.types.Instance.
            sql_interpolation_expr = method_ctx.args[0][0].args[0].items
            sql_string = ""
            table_names = []
            for idx, item in enumerate(sql_interpolation_expr):
                if isinstance(item, n.StrExpr):
                    sql_string += item.value
                elif (
                    isinstance(item, n.CallExpr) and
                    isinstance(item.args[0], n.NameExpr) and
                    isinstance(item.args[0].node, n.Var) and
                    isinstance(item.args[0].node.type, mt.Instance)
                ):
                    table_schema_type = item.args[0].node.type.args[0]

                    # TODO: Use a better value for table_name
                    # table_name = f"table_{idx}"
                    table_name = item.args[0].name
                    table_names.append(table_name)
                    table_schema_dict = {}
                    for column_name, column_type in map(lambda t: t.items, table_schema_type.items):
                        table_schema_dict[column_name.value] = column_type.value
                    columns_def = ",".join(
                        f"\"{column_name}\" {column_type}"
                        for column_name, column_type in table_schema_dict.items()
                    )
                    self._con.execute(
                        f"CREATE TEMPORARY TABLE IF NOT EXISTS {table_name} ({columns_def})"
                    )
                    sql_string += table_name

            # Now make a CREATE VIEW AS query
            view_name = f"view_{id(method_ctx)}"

            view_sql = f"CREATE TEMPORARY VIEW {view_name} AS {sql_string}"

            self._con.execute(view_sql)
            self._con.execute(
                f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{view_name}' ORDER BY ordinal_position"
            )

            schema = list(self._con.fetchall())

            for t in table_names:
                self._con.execute(f"DROP TABLE IF EXISTS {t}")
            self._con.execute(f"DROP VIEW {view_name}")

            str_type = method_ctx.api.named_type("builtins.str")

            schema_tuple = mt.TupleType(
                [
                    mt.TupleType(
                        [
                            mt.LiteralType(column_name, fallback=str_type),
                            mt.LiteralType(column_type, fallback=str_type),
                        ],
                        fallback=method_ctx.api.named_type("builtins.tuple")
                    )
                    for column_name, column_type in schema
                ],
                fallback=method_ctx.api.named_type("builtins.tuple")
            )

            method_ctx.default_return_type.args = (
                schema_tuple,
            )

        except Exception as e:
            method_ctx.api.fail(str(e), method_ctx.context)
        finally:
            return method_ctx.default_return_type

    def _analyze_method_context_create_table(self, method_ctx: MethodContext) -> Type:
        try:
            method_ctx.default_return_type

            create_table_sql = (
                f"CREATE TEMPORARY TABLE tmp ({method_ctx.args[1][0].value});"
            )
            self._con.execute(create_table_sql)

            self._con.execute(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='tmp' ORDER BY ordinal_position"
            )

            schema = list(self._con.fetchall())

            self._con.execute("DROP TABLE tmp")

            str_type = method_ctx.api.named_type("builtins.str")

            schema_tuple = mt.TupleType(
                [
                    mt.TupleType(
                        [
                            mt.LiteralType(column_name, fallback=str_type),
                            mt.LiteralType(column_type, fallback=str_type),
                        ],
                        fallback=method_ctx.api.named_type("builtins.tuple")
                    )
                    for column_name, column_type in schema
                ],
                fallback=method_ctx.api.named_type("builtins.tuple")
            )

            method_ctx.default_return_type.args = (
                schema_tuple,
            )
        except Exception as e:
            method_ctx.api.fail(str(e), method_ctx.context)
        finally:
            return method_ctx.default_return_type


def plugin(version: str) -> typing.Type[CustomPlugin]:
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
