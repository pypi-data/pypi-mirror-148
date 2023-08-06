from typing import List, Set
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import os


@dataclass_json
@dataclass
class JdbcDataType:
    character_maximum_length: int
    data_type_name: str
    jdbc_data_type_id: int
    numeric_precision: int
    numeric_scale: int


@dataclass_json
@dataclass
class Column:
    column_id: str
    column_order: int
    column_comment: str
    column_name: str
    complete_data_type: str
    jdbc_data_type: JdbcDataType


@dataclass_json
@dataclass
class Hub:
    hub_id: str
    hub_comment: str
    hub_id_of_alias_parent: str
    hub_name_of_alias_parent: str
    hub_subject_area_name: str


@dataclass_json
@dataclass
class HubLoad:
    business_key_prefix: str
    business_key_short: str
    columns: Set[Column]
    datavault_category_id: str
    hub_id: str
    hub_load_display_name: str
    hub_load_id: str
    keys_are_prehashed: bool
    keys_are_unique: bool
    staging_table_id: str
    system_id: str
    system_name: str


@dataclass_json
@dataclass
class Satellite:
    column_ids: List
    functional_suffix_id: str
    functional_suffix_name: str
    hub_id: str
    satellite_comment: str
    satellite_id: str
    satellite_is_prototype: bool
    satellite_subject_area_name: str
    staging_resource_id: str
    staging_table_id: str
    system_id: str


@dataclass_json
@dataclass
class LinkLoad:
    link_id: str
    link_load_display_name: str
    link_load_id: str
    staging_table_id: str
    system_id: str


@dataclass_json
@dataclass
class Link:
    hub_a_id: str
    hub_b_id: str
    link_comment: str
    link_id: str
    link_subject_area_name: str
    link_suffix_id: str
    link_suffix_name: str
    link_type: str


@dataclass_json
@dataclass
class SourceSystem:
    deployable: bool
    hidden_in_system_deployment: bool
    source_type_id: str
    source_type_name: str
    source_type_parameters: List
    source_type_url: str
    system_color: str
    system_comment: str
    system_id: str
    system_name: str


@dataclass_json
@dataclass
class StagingTable:
    columns: List[Column]
    loading_batch_size: int
    source_schema_name: str
    source_schema_or_system_id: str
    source_table_id: str
    source_table_name: str
    source_table_staging_id: str
    source_table_type_id: str
    staging_table_comment: str
    staging_table_id: str
    staging_table_name: str
    system_id: str
    where_clause_delta_part_template: str
    where_clause_general_part: str


path = r"/home/torsten/project/dwh_2020/datavault/dvb/datavaultbuilder_objects/staging/staging_tables/"
directories = os.listdir( path )

for file in os.scandir(path):  
    if file.is_file():
        fs = open("{}/{}".format(path,file.name),'r')
        stg = StagingTable.from_json(fs.read())
        print(stg)

