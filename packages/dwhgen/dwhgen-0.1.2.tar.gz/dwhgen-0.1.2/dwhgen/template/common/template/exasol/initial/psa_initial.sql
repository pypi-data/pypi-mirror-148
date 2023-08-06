create or replace connection geos to 'jdbc:db2://192.168.1.108:50000/testdb' user 'db2inst1' identified by 'start123';
create or replace connection epicor to 'jdbc:sqlserver://192.168.1.108:1433' user 'sa' identified by 'Pass@word';
create or replace connection dwhexa to 'localhost:8563' user 'sys' identified by 'exasol';
create schema if not exists yyypsa;
create or replace python3 scalar script
	yyypsa.importjsonfrom(
		source_system varchar(2000000),
		interface_schema varchar(2000000),
		interface_name varchar(2000000)
	) 
	emits (source_system varchar(2000000),
	       interface_schema varchar(2000000),
	       interface_name varchar(2000000),
	       payload varchar(2000000)) as 
import pyexasol
import os
import json
def run(ctx):
	C = pyexasol.connect(
		dsn=exa.get_connection('dwhexa').address, 
		user=exa.get_connection('dwhexa').user,
		password=exa.get_connection('dwhexa').password, 
		fetch_dict=True
		)
	sql = "SELECT * FROM ( IMPORT FROM JDBC AT %s STATEMENT 'select * from %s.%s')" % (ctx.source_system, ctx.interface_schema, ctx.interface_name)
	stmt = C.execute(sql)
	for row in stmt:
		ctx.emit(ctx.source_system.lower(), ctx.interface_schema.lower(), ctx.interface_name.lower(), json.dumps({k.lower():v for k, v in row.items()}))
	C.close()
;
create or replace table yyypsa.psa_insert (
	ldts timestamp not null,
	source_system varchar(2000000) not null,
	interface_schema varchar(2000000) not null,
	interface_name varchar(2000000) not null,
	bk hashtype not null,
	payload VARCHAR(2000000) not null
);
