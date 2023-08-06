import argparse
import logging
import logging.config
import os
import sys
import tempfile
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from dbtparse import DbtProject, DbtProjectType
from meta import DBMSMeta

APPNAME="dbt-dwhgen"
this_dir, this_filename = os.path.split(__file__)
TEMPLATE_PATH = '{}{}'.format(this_dir, '/template/exasol/templates')
TEMPLATE_PATH_DBT = '{}{}'.format(this_dir, '/template/exasol/templates_dbt')
TARGET_PATH='./target'
LOG_LEVEL=logging.INFO
LOG = logging.getLogger(APPNAME)


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sources', required=True)
    parser.add_argument('-p' '--project', required=True)
    parser.add_argument('-d', '--database', default='exasol')

    args = parser.parse_args()
    TEMPLATE_PATH = '{}/template/{}/templates'.format(this_dir, args.database)
    TEMPLATE_PATH_DBT = '{}/template/{}/templates_dbt'.format(this_dir, args.database)
    TARGET_PATH='{}/dwhgen'.format(tempfile.gettempdir())
    os.makedirs(TARGET_PATH)
    LOG.info('Temporary target path: {}'.format(TARGET_PATH))
    source_list = args.sources.split(',')
    dbt_deck = DbtProject.create_deck_hardrule(args.p__project, source_list  )

    tables = []
    sources = {}
    for dbt in dbt_deck:
        rc, output = dbt.initialize()
        if rc != 0:
            LOG.error(output)
            return -1
            
        localsrc = dbt.sources()
        
        for source in localsrc.values():
            sources[source.name] = source
            for interface in source.interfaces:                
                table = DBMSMeta.read(source.name, interface.table_name,
                    interface.schema_name,
                    interface.unique_index,
                    source.connection_url)
                interface.table = table
                tables.append(table)

    start = time.time()

    LOG.info("Starting templates:")
    for table in tables:
        env = Environment(
            loader=FileSystemLoader(TEMPLATE_PATH),
            autoescape=select_autoescape(['sql','yml'])
        )
        for k,v in os.environ.items():
            env.globals[k]=v

        result = list(Path(TEMPLATE_PATH).glob('**/*.sql'))
        result.extend(list(Path(TEMPLATE_PATH).glob('**/*.yml')))
        for entry in result:
            template = env.get_template(str(entry.relative_to(TEMPLATE_PATH).as_posix())).render(tables=tables,sources=sources)
            target_dir = '{}/{}/'.format(TARGET_PATH, entry.parent.name)
            if not Path(target_dir).exists():
                os.makedirs(target_dir)
            with open('{}/{}'.format(target_dir, entry.name), 'w') as f:
                f.write(template)

        env = Environment(
            loader=FileSystemLoader(TEMPLATE_PATH_DBT),
            autoescape=select_autoescape(['sql','yml'])
        )
        for k,v in os.environ.items():
            env.globals[k]=v
        for source in sources.values():
            for interface in source.interfaces:
                template = env.get_template('stg/stg.sql').render(source=source,interface=interface)
                target_dir = '{}/dbt/stg/'.format(TARGET_PATH)
                if not Path(target_dir).exists():
                    os.makedirs(target_dir)
                with open('{}/stg_{}_{}_{}.sql'.format(target_dir, source.name, interface.table.schema, interface.table.name), 'w') as f:
                    f.write(template)

                #template = env.get_template('src/psa_src.sql').render(source=source,interface=interface)
                target_dir = '{}/dbt/'.format(TARGET_PATH)
                if not Path(target_dir).exists():
                    os.makedirs(target_dir)
                with open('{}/{}_{}_{}.sql'.format(target_dir, source.name, interface.table.schema, interface.table.name), 'w') as f:
                    f.write(template)
                    
    end = time.time()
    LOG.info('Execution finished in {}.'.format((end-start)))


if __name__ == '__main__':
    sys.exit(main())
