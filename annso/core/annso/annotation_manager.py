#!env/python3
# coding: utf-8
import ipdb

import os
import json
import datetime
import uuid
import psycopg2
import hashlib
import asyncio
import ped_parser



from config import *
from core.framework.common import *
from core.model import *




# =====================================================================================================================
# ANNOTATION DATABASE MANAGER
# =====================================================================================================================
# Format of data
# ref_list  : contains the list of available genome referencial
#              { <ref_id>: <ref_name> }
# db_list   : contains the list of available annotation databases according to the referencial
#              { <ref_id>:  {
#                   'order': [<db_name_ui>, ...],
#                   'db'   : {
#                       <db_name_ui>: {
#                           'versions': { <version_name>: <db_uid>, ... },
#                           'desc': <db_description>
#              }}}
# db_map    : contains the data for all annotation databases
#              { <db_uid>: {
#                   'uid': <db_uid>
#                   'fields':
#                   'name'
#                   'description'
#                   'order'
#                   ...
#               }}
# fields_map:


class AnnotationManager:
    def __init__(self):
        run_until_complete(self.load_annotation_metadata())


    async def load_annotation_metadata(self):
        self.ref_list = {}
        self.db_list = {}
        self.db_map = {}
        self.fields_map = {}

        query = "SELECT d.uid, d.reference_id, d.version, d.name_ui, d.description, d.url, r.name \
                 FROM annotation_database d INNER JOIN reference r ON r.id=d.reference_id \
                 ORDER BY r.name ASC, d.ord ASC, version DESC"
        result = await execute_aio(query)
        for row in result:
            self.ref_list.update({row.reference_id: row.name})
            if row.reference_id in self.db_list.keys():
                if row.name_ui in self.db_list[row.reference_id].keys():
                    self.db_list[row.reference_id][row.name_ui]["versions"][row.version] = row.uid
                else:
                    self.db_list[row.reference_id]['order'].append(row.name_ui)
                    self.db_list[row.reference_id]['db'][row.name_ui] = {"name": row.name_ui, "description": row.description, "versions": {row.version: row.uid}}
            else:
                self.db_list[row.reference_id] = {'order': [row.name_ui], 'db': {row.name_ui: {"name": row.name_ui, "description": row.description, "versions": {row.version: row.uid}}}}

        query = "SELECT d.uid AS duid, d.reference_id AS ref, d.version, d.ord AS dord, d.name_ui AS dname, d.description AS ddesc, d.update_date AS ddate, a.uid AS fuid, a.name_ui AS name, a.ord AS ford, a.type AS type, a.description AS desc, a.meta AS meta \
                 FROM annotation_field a \
                 INNER JOIN annotation_database d ON a.database_uid=d.uid \
                 ORDER BY d.uid, a.ord"
        result = await execute_aio(query)
        for row in result:
            meta = None if row.meta is None else json.loads(row.meta)
            self.fields_map[row.fuid] = {"uid": row.fuid, "name": row.name, "description": row.desc, "type": row.type, "meta": meta, "order": row.ford, "dbuid": row.duid}
            if row.duid in self.db_map.keys():
                self.db_map[row.duid]["fields"].append(row.fuid)
            else:
                self.db_map[row.duid] = {"uid": row.duid, "name": row.dname, "description": row.ddesc, "order": row.dord, "update": row.ddate, "fields": [row.fuid], "version": row.version, "ref": row.ref}


    # build the sql query according to the annso filtering parameter and return result as json data
    def get_databases(self):
        return self.db_map


    def get_fields(self):
        return self.fields_map 
