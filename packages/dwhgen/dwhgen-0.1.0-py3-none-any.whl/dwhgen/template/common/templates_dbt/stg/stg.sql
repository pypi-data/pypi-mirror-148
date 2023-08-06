with

src_view as (

    select 
{%- for column in interface.columns %}
        {{column.name}}{{ "," if not loop.last }}
{%- endfor %}
    from {% raw %}{{{%- endraw %} source('{{schema_name}}','{{interface.name}}') {% raw %}}}{%- endraw %}

),

sor_delta as (

    select 
{%- for column in interface.columns %}
        {{column.name}}{{ "," if not loop.last }}
{%- endfor %}
    from yyypsa.psa_insert
    where source_system = '{{source.name}}' and interface_name = '{{interface.name}}' and ldts = (
        select max(ldts) from yyypsa.psa_insert
        where source_system = '{{source.name}}' and interface_name = '{{interface.name}}'
    )

)

select * from src_view