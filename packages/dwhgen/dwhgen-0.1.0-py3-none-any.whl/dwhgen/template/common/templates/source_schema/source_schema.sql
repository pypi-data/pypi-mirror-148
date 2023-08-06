USE DATABASE {% raw %}{{ dbname }}{% endraw %};
{%- set view_prefix='s3view' | lower() -%}
{%- set exttable_prefix='s3ext' | lower() -%}
{%- set file_format_name='gvl_datalake' -%}
{%- set env='test' %}
{%- set elt_role='{{ elt_role }}' %}
{%- set dvb_role='{{ dvb_role }}' %}
{%- set tst_role='{{ tst_role }}' %}
{%- for source in sources.values() -%}
{%- set schema_name='zzzsrc_' ~ source.name | lower() %}
create transient schema if not exists {{schema_name}};
create file format if not exists {{schema_name}}.{{file_format_name}} type='parquet';
create stage if not exists {{schema_name}}.s3file
    file_format={{schema_name}}.{{file_format_name}}
    url='s3://{% raw %}{{ bucket_name }}{% endraw %}'
    credentials=(aws_key_id='{% raw %}{{ access_key }}{% endraw %}',aws_secret_key='{% raw %}{{ secret_key }}{% endraw %}');

{% for interface in source.interfaces %}
create or replace external table {{schema_name}}.{{exttable_prefix}}_{{interface.name}}
    with location = @{{schema_name}}.s3file/{{interface.info.database}}/{{interface.schema}}/{{interface.name}}/
    auto_refresh = true
    file_format = {{schema_name}}.{{file_format_name}}
    pattern = '.*parquet';
{% endfor %}

grant usage on schema {{schema_name}} to role {{elt_role}};
grant select on all tables in schema {{schema_name}} to role {{elt_role}};
grant select on all views in schema {{schema_name}} to role {{elt_role}};
grant select on all external tables in schema {{schema_name}} to role {{elt_role}};
grant usage on schema {{schema_name}} to role {{dvb_role}};
grant select on all tables in schema {{schema_name}} to role {{dvb_role}};
grant select on all views in schema {{schema_name}} to role {{dvb_role}};
grant select on all external tables in schema {{schema_name}} to {{dvb_role}};
grant usage on schema {{schema_name}} to role {{tst_role}};
grant select on all tables in schema {{schema_name}} to role {{tst_role}};
grant select on all views in schema {{schema_name}} to role {{tst_role}};
grant select on all external tables in schema {{schema_name}} to {{tst_role}};

{%endfor%}
