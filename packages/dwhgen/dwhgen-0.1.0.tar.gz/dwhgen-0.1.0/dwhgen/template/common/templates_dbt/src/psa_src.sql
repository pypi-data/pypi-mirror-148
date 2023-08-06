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
        '{{source.name}}'::varchar(200) as source_system,
        '{{interface.name}}'::varchar(200) as interface_name,
        parse_json('[{% for column in interface.primary_key.columns -%}
            {{',' if not loop.first }}"{{column.name}}" 
         {%- endfor %}]')::variant as index_col,
 
    sha2_binary(
    {%- for column in interface.primary_key.columns -%}
          {{ ' ||' if not loop.first}} parse_json($1):{{column.name}} || '^~|'
    {%- endfor %})::binary as bk, 

        $1 as payload

    from @{{schema_file}}.{{view_file}}/{{interface.info.database}}/{{interface.schema}}/{{interface.name}}/
