{%- set schema_file='zzzsrc_' ~ source.name | lower() %}
{%- set view_file='s3file' | lower() -%}

{%- raw %}
{{
    config(
        materialized='table'
    )
}}
{%- endraw %}

select 
	current_timestamp as ldts, 
	'{{source.name}}' as source_system,
	'{{interface.schema}}' as interface_schema,
	'{{interface.name}}' as interface_name,
	HASHTYPE_MD5(
    {%- for column in interface.primary_key.columns -%}
        {{ ' ||' if not loop.first}} json_value(
            payload, 
            '$.{{column.name}}' default 'n/a' on empty default 'n/a' on error) || '^~|'
    {%- endfor %}
    ) as bk, 
	payload
from (

	select
        yyypsa.importjsonfrom(
            '{{source.name}}',
            '{{interface.schema}}',
            '{{interface.name}}')

    from dual
)
