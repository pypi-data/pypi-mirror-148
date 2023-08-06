import json
import yaml
from dataclasses import Field, dataclass, field
from typing import Dict, List, Set, Optional, Text
from enum import Enum
from pydantic import BaseModel, validator, Field
from pydantic.errors import PathError
from pathlib import Path
import glob
import subprocess as sp
import os
from os.path import dirname
import logging
import sys
import concurrent.futures
from meta import Source, Interface
from sqlalchemy import Table

project_exceptions = ['dbt_utils', 'dbt_expectations']

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

LOG = logging.getLogger('dbt_artifact')


class DbtResourceType(str, Enum):
    model = 'model'
    analysis = 'analysis'
    test = 'test'
    operation = 'operation'
    seed = 'seed'
    source = 'source'


class DbtMaterializationType(str, Enum):
    table = 'table'
    view = 'view'
    incremental = 'incremental'
    ephemeral = 'ephemeral'
    seed = 'seed'
    test = 'test'


class NodeDeps(BaseModel):
    nodes: List[str]


class NodeConfig(BaseModel):
    materialized: Optional[DbtMaterializationType]


class Node(BaseModel):
    unique_id: str
    name: str
    alias: Optional[str]
    database: str
    schema_name: str = Field(alias='schema')
    package_name: str
    original_file_path: str
    path: Path
    root_path: Path
    resource_type: DbtResourceType
    description: str
    fqn: Optional[List]
    tags: Optional[List]
    depends_on: Optional[NodeDeps]
    config: NodeConfig
    meta: Optional[Dict]
    source_name: Optional[str]
    source_description: Optional[str]
    source_meta: Optional[Dict]
    

class Manifest(BaseModel):
    nodes: Dict["str", Node]
    sources: Dict["str", Node]

    @validator('nodes', 'sources')
    def filter(cls, val):
        return {k: v for k, v in val.items() if v.resource_type.value in ('model', 'seed', 'source')}


class DbtProjectType(str, Enum):
    psa = 'psa'
    hardrule = 'hardrule'
    datavault = 'datavault'
    softrule = 'softrule'
    dimensional = 'dimensional'


@dataclass(unsafe_hash=True, eq=True)
class DbtProject():
    project_path: str = ''
    project_cfg: str = None
    project_type: DbtProjectType = None
    project_name: str = ''
    source_paths: List[str] = field(default_factory=list)
    data_paths: List[str] = field(default_factory=list)
    test_paths: List[str] = field(default_factory=list)
    analysis_paths: List[str] = field(default_factory=list)
    macro_paths: List[str] = field(default_factory=list)
    snapshot_paths: List[str] = field(default_factory=list)
    target_path: str = 'target'
    log_path: str = 'logs'
    modules_path: str = 'dbt_modules'
    initialized: bool = False
    manifest: Manifest = None


    @staticmethod
    def create_deck_hardrule(project_path: str, source_filter):
        dbt_files = glob.glob(project_path + "/00_src/**/dbt_project.yml", recursive=False)
        hardrules = []
        for dbt_file in dbt_files:
            with open(dbt_file, 'r') as f:
                py = yaml.safe_load(f)
                dbtproj = DbtProject(
                    project_path=dirname(f.name),
                    project_cfg=py
                )
                if dbtproj.project_type == DbtProjectType.hardrule and dbtproj.project_name in source_filter:
                    hardrules.append(dbtproj)
        return hardrules


    @staticmethod
    def create_psa(project_path: str):
        dbt_file = glob.glob(project_path + "/**/psa/dbt_project.yml", recursive=True)
        if len(dbt_file) == 1:
            with open(dbt_file[0], 'r') as f:
                py = yaml.safe_load(f)
                dbtproj = DbtProject(
                    project_path=dirname(f.name),
                    project_cfg=py
                )
                if dbtproj.project_type == DbtProjectType.psa:
                    return dbtproj


    @staticmethod
    def create_deck(project_path: str, prj_except: List):
        dbt_files = glob.glob(project_path + "/**/dbt_project.yml", recursive=True)
        dbts = {}
        hardrules = []
        datavaults = []
        psas = []
        softrules = []
        dimensionals = []
        dbts[DbtProjectType.psa]=psas
        dbts[DbtProjectType.hardrule]=hardrules
        dbts[DbtProjectType.datavault]=datavaults
        dbts[DbtProjectType.softrule]=softrules
        dbts[DbtProjectType.dimensional]=dimensionals
        for dbt_file in dbt_files:
            if not dirname(dirname(dbt_file)) in prj_except:
                with open(dbt_file, 'r') as f:
                    py = yaml.safe_load(f)
                    dbtproj = DbtProject(
                        project_path=dirname(f.name),
                        project_cfg=py
                    )
                    if dbtproj.project_type == DbtProjectType.hardrule:
                        hardrules.append(dbtproj)
                    elif dbtproj.project_type == DbtProjectType.psa:
                        psas.append(dbtproj)
                    elif dbtproj.project_type == DbtProjectType.datavault:
                        datavaults.append(dbtproj)
                    elif dbtproj.project_type == DbtProjectType.softrule:
                        softrules.append(dbtproj)
                    elif dbtproj.project_type == DbtProjectType.dimensional:
                        dimensionals.append(dbtproj)
        return dbts


    def __post_init__(self):
        if 'models' in self.project_cfg:
            #if not '+tags' in self.project_cfg['models']:
            #    raise RuntimeError('In {0} type (psa,hardrule,datavault,softrule,dimensional) must be set as +tags entry'.format(self.project_path))

            if '+tags' in self.project_cfg['models']:
                if DbtProjectType.hardrule in self.project_cfg['models']['+tags']:
                    self.project_type = DbtProjectType.hardrule
                elif DbtProjectType.psa in self.project_cfg['models']['+tags']:
                    self.project_type = DbtProjectType.psa
                elif DbtProjectType.datavault in self.project_cfg['models']['+tags']:
                    self.project_type = DbtProjectType.datavault
                elif DbtProjectType.softrule in self.project_cfg['models']['+tags']:
                    self.project_type = DbtProjectType.softrule
                elif DbtProjectType.dimensional in self.project_cfg['models']['+tags']:
                    self.project_type = DbtProjectType.dimensional
                else:
                    raise RuntimeError('In {0} type (psa,hardrule,datavault,softrule,dimensional) must be set as +tags entry'.format(self.project_path))

        self.project_name = self.project_cfg['name']

        if 'source-paths' in self.project_cfg:
            self.source_paths = self.project_cfg['source-paths']
        else:
            self.source_paths = ['models']
        if 'data-paths' in self.project_cfg:
            self.data_paths = self.project_cfg['data-paths']
        else:
            self.data_paths = ['data']
        if 'test-paths' in self.project_cfg:
            self.test_paths = self.project_cfg['test-paths']
        else:
            self.test_paths = ['test']
        if 'analysis-paths' in self.project_cfg:
            self.analysis_paths = self.project_cfg['analysis-paths']
        else:
            self.analysis_paths = ['analysis']
        if 'macro-paths' in self.project_cfg:
            self.macro_paths = self.project_cfg['macro-paths']
        else:
            self.macro_paths = ['macros']
        if 'snapsho-paths' in self.project_cfg:
            self.snapshot_paths = self.project_cfg['snapshot-paths']
        else:
            self.snapshot_paths = ['snapshots']

        if 'modules_path' in self.project_cfg:
            self.modules_path = self.project_cfg['modules_path']
        if 'target-path' in self.project_cfg:
            self.target_path = self.project_cfg['target-path']
        if 'log-path' in self.project_cfg:
            self.log_path = self.project_cfg


    def sources(self):
        srcs = {}
        if self.initialized:
            for source in self.manifest.sources:
                src_node = self.manifest.sources[source]
                if 'dburl' in src_node.source_meta:
                    src = None
                    if not src_node.source_name in srcs.keys():
                        src = Source(schema_name=src_node.schema_name,
                            name=src_node.source_name,
                            description=src_node.source_description,
                            connection_url=src_node.source_meta['dburl'])
                        srcs[src.name] = src
                    else:
                        src = srcs[src_node.source_name]
                    if src_node.meta:
                        interface = Interface(name=src_node.name,
                            schema_name=src_node.meta.get('source_schema', ''),
                            table_name=src_node.meta.get('source_name', src_node.name),
                            unique_index=src_node.meta.get('unique_index', ''),
                            description=src_node.description)
                        if src_node.meta.get('full'):
                            interface.full = True
                        if not src.interfaces:
                            src.interfaces = set()
                        src.interfaces.add(interface)
        return srcs


    def initialize(self):
        cmd = ['dbt', 'deps']
        cmp_rc, cmp_out = self.exec_dbt(cmd)
        if cmp_rc != 0:
            return cmp_rc, cmp_out

        cmd = ['dbt', 'compile']
        cmp_rc, cmp_out = self.exec_dbt(cmd)
        if cmp_rc == 0:
            mj = self.project_path + '/' + self.target_path + '/' + 'manifest.json'
            with open(mj, 'r') as fh:
                data = json.load(fh)
            self.manifest = Manifest(**data)
            self.initialized = True
        return cmp_rc, cmp_out


    def run(self):
        if not self.initialized:
            self.initialize()
        cmd = ['dbt', 'run']
        return self.exec_dbt(cmd)

    def test(self):
        if not self.initialized:
            self.run()
        cmd = ['dbt', 'run']
        return self.exec_dbt(cmd)

    def docs(self):
        if not self.initialized:
            self.initialize()
        cmd = ['dbt', 'docs', 'generate']
        return self.exec_dbt(cmd)

    def exec_dbt(self, cmd):
        cmd = cmd + ['--project-dir', self.project_path,
                     '--profiles-dir', self.project_path]
        LOG.debug(cmd)
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT) as process:
            try:
                outs, errs = process.communicate(timeout=15)
                returncode = process.wait()
                if returncode == 0:
                    LOG.info('DbtProjet {0} {1} succeeded.'.format(
                        cmd[1], self.project_name))
                else:
                    LOG.error('DbtProjet {0} {1} failed.'.format(
                        cmd[1], self.project_name))
                    LOG.error(outs)

                return returncode, outs
            except sp.TimeoutExpired:
                process.kill()
                outs, errs = process.communicate()
                return -1, outs


def initialize_dbt(dbtProject):
    return dbtProject.initialize()

