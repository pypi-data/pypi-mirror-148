

import json
import sys
from dataclasses import dataclass, field
from typing import List
from io import StringIO


@dataclass
class Column:
    column_name: str
    source_name: str = None
    data_type: str = 'string'
    is_key: bool = False
    is_hidden: bool = False

    @staticmethod
    def md_header(self) -> List[str]:
        return ['| Column | Source | Type | Key | Hidden |\n', 
                '| ------ | ------ | --- | --- | --- |\n']

    def md_rows(self) -> List[str]:
        return [ "|{0}|{1}|{2}|{3}|{4}|\n".format(self.column_name, self.source_name, self.data_type, self.is_key, self.is_hidden) ]


@dataclass
class Table:
    table_name: str
    columns: List[Column] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)

    def md_header(self) -> List[str]:
        return [ "### Table: {0}\n".format(self.table_name) ]

    def md_column_table(self) -> List[str]:
        lines = Column.md_header(self)
        for col in self.columns:
            lines = lines + col.md_rows()
        return lines

    def md_partitions(self) -> List[str]:
        lines = [ "- Partition source: \n", "```\n" ]
        for src in self.sources:
            for line in src.get('expression', '').splitlines():
                lines.append("{0}\n".format(line)) 
        return lines + [ "\n```\n" ]


@dataclass
class Query:
    name: str
    sql: str = None
    database: str = None
    query_group: str = None
    expression: List[str] = field(default_factory=list)
    
    def md_header(self) -> List[str]:
        return [
            "### Query: {0}\n".format(self.name),
            "\n",
            "- Database: {0}\n".format(self.database),
            "- Query Group: {0}\n".format(self.query_group),
            "- Sql: \n"
        ]

    def md_sql(self) -> List[str]:
        return [
            "```\n",
            "{0}\n".format(self.sql),
            "```\n"
        ]

    def md_expression(self) -> List[str]:
        list = [ "- Expressions: \n", "```\n" ]
        for exp in self.expression:
            list = list + [ "{0}\n".format(exp) ]
        return list + [ "```\n" ]


@dataclass
class Report:
    report_name: str
    queries: List[Query] = None
    tables: List[Table] = None

    def render_md(self) -> StringIO:
        output = StringIO()
        output.writelines( [ "# {0}\n".format(self.report_name), " \n" ])
        output.writelines( [ "## Expressions\n" ])
        if self.queries:
            for query in self.queries:
                output.writelines(query.md_header())
                output.writelines(query.md_sql())
                output.writelines(query.md_expression())
        if self.tables:
            output.writelines( [ "## Tables\n" ])
            for table in self.tables:
                output.writelines(table.md_header())
                output.writelines(table.md_column_table())
                output.writelines("\n")
                output.writelines(table.md_partitions())
        return output


def parse_query(json_model) -> List[Query]:
    if not 'expressions' in json_model:
        return None
    queries = []
    for exp in json_model['expressions']:
        query = Query(exp['name'])
        queries.append(query)
        expStr = exp['expression']
        idb = int(expStr.find('Database("'))
        edb = int(expStr.find('\"]),'))
        isql = int(expStr.find('Query="'))
        query.database = expStr[idb+9:isql-2]
        sql = expStr[isql+7:edb].replace('\n', '')
        sql = sql.replace('#(lf)', '\n')
        sql = sql.replace('#(tab)', '\t')
        query.sql = sql
        expressions = expStr[edb+5:len(expStr)]
        for line in expressions.splitlines():
            if line.find('#') > 0:
                query.expression.append(line)
        if 'queryGroup' in exp:
            query.query_group = exp['queryGroup']
    return queries


def parse_table(json_model) -> List[Table]:
    if not 'tables' in json_model:
        return
    tables = []
    for tab in json_model['tables']:
        table = Table(tab['name'])
        tables.append(table)
        for col in tab['columns']:
            column = Column(col['name'])
            column.data_type = col.get('dataType', 'string')
            column.is_key = col.get('isKey', False)
            column.is_hidden = col.get('isHidden', False)
            column.source_name = col.get('sourceColumn', None)
            table.columns.append(column)
        for part in tab['partitions']:
            table.sources.append(part['source'])
    return tables


def main():
    data = json.load(sys.stdin)
    model = data['model']
    report = Report('reportname')
    report.queries = parse_query(model)
    report.tables = parse_table(model)
    print(report.render_md().getvalue())


if __name__ == '__main__':
    sys.exit(main())
