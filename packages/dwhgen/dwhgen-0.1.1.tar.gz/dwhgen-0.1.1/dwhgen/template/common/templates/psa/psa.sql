{%- set elt_role='{{ elt_role }}' %}
{%- set dvb_role='{{ dvb_role }}' %}
USE DATABASE {% raw %}{{ dbname }}{% endraw %};
create transient schema if not exists yyypsa;
grant usage on schema yyypsa to role {{elt_role}};
grant select on all tables in schema yyypsa to role {{elt_role}};
grant select on all views in schema yyypsa to role {{elt_role}};
grant usage on schema yyypsa to role {{dvb_role}};
grant select on all tables in schema yyypsa to role {{dvb_role}};
grant select on all views in schema yyypsa to role {{dvb_role}};

create transient table yyypsa.psa_insert (
    ldts timestamp, 
    source_system varchar(200),
    interface_name varchar(200),
    bk binary(32),
    index_col varchar(200),
    payload variant) 
if not exists;
create transient table yyypsa.psa_delete (
    dlts timestamp, 
    source_system varchar(200),
    interface_name varchar(200),
    bk binary(32),
    index_col varchar(200),
    payload variant) 
if not exists;

{%- for source in sources.values() -%}
{%- set schema_name='yyypsa_' ~ source.name | lower() %}
create transient schema if not exists {{schema_name}};
grant usage on schema {{schema_name}} to role {{elt_role}};
grant select on all tables in schema {{schema_name}} to role {{elt_role}};
grant select on all views in schema {{schema_name}} to role {{elt_role}};
grant usage on schema {{schema_name}} to role {{dvb_role}};
grant select on all tables in schema {{schema_name}} to role {{dvb_role}};
grant select on all views in schema {{schema_name}} to role {{dvb_role}};

{%- for interface in source.interfaces %}

create view if not exists {{schema_name}}.{{interface.name}} as (
select 
    ldts, 
{%- for column in interface.columns %}
{% if (column.type | string()).startswith('TIMESTAMP') -%}
    try_to_timestamp( parse_json(payload):{{column.name}}::varchar) as {{column.name}}{{ ", " if not loop.last }}
    {%- elif (column.type | string()).startswith('DATE') -%}
    try_to_date( parse_json(payload):{{column.name}}::varchar) as {{column.name}}{{ ", " if not loop.last }}
    {%- elif (column.type | string()).startswith('TIME') -%}
    try_to_TIME( parse_json(payload):{{column.name}}::varchar) as {{column.name}}{{ ", " if not loop.last }}
{%- else -%}
    parse_json(payload):{{column.name}}::{{column.type}} as {{column.name}}{{ ", " if not loop.last }}
{%- endif %}
{%- endfor %}
from (
    select 
        payload, ldts , rank() over (partition by source_system,interface_name,bk order by ldts desc) as latest
    from yyypsa.psa_insert where source_system = '{{source.name}}' and interface_name = '{{interface.name}}'
    ) psa where psa.latest=1
);

{% endfor %}

{% endfor -%}
