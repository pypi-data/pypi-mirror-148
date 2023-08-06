import warnings
import os
import sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine, MetaData, Table, func, select
import sqlalchemy.types as sq
import sqlalchemy.dialects as sd
from sqlalchemy import exc as sa_exc
import numpy as np


USER_NAME = os.getenv('PIPE_USER', None)
USER_PWD = os.getenv('PIPE_PWD', None)
HOST_NAME = os.getenv('PIPE_HOST', None)
DB_NAME = os.getenv('PIPE_DB', 'nucleus')
TABLE_NAME = os.getenv('PIPE_TABLE', None)
SCHEMA_NAME = os.getenv('PIPE_SCHEMA', None)
APPNAME = 'csv2parquet'
DRIVER_NAME = os.getenv('PIPE_DRIVER', 'postgresql+psycopg2')
CONNECTION_STRING = '{}://{}:{}@{}/{}?application_name="{}"'.format(
    DRIVER_NAME, USER_NAME, USER_PWD, HOST_NAME, DB_NAME, APPNAME)
PARTITIONS = os.getenv('PIPE_PARTITION', 4)
TARGET_ROOT_LOCAL = os.getenv('PIPE_TARGET_LOCAL', '~/')
CHUNK_SIZE = os.getenv('PIPE_CHUNKSIZE', '100000')

PA_BOOL = pa.bool_()
PA_FLOAT32 = pa.float32()
PA_FLOAT64 = pa.float64()
PA_INT8 = pa.int8()
PA_INT16 = pa.int16()
PA_INT32 = pa.int32()
PA_INT64 = pa.int64()
PA_STRING = pa.string()
PA_TIMESTAMP = pa.timestamp('ns')
PA_BINARY = pa.binary()

def convert(table: Table): 
    fields = []
    for column in table.columns:
        paType = None
        if type(column.type) in (sq.Float,sq.Numeric,sq.NUMERIC):
            paType = PA_FLOAT64
        elif type(column.type) in (sq.Unicode,sq.Text,sq.String,sq.VARCHAR,sq.TEXT,sq.CLOB):
            paType = PA_STRING
        elif type(column.type) in (sq.BigInteger,sq.Integer,sq.SmallInteger, sq.BIGINT, sq.INTEGER):
            paType = PA_INT64
        elif type(column.type) in (sq.Binary,sq.BLOB):
            paType = PA_BINARY
        elif type(column.type) in (sq.BOOLEAN, sq.Boolean):
            paType = PA_STRING
        elif type(column.type) in (sq.TIMESTAMP, sq.DATETIME, sq.DateTime,sd.postgresql.base.TIMESTAMP):
            paType = PA_STRING
        elif type(column.type) in (sq.Date,sq.Time,sq.DATE,sq.TIME):
            paType = PA_STRING
        else:
            raise Exception("unknown sql datatype: {}".format(column.type) )
        fields.append(pa.field(column.name, paType))
    return pa.schema(fields)


def append_to_parquet_table(dataframe, filepath=None, writer=None, paSchema=None, dtypeSchema=None):
    """Method writes/append dataframes in parquet format.

    This method is used to write pandas DataFrame as pyarrow Table in parquet format. If the methods is invoked
    with writer, it appends dataframe to the already written pyarrow table.

    :param dataframe: pd.DataFrame to be written in parquet format.
    :param filepath: target file location for parquet file.
    :param writer: ParquetWriter object to write pyarrow tables in parquet format.
    :return: ParquetWriter object. This can be passed in the subsequenct method calls to append DataFrame
        in the pyarrow Table
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    for colname in dtypeSchema:
        if dataframe[colname].dtype != dtype_schema[colname]:
            if dtype_schema[colname] is not np.bool:
                dataframe[colname] = dataframe[colname].astype(dtype_schema[colname], copy=False)
        if dtype_schema[colname] == np.str:
            dataframe[colname].replace('nan','', inplace=True)

    table = pa.Table.from_pandas(dataframe, schema=paSchema)
    if writer is None:
        writer = pq.ParquetWriter(where=filepath, 
                                  schema=table.schema, 
                                  compression="snappy")
    writer.write_table(table=table)
    return writer


def convertDtypes(table: Table):
    dtypes = {}
    for column in table.columns:
        if type(column.type) in (sq.Float,sq.Numeric,sq.NUMERIC):
            pdType = np.float64
        elif type(column.type) in (sq.Unicode,sq.Text,sq.String,sq.VARCHAR,sq.TEXT,sq.CLOB):
            pdType = np.str
        elif type(column.type) in (sq.BigInteger,sq.Integer,sq.SmallInteger, sq.BIGINT, sq.INTEGER):
            pdType = "Int64"
        elif type(column.type) in (sq.Binary,sq.BLOB):
            pdType = np.binary
        elif type(column.type) in (sq.BOOLEAN, sq.Boolean):
            pdType = np.bool
        elif type(column.type) in (sq.TIMESTAMP, sq.DATETIME, sq.DateTime,sd.postgresql.base.TIMESTAMP):
            pdType = np.object
        elif type(column.type) in (sq.Date,sq.Time,sq.DATE,sq.TIME):
            pdType = np.object
        else:
            raise Exception("unknown sql datatype: {}".format(column.type) )
        dtypes[column.name]=pdType
    return dtypes


def tableMetadata(connection: str, schema_name: str, table_name: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        db_engine = create_engine(connection)
        metadata = MetaData()
        sqlTable = Table(table_name, metadata, schema=schema_name, autoload=True,
                        autoload_with=db_engine)
        rowQuery = select([func.count()]).select_from(sqlTable)
        rows = db_engine.scalar(rowQuery)
        return sqlTable, rows


schema_name = SCHEMA_NAME
table_name = TABLE_NAME
parquet_root = '{}/target/{}/{}/{}/'.format(
                                           TARGET_ROOT_LOCAL,
                                           DB_NAME,
                                           schema_name,
                                           table_name)
if not os.path.exists(parquet_root):
    os.makedirs(parquet_root)

sqlTable, rows = tableMetadata(CONNECTION_STRING, schema_name, table_name)
rows_per_partition = int(round(rows / 8))
dtype_schema = convertDtypes(sqlTable)
paSchema = convert(sqlTable)
chunksize = min([int(CHUNK_SIZE), rows_per_partition])
writer = None
partition_row_count = 0
partition_number = 1
parquet_file = '{}{}{}.parquet'.format(parquet_root, table_name, partition_number)
for chunk in pd.read_csv(sys.stdin,
                         sep=',',
                         chunksize=chunksize,
                         iterator=True,
                         low_memory=False,
                         encoding='utf-8'):
    writer = append_to_parquet_table(chunk, parquet_file, writer, paSchema, dtype_schema);
    partition_row_count += len(chunk)
    if partition_row_count >= rows_per_partition:
        partition_row_count = 0
        partition_number += 1
        writer = None
        parquet_file = '{}/{}{}.parquet'.format(parquet_root, table_name, partition_number)
