import warnings
from dataclasses import dataclass
from typing import Set, Optional
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.engine.url import make_url
from sqlalchemy import exc as sa_exc
from concurrent.futures import ThreadPoolExecutor
import os

@dataclass(unsafe_hash=True, eq=True)
class Interface:
    name: str
    schema_name: str
    table_name: Optional[str]
    unique_index: str
    description: str
    table: Optional[Table] = None
    full: bool = False


@dataclass(unsafe_hash=True, eq=True)
class Source:
    name: str
    description: str
    connection_url: str
    schema_name: Optional[str]
    interfaces: Optional[Set[Interface]] = None


@dataclass
class DBMSMeta:

    @staticmethod
    def read(source_name: str, table_name: str, 
             schema_name: str, 
             index_col: str, 
             connection_url: str):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            url = make_url(connection_url)
            url.username=os.environ['{}_USER'.format(source_name).upper()]
            url.password=os.environ['{}_PASS'.format(source_name).upper()]
            engine = create_engine(url)
            metadata = MetaData()
            table = Table(table_name, metadata, schema=schema_name, autoload=True, autoload_with=engine)
            for col in table.columns:
                if type(col.type).__name__ == 'TIMESTAMP' and connection_url.startswith('mssql'):
                    col.doc = 'NVARCHAR'
                else:
                    col.doc = type(col.type).__name__
            if index_col:
                ixcols = index_col.split(',')
                for col in ixcols:
                    if table.columns.has_key(col):
                        table.primary_key.columns[col] = table.columns[col]
                    else:
                        table.primary_key.columns[col] = table.columns[col.upper()]
            table.info = { "database": engine.url.database}
            return table
