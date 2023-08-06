# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dwhgen']

package_data = \
{'': ['*'],
 'dwhgen': ['template/common/template/exasol/initial/*',
            'template/common/template/exasol/interface/*',
            'template/common/templates/dbt/*',
            'template/common/templates/psa/*',
            'template/common/templates/source_schema/*',
            'template/common/templates_dbt/src/*',
            'template/common/templates_dbt/stg/*',
            'template/exasol/templates/dbt/*',
            'template/exasol/templates_dbt/stg/*']}

install_requires = \
['HiYaPyCo>=0.4.16,<0.5.0',
 'SQLAlchemy==1.3.23',
 'dbt-exasol>=1.0.3,<2.0.0',
 'dbt>=0.21.1,<0.22.0',
 'ibm-db-sa>=0.3.7,<0.4.0',
 'markupsafe==2.0.1',
 'pydantic>=1.8.2,<2.0.0',
 'pyexasol>=0.21.1,<0.22.0',
 'pymssql>=2.2.2,<3.0.0',
 'pysqlite3>=0.4.6,<0.5.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'sqlalchemy-exasol>=2.2.0,<3.0.0',
 'sqlalchemy-pysqlite3>=0.0.4,<0.0.5',
 'sqlfluff>=0.8.1,<0.9.0',
 'yamlreader>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['dwhgen = dwhgen.main:main']}

setup_kwargs = {
    'name': 'dwhgen',
    'version': '0.1.2',
    'description': 'generating schema YAML and models for source system interfaces and PSA historization',
    'long_description': None,
    'author': 'Torsten Glunde',
    'author_email': 'torsten@glunde.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
