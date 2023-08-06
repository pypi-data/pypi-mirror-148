import os
from sqlalchemy import inspect
from pystark.utils import patch
from pystark.logger import logger
from sqlalchemy.engine.base import Connection
from sqlalchemy import create_engine, MetaData


@patch(Connection)
class Connection:
    async def get(self, table_name: str, pk_column: str, primary_key) -> dict | None:
        x = self.execute("SELECT * FROM %s WHERE %s='%s'" % (table_name, pk_column, primary_key))
        x = [getattr(i, "_asdict")() for i in x]
        if x:
            return x[0]
        else:
            return None

    async def set(self, table_name: str, pk_column: str, primary_key, data: dict):
        text = ""
        for i in data:
            if isinstance(data[i], str):
                text += f"""{i}='{data[i].replace("'", "''")}'"""
            else:
                text += f"{i}={data[i]}"
            text += ", "
        data = text[:-2]
        self.execute(f"""UPDATE {table_name} SET {data} WHERE {pk_column}={primary_key}""")

    async def add(self, table_name: str, pk_column: str, primary_key, data: dict = None):
        if not data:
            data = {}
        data[pk_column] = primary_key
        data = {i: str(data[i]).replace("'", "''") for i in data}
        self.execute(f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(data.values())})")

    async def delete(self, table_name: str, pk_column: str, primary_key):
        self.execute("DELETE FROM %s WHERE %s=%s" % (table_name, pk_column, primary_key))

    async def count(self, table_name: str) -> int:
        return len(await self.get_all_primary_keys(table_name))

    async def get_all_primary_keys(self, table_name: str) -> list:
        return [i[0] for i in self.execute('SELECT * FROM %s' % table_name)]

    async def get_all_data(self, table_name: str) -> list[dict]:
        return [getattr(x, "_asdict")() for x in self.execute('SELECT * FROM %s' % table_name)]

    async def change_column_type(self, table_name: str, column_name: str, column_type: str):
        self.execute('ALTER TABLE %s ALTER COLUMN %s TYPE %s' % (table_name, column_name, column_type))

    async def add_column(self, table_name: str, column_name: str, column_type: str):
        self.execute('ALTER TABLE %s ADD %s %s' % (table_name, column_name, column_type))

    async def drop_column(self, table_name: str, column_name: str):
        self.execute('ALTER TABLE %s DROP COLUMN %s' % (table_name, column_name))

    async def drop_table(self, table_name: str,):
        self.execute('DROP TABLE %s' % table_name)

    async def columns(self, table_name: str) -> list[tuple[str]]:
        return [x[0] for x in self.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '%s'" % table_name)]

    async def list_tables(self) -> list:
        return inspect(self).get_table_names()

    async def has_table(self, table_name: str) -> bool:
        inspect(self.engine)
        return inspect(self.engine).has_table(table_name)


class Database:
    conn: Connection

    def __init__(self, url: str = os.getenv("DATABASE_URL")):
        """Initiate an SQL database. If url is not passed, environment variable DATABASE_URL is used"""
        if not url:
            logger.critical("No database url found")
            raise SystemExit
        self.engine = create_engine(url, executemany_mode='values_plus_batch')
        self.metadata = MetaData()

    def create(self) -> Connection:
        """Create the database tables and connect to the database.

        Returns:
            Connection object with monkey-patched helper methods.
        """
        self.metadata.create_all(bind=self.engine, checkfirst=True)
        connection = self.engine.connect()
        self.conn = connection
        return connection
