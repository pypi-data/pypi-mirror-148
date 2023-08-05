import os
import re
from functools import lru_cache
from urllib.parse import urlparse

from pony import orm

db = orm.Database()


@lru_cache()
def compile_pattern(pattern: str, case_sensitive: bool):
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(pattern, flags=flags)


@lru_cache()
def get_rule(rule_id: int):
    return Rule.select(lambda r: r.id == rule_id).first()


class Rule(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    label = orm.Required(str)
    meta = orm.Optional(orm.Json, nullable=True)

    # regex (expression or composite)
    pattern = orm.Optional(str, nullable=True)

    # literals
    name = orm.Optional(str, nullable=True)
    synonyms = orm.Optional(orm.StrArray, nullable=True)

    # flags
    is_composite = orm.Optional(bool, sql_default=False)
    case_sensitive = orm.Optional(bool, sql_default=False)
    ignore_punctuation = orm.Optional(bool, sql_default=False)
    has_groups = orm.Optional(bool, sql_default=False)
    skip_boundaries = orm.Optional(bool, sql_default=False)

    @property
    def is_pattern(self):
        return not self.is_literal and not self.is_composite

    @property
    def is_literal(self):
        return self.name is not None

    def get_groups(self, text: str):
        if self.has_groups:
            pattern = compile_pattern(self.pattern, self.case_sensitive)
            match = pattern.match(text)
            return match.groupdict()


class Connection:
    def __init__(self, db_url: str = None, create_tables: bool = False):
        db_url = db_url or os.environ.get("ENTITYSCAN_DB_URL")
        db_bind_params = parse_url(db_url)

        table = db_bind_params.pop("_table_", False)
        if table:
            Rule._table_ = table

        db.bind(**db_bind_params)
        db.generate_mapping(create_tables=create_tables)
        self.rule_cache = lru_cache(maxsize=1000)

    @classmethod
    def close(cls):
        db.disconnect()
        db.provider = None

    @orm.db_session
    def get_count(self):
        return Rule.select().count()

    @orm.db_session
    def clear(self):
        get_rule.cache_clear()  # https://stackoverflow.com/a/55497384
        return Rule.select().delete()


def parse_url(db_url: str):
    # generate arguments for database binding:
    # https://docs.ponyorm.org/firststeps.html#database-binding

    url = urlparse(db_url)
    scheme = "postgres" if url.scheme == "postgresql" else url.scheme
    assert scheme in {"sqlite", "postgres"}, f"Unsupported: {url.scheme}"

    kw = {"provider": scheme}
    path_parts = url.path.split("/")

    if scheme == "sqlite":
        if path_parts[1].startswith(":"):
            kw["filename"] = path_parts[1]
        else:
            kw["filename"] = "/".join(path_parts)

    # postgres://user:pass@host:port/database/schema.table
    if scheme == "postgres":
        kw["user"] = url.username or ""
        kw["password"] = url.password or ""
        kw["host"] = url.hostname or ""

        path_parts += ["", "", ""]
        kw["database"] = path_parts[1]

        schema = path_parts[2] or ""
        table = path_parts[3] or ""
        if schema and table:
            kw["_table_"] = (schema, table)

        assert kw["database"], f"No database name provided in URL {db_url}"

    return kw
