{% macro render_type(column) -%}
{%- if column.doc in ('DECIMAL','REAL','NUMBER','DOUBLE','FLOAT') -%}
{%- if column.type.scale and column.type.scale==0 -%}
bigint
{%- else -%}
decimal(36,12)
{%- endif %}
{%- elif column.doc in ('BOOL','BOOLEAN','BIT') -%}
boolean
{%- elif column.doc in ('DATE') -%}
date
{%- elif column.doc in ('TIMESTAMP','DATETIME','DATETIME2','TIME') -%}
timestamp
{%- elif column.doc in ('INTEGER','SMALLINT','BIGINT') -%}
bigint
{%- else -%}
varchar(2000000)
{%- endif %}
{%- endmacro %}
with

seed as (

{% raw %}{% if target.name == 'ci' %}{%- endraw %}
    select 
{%- for column in interface.table.columns %}
        cast( {{column.name| lower()}} as {{render_type(column)}}) as "{{column.name| upper()}}"{{ "," if not loop.last }}
{%- endfor %}
    from {% raw %}{{{%- endraw %} source('{{source.name}}','{{source.name}}_{{interface.table.schema}}_{{interface.table.name}}') {% raw %}}}{%- endraw %}
{% raw %}{% else %}{%- endraw %}
    select 'seed' as seedname from dual
{% raw %}{% endif %}{%- endraw %}

),

sor_view_delta as (

    select
{%- for column in interface.table.columns %}
        cast( json_value( payload, '$.{{column.name | lower()}}') as {{render_type(column)}}) as "{{column.name| upper()}}"{{ "," if not loop.last }}
{%- endfor %}
{% if interface.full %}
    from (
    	select payload from (
    		select payload, row_number() over(partition by source_name, interface_schema, interface_name, bk order by ldts desc) as latestrecord
    		from yyy_q3_psa.psa_insert
		    where source_name = '{{source.name}}' and interface_schema='{{interface.schema_name}}' and interface_name = '{{interface.table.name}}'
    	) where latestrecord=1
    )
{%- else %}
    from yyy_q3_psa.psa_insert
    where source_name = '{{source.name}}' and interface_schema='{{interface.schema_name}}' and interface_name = '{{interface.table.name}}'
        and ldts = (
            select max(ldts)
            from yyy_q3_psa.psa_insert
            where source_name = '{{source.name}}' and interface_schema='{{interface.schema_name}}' and interface_name = '{{interface.table.name}}'
        )
{%- endif %}
)
{% raw %}{% if target.name == 'ci' %}{%- endraw %}
select * from seed
{% raw %}{% else %}{%- endraw %}
select * from sor_view_delta
{% raw %}{% endif %}{%- endraw %}
