{%- set view_prefix='s3view' | lower() -%}
{%- raw %}
{{
    config(
        materialized='incremental', cluster_by=['source_system,interface_name,bk,ldts']
    )
}}
{%- endraw %}

with 
{% for source in sources.values() -%}
{%- set schema_name='zzzsrc_' ~ source.name | lower() %}
{%- for interface in source.interfaces %}
{{source.name}}_{{interface.name}} as (

    select 
	*
	from {% raw %}{{{% endraw %} ref('{{source.name}}_{{interface.name}}') {% raw %}}}{% endraw %} 
),
{% endfor %}
{%- endfor %}
combined as (
{% for source in sources.values() %}
    {{'union all' if not loop.first }}
{%- for interface in source.interfaces %}
    select * from {{source.name}}_{{interface.name}}
    {{'union all' if not loop.last}}
{%- endfor %}
{% endfor %}
{%- raw %}{% if is_incremental() %}{% endraw %}
),

psa_latest as (

    select ldts,source_system, interface_name, index_col, bk, payload from 
    (
        select *,
            row_number() over (partition by source_system, interface_name, bk order by ldts desc) as ranked 
        from
            {% raw %}{{this}}{% endraw %}
    ) where ranked = 1
{% raw %}{% endif %}{% endraw %}
)

select
    
    current_timestamp() as ldts, source_system, interface_name, index_col, bk, payload

from combined

{% raw %}{% if is_incremental() %}{% endraw %}
where not exists 
(
    select 
        1 
    from psa_latest target 
    where 
        target.source_system=combined.source_system and 
        target.interface_name=combined.interface_name and
        target.index_col=combined.index_col and
        target.bk=combined.bk and 
        target.payload=combined.payload 

)
{% raw %}{% endif %}{% endraw %}
