#!env/python3
# coding: utf-8
import ipdb

import os
import shutil
import json
import tarfile
import datetime
import time
import uuid
import subprocess
import requests
import psycopg2


from core.framework import *
from core.model import *
from core.report import *
from core.vcf import import_vcf









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# CORE OBJECT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Core:
    def __init__(self):
        self.annotation_db = AnnotationDatabaseManager()
        self.analysis = AnalysisManager()
        self.sample = SampleManager()
        self.variant = VariantManager()
        self.filter = FilterEngine()
        self.file = FileManager()
        # self.selection = SelectionManager()

        # Todo
        pass



    def init(self):
        """
            Do some verifications on the server to check that all is good.
             - check that config parameters are consistency
             - check that 
        """
        pass

    def get_report(self, variants_ids, report_template=None, report_lang=None, report_option=None):
        # Retrieve gene from variant ids list
        return Gene("GJB2", [])
        result = []
        sql =  "SELECT v.chr, v.pos, v.ref, v.alt, array_agg(rg.name) "
        sql += "FROM variant_hg19 v "
        sql += "INNER JOIN refgene_hg19 rg ON v.chr = rg.chrom AND rg.txrange @> int8(v.pos) "
        sql += "WHERE v.id IN (" + ','.join(variants_ids) + ") GROUP BY v.id"
        for r in db_engine.execute():
            result.append((r[1], r[0], r[3], r[4], r[5], r[6]))



        return Gene("GJB2", [])
    

    def notify_all(self, json):
        print ("Core Notify All : " + str(json))

 


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# FILE MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class FileManager:
    def __init__(self):
        self.fields_map = {}
        self.db_map = {}



    def upload_init(self, filename, file_size, metadata={}):
        """ 
            Create an entry for the file in the database and return the id of the file in annso
            This method shall be used to init a resumable upload of a file 
            (the file is not yet available, but we can manipulate its annso metadata)
        """
        # TODO : test file extension if ["vcf", "gvcf", "vcf.gz", "gvcf.gz"] : sample file, otherwise ...
        sample_file = File.new_from_tus(filename, file_size)
        return sample_file.id



    def upload_finish(self, file_id, checksum=None, checksum_type="md5"):
        """ 
            When upload of a file is finish, we move it from the download temporary folder to the
            files folder. A checksum validation can also be done if provided. 
            Update finaly the status of the file to UPLOADED or CHECKED -> file ready to be used
        """
        # Retrieve file
        ipdb.set_trace()
        file = File.from_id(file_id)
        if file == None:
            raise AnnsoException("Unable to retrieve the file with the provided id : " + file_id)
        # Move file
        old_path = file.path
        new_path = os.path.join(FILES_DIR, "{0}.{1}".format(uuid.uuid4(), file.type))
        os.rename(old_path, new_path)
        # If checksum provided, check that file is correct
        file_status = "UPLOADED"
        if checksum is not None:
            if checksum_type == "md5" and md5(fullpath) != checksum : 
                raise error
            file_status = "CHECKED"            
        # Update file data in database
        file.upload_offset = file.size
        file.status = file_status
        file.path = new_path

        db_session.add(file)
        db_session.commit()

        import_vcf(file.id, file.path, annso)

        # Notify all about the new status
        # msg = {"action":"file_changed", "data" : [pfile.to_json_data()] }
        # annso.notify_all(json.dumps(msg))
        # TODO : check if run was waiting the end of the upload to start


 


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANNOTATION DATABASE MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnnotationDatabaseManager:
    def __init__(self, reference=1):
        self.fields_map = {}
        self.db_map = {}
        query = "SELECT d.id, d.name_ui, d.description, a.id, a.name_ui, a.type, a.description FROM annotation_field a LEFT JOIN annotation_database d ON a.database_id=d.id WHERE d.reference_id={0} ORDER BY d.name_ui, a.name_ui".format(reference)
        for row in db_session.execute(query):
            if row[0] not in self.db_map:
                self.db_map[row[0]] = {"name" : row[1], "description": row[2], "fields" : []}
            self.db_map[row[0]]["fields"].append({"id" : row[3], "name" : row[4], "type" : row[5]})
            self.fields_map[row[3]] = {"name" : row[4], "type" : row[5], "db_id" : row[0], "db_name" : row[1], "description": row[6]}

    # build the sql query according to the annso filtering parameter and return result as json data
    def get_databases(self):
        return self.db_map

    def get_fields(self):
        return self.fields_map





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Analysis MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnalysisManager:
    def __init__(self):
        pass



    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """
            Generic method to get analysis metadata according to provided filtering options.
        """
        global db_session
        if fields is None:
            fields = Analysis.public_fields
        if query is None:
            query = {}
        if order is None:
            order = ['-create_date', "name"]
        if offset is None:
            offset = 0
        if limit is None:
            limit = offset + RANGE_MAX
        return db_session.query(Analysis).filter_by(**query).offset(offset).limit(limit).all()



    def create(self, name, template_id=None):
        """
            Create a new analysis in the database.
        """
        global db_session
        instance = None
        db_session.begin(nested=True)
        try:
            instance = Analysis(name=name, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now(), setting='{"fields" : [2,3,4,5,6,8,9], "filter":["AND", []]}')
            db_session.add(instance)
            db_session.commit() # commit the save point into the session (opened by the .begin() before the try:)
            db_session.commit() # commit into the database.
            return instance.to_json(), True
        except IntegrityError as e:
            db_session.rollback()
        return None, False
        


    def load(self, analysis_id):
        """
            Load all data about the analysis with the provided id and return result as JSON object.
        """
        analysis = db_session.execute("SELECT a.id, a.name, a.update_date, a.creation_date, a.setting, t.name AS t_name, t.id AS t_id FROM analysis a LEFT JOIN template t ON a.template_id = t.id WHERE a.id = {0}".format(analysis_id)).first()
        result = {
            "id" : analysis.id, 
            "name" : analysis.name, 
            "update_date" : analysis.update_date.ctime(),
            "creation_date" : analysis.creation_date.ctime(),
            "template_id" : analysis.t_id,
            "template_name" : analysis.t_name,
            "samples" : [],
            "attributes" : [],
            "filters" : {}}
        if analysis.setting is not None and analysis.setting.strip() is not "":
            result["setting"] = json.loads(analysis.setting)
        else:
            result["setting"] = '{"fields" : [2,3,4,5,6,8,9], "filter":["AND", []]}'

        # Get predefined filters set for this analysis
        query = "SELECT * FROM filter WHERE analysis_id = {0} ORDER BY name ASC;"
        for f in db_engine.execute(query.format(analysis_id)):
            result["filters"][f.id] = { "name" : f.name, "description" : f.description, "filter": json.loads(f.filter)}


        # Get attributes used for this analysis
        query = "SELECT a.sample_id, a.name, a.value \
            FROM attribute a \
            WHERE a.analysis_id = {0}\
            ORDER BY a.name ASC, a.sample_id ASC"

        current_attribute = None;
        for r in db_engine.execute(query.format(analysis_id)):
            if current_attribute == None or current_attribute != r.name:
                current_attribute = r.name
                result["attributes"].append({ "name" : r.name, "samples_value" : {r.sample_id : r.value} })
            else:
                result["attributes"][-1]["samples_value"][r.sample_id] = r.value

        # Get Samples used for this analysis
        query = "SELECT s.id, s.name, s.comments, s.is_mosaic, asp.nickname, f.id as f_id, f.filename, f.import_date \
            FROM analysis_sample asp \
            LEFT JOIN sample s ON asp.sample_id = s.id \
            LEFT JOIN sample_file sf ON s.id = sf.sample_id \
            LEFT JOIN file f ON f.id = sf.file_id \
            WHERE asp.analysis_id = {0}"
        for r in db_engine.execute(query.format(analysis_id)):
            result["samples"].append({ 
                "id" : r.id, 
                "name" : r.name, 
                "comments" : r.comments, 
                "is_mosaic" : r.is_mosaic, 
                "nickname" : r.nickname, 
                "file_id" : r.f_id, 
                "filename" : r.filename,
                "import_date" : r.import_date,
                "attributes" : {}})
            for a in result["attributes"]:
                if r.id in a["samples_value"].keys():
                    result["samples"][-1]["attributes"][a['name']] = a["samples_value"][r.id]
                else :
                    result["samples"][-1]["attributes"][a['name']] = ""

        return result




    def update(self, analysis_id, data):
        """ 
            Update analysis with provided data. Data that are not provided are not updated (ignored).
        """
        update_query = ""
        # BASICS SETTINGS (current filter and displayed fields)
        if "fields" in data.keys() or "filter" in data.keys() or "selection" in data.keys():
            #retrieved current settings from database
            setting = {}
            try : 
                setting = json.loads(db_engine.execute("SELECT setting FROM analysis WHERE id={}".format(analysis_id)).first().setting)
            except : 
                # TODO : log error
                setting = {}
            if "fields" in data.keys():
                setting["fields"] = data["fields"]
            if "filter" in data.keys():
                setting["filter"] = data["filter"]
            if "selection" in data.keys():
                setting["selection"] = data["selection"]
            # update database
            main_query = "setting='{0}', ".format(json.dumps(setting))

        # saved filters
        if "filters" in data.keys():
            # delete old filters
            db_engine.execute("DELETE FROM filter WHERE analysis_id={}".format(analysis_id))
            # create new associations
            query    = "INSERT INTO filter (analysis_id, name, filter) VALUES "
            subquery = "({0}, '{1}', '{2}'')"
            query = query + ', '.join([subquery.format(analysis_id, f['name'], f['filter']) for f in data["filters"]])
            db_engine.execute(query)

        # samples + nickname
        if "samples" in data.keys():
            # create new associations
            pattern = "({0}, {1}, {2})"
            query   = ', '.join([pattern.format(analysis_id, s['id'], "'{0}'".format(s['nickname']) if 'nickname' in s.keys() else 'NULL') for s in data["samples"]])
            # check if query seems good then apply change
            if query != "":
                # delete old analysis sample associations
                db_engine.execute("DELETE FROM analysis_sample WHERE analysis_id={}".format(analysis_id))
                db_engine.execute("INSERT INTO analysis_sample (analysis_id, sample_id, nickname) VALUES " + query)
            else:
                # TODO : log error
                pass

        # attributes + values
        if "attributes" in data.keys():
            # create new attributes
            pattern = "({0}, {1}, '{2}', '{3}')"
            data['attributes'] = [a for a in data['attributes'] if a['name'] != ""]
            query   = ', '.join([pattern.format(analysis_id, sid, att['name'], att['samples_value'][sid]) for att in data['attributes'] for sid in att['samples_value']])
            # check if query seems good then apply change
            if query != "":
                db_engine.execute("DELETE FROM attribute WHERE analysis_id={}".format(analysis_id))
                db_engine.execute("INSERT INTO attribute (analysis_id, sample_id, name, value) VALUES " + query)
            else:
                # TODO : log error
                pass

        # analysis name, ...
        if "name" in data.keys():
            main_query += "name='{0}', ".format(data["name"])

        # update analysis
        db_engine.execute("UPDATE analysis SET {0}update_date=CURRENT_TIMESTAMP WHERE id={1}".format(main_query, analysis_id))



    def save_filter(self, analysis_id, name, filter_json):
        """
            Save (add) a new filter for the analysis with the provided id.
        """
        global db_session
        instance = None
        db_session.begin(nested=True)
        try:
            instance = Filter(analysis_id=analysis_id, name=name, filter=json.dumps(filter_json))
            db_session.add(instance)
            db_session.commit() # commit the save point into the session (opened by the .begin() before the try:)
            db_session.commit() # commit into the database.
            return instance.to_json(), True
        except IntegrityError as e:
            db_session.rollback()
        return None, False


    def update_filter(self, filter_id, name, filter_json):
        query    = "UPDATE filter SET name='{1}', filter='{2}' WHERE id={0}".format(filter_id, name, json.dumps(filter_json))
        db_engine.execute(query)


    def delete_filter(self, filter_id):
        db_engine.execute("DELETE FROM filter WHERE id={}".format(filter_id))







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Variant MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VariantManager:


    def total(self):
        return 350



    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """
            Generic method to get files metadata according to provided filtering options
        """
        global db_session
        if fields is None:
            fields = Sample.public_fields
        if query is None:
            query = {}
        if order is None:
            order = ['-create_date', "name"]
        if offset is None:
            offset = 0
        if limit is None:
            limit = offset + RANGE_MAX

        result = []
        for r in db_engine.execute("SELECT s.name, sv.* FROM sample_variant_hg19 sv INNER JOIN sample s ON s.id = sv.sample_id"):
            result.append((r[1], r[0], r[3], r[4], r[5], r[6]))

        return result










# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Samples MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SampleManager:
    def __init__(self):
        pass


    def total(self):
        return 3


    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """
            Generic method to get files metadata according to provided filtering options
        """
        global db_session
        if fields is None:
            fields = Sample.public_fields
        if query is None:
            query = {}
        if order is None:
            order = ['-create_date', "name"]
        if offset is None:
            offset = 0
        if limit is None:
            limit = offset + RANGE_MAX


        result = []
        for s in db_session.execute("SELECT sp.id, sp.name, sp.comments  FROM sample sp"):
            result.append({"id" : s[0], "name" : s[1], "comments": s[2], "analyses" : []})
        return result













# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# FILTER ENGINE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class FilterEngine:
    op_map = {'AND' : ' AND ', 'OR': ' OR ', '==' : '=', '!=': '<>', '>':'>', '<':'<', '>=':'>=', '<=':'<=', 
        # As a left join will be done on the chr+pos or chr+pos+ref+alt according to the type of the set operation (by site or by variant)
        # We just need to test if one of the "joined" field is set or not
        'IN'       : '{0}.chr is not null', 
        'NOTIN'    : '{0}.chr is null'}

    def __init__(self, reference=1):
        """
            Init Annso Filtering engine. (reference=1 mean "hg19", see database import script)
            Init mapping collection for annotations databases and fields
        """
        refname = db_session.execute("SELECT table_suffix FROM reference WHERE id="+str(reference)).first()["table_suffix"]

        self.reference = reference
        self.fields_map = {}
        self.db_map = {}
        self.variant_table = "sample_variant_{0}".format(refname)
        query = "SELECT d.id, d.name, d.jointure, a.id, a.name, a.type FROM annotation_field a LEFT JOIN annotation_database d ON a.database_id=d.id WHERE d.reference_id=" + str(reference)
        for row in db_session.execute(query):
            if row[0] not in self.db_map:
                self.db_map[row[0]] = {"name" : row[1], "join": row[2].format(self.variant_table), "fields" : {}}
            self.db_map[row[0]]["fields"][row[3]] = {"name" : row[4], "type" : row[5]}
            self.fields_map[row[3]] = {"name" : row[4], "type" : row[5], "db_id" : row[0], "db_name" : row[1], "join": row[2].format(self.variant_table)}





    def request(self, analysis_id, mode, filter_json, fields=None, limit=100, offset=0):
        """
            Build the sql query according to the annso filtering parameter and return result as json data
        """
        # Check parameter
        if type(analysis_id) != int or analysis_id <=0 : analysis_id = None
        if mode not in ["table", "list"]: mode = "table"

        # Get sample ids used for the analysis
        sample_ids = []
        if analysis_id is not None : 
            # Retrieve sample ids for the analysis 
            for row in db_session.execute("select sample_id from analysis_sample where analysis_id = {0}".format(analysis_id)):
                sample_ids.append(str(row.sample_id))

        # Build SELECT
        q_select = ["{0}.{1}".format(self.fields_map[f_id]["db_name"], self.fields_map[f_id]["name"]) for f_id in fields]

        # Build FROM/JOIN
        tables_to_import = [1] # 1 is for the sample_variant_{ref} table. We always need this table as it's used for the join with other tables
        for f_id in fields:
            if self.fields_map[f_id]["db_id"] not in tables_to_import :
                tables_to_import.append(self.fields_map[f_id]["db_id"])

        # Build WHERE 
        temporary_to_import = {}

        def build_filter(data):
            """ Recursive method that build the query from the filter json data at operator level """
            operator = data[0]
            if operator in ['AND', 'OR']:
                if len(data[1]) == 0 :
                    return ''
                return ' (' + FilterEngine.op_map[operator].join([build_filter(f) for f in data[1]]) + ') '

            elif operator in ['==', '!=', '>', '<', '>=', '<=']:
                if data[1][0] == 'field' :
                    t = self.fields_map[data[1][1]]["type"]
                elif (data[2][0] == 'field') :
                    t = self.fields_map[data[2][1]]["type"]
                else:
                    t = 'string'
                return '{0}{1}{2}'.format(parse_value(t, data[1]), FilterEngine.op_map[operator], parse_value(t, data[2]))

            elif operator in ['IN', 'NOTIN']:
                tmp_table = get_tmp_table(data[1], data[2])
                temporary_to_import[tmp_table]['where'] = FilterEngine.op_map[operator].format(tmp_table, self.fields_map[1]["db_name"])
                if data[1] == 'site' :
                    temporary_to_import[tmp_table]['from']  = " LEFT JOIN {1} ON {0}.chr={1}.chr AND {0}.pos={1}.pos".format(self.fields_map[1]["db_name"], tmp_table)
                else: #if data[1] == 'variant' :
                    temporary_to_import[tmp_table]['from']  = " LEFT JOIN {1} ON {0}.chr={1}.chr AND {0}.pos={1}.pos AND {0}.ref={1}.ref AND {0}.alt={1}.alt".format(self.fields_map[1]["db_name"], tmp_table)
                return temporary_to_import[tmp_table]['where']


        def get_tmp_table(mode, data):
            """ 
                Parse json data to build temp table for ensemblist operation IN/NOTIN 
                    mode : site or variant
                    data : json data about the temp table to create
            """
            ttable_quer_map = "CREATE TEMP TABLE IF NOT EXISTS {0} WITH (OIDS) ON COMMIT DROP AS {1}; "

            if data[0] == 'sample' :
                tmp_table_name    = "tmp_sample_{0}_{1}".format(data[1], mode)
                if mode == 'site':
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.chr, {0}.pos FROM {0} WHERE {0}.sample_id={1}".format(self.variant_table, data[1]))
                else : # if mode = 'variant' :
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.chr, {0}.pos, {0}.ref, {0}.alt FROM {0} WHERE {0}.sample_id={1}".format(self.variant_table, data[1]))

            elif (data[0] == 'filter') :
                tmp_table_name  = "tmp_filter_{0}".format(data[1])
                tmp_table_query = ttable_quer_map.format(tmp_table_name, "#Retrieve query in database" ) 
                
            elif (data[0] == 'attribute') :
                key, value = data[1].split(':')
                tmp_table_name    = "tmp_attribute_{0}_{1}_{2}_{3}".format(analysis_id, key, value, mode)
                if mode == 'site':
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.chr, {0}.pos FROM {0} INNER JOIN {1} ON {0}.sample_id={1}.sample_id AND {1}.analysis_id={2} AND {1}.name='{3}' AND {1}.value='{4}'".format(self.variant_table, 'attribute', analysis_id, key, value))
                else : # if mode = 'variant' :
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.chr, {0}.pos, {0}.ref, {0}.alt FROM {0} INNER JOIN {1} ON {0}.sample_id={1}.sample_id AND {1}.analysis_id={2} AND {1}.name='{3}' AND {1}.value='{4}'".format(self.variant_table, 'attribute', analysis_id, key, value))

            temporary_to_import[tmp_table_name] = {'query' : tmp_table_query}
            return tmp_table_name


        def parse_value(ftype, data):
            if data[0] == 'field':
                if self.fields_map[data[1]]["db_id"] not in tables_to_import :
                    tables_to_import.append(self.fields_map[data[1]]["db_id"])

                if self.fields_map[data[1]]["type"] == ftype :
                    return "{0}.{1}".format(self.fields_map[data[1]]["db_name"], self.fields_map[data[1]]["name"])

            if data[0] == 'value':
                if ftype in ['int', 'float']:
                    return str(data[1])
                elif ftype == 'string':
                    return "'{0}'".format(data[1])
                elif ftype == 'range' and len(data) == 3:
                    return 'int8range({0}, {1})'.format(data[1], data[2])
            raise AnnsoException("FilterEngine.request : Impossible to compare arguments without same type : {0} ({1}) and {2} ({3})")


        q_where = ""
        if len(sample_ids) == 1 :
            q_where = "{0}.sample_id={1}".format(self.variant_table, sample_ids[0])
        elif len(sample_ids) > 1:
            q_where = "{0}.sample_id IN ({1})".format(self.variant_table, ','.join(sample_ids))

        q_where2 = build_filter(filter_json)
        if  len(q_where2.strip()) > 0:
            q_where += " AND " + q_where2

        
        # Build FROM/JOIN according to the list of used annotations databases
        q_from  = " LEFT JOIN ".join([self.db_map[d_id]["join"] for d_id in tables_to_import])
        q_from += " " + " ".join([t['from'] for t in temporary_to_import.values()])
        

        # build query
        query = "".join([t['query'] for t in temporary_to_import.values()])
        query += "SELECT {0} FROM {1} WHERE {2} LIMIT {3} OFFSET {4};".format(', '.join(q_select), q_from, q_where, limit, offset)


        # Save filter in analysis setting
        if (analysis_id > 0):
            setting = {}
            try : 
                setting = json.loads(db_engine.execute("SELECT setting FROM analysis WHERE id={}".format(analysis_id)).first().setting)
                setting["filter"] = filter_json
                db_engine.execute("UPDATE analysis SET {0}update_date=CURRENT_TIMESTAMP WHERE id={1}".format("setting='{0}', ".format(json.dumps(setting)), analysis_id))
            except : 
                # TODO : log error
                print ("Not able to save current filter")        


        # Execute query and get result
        print (query)
        result = []
        for s in db_session.execute(query): 
            variant = {}
            i=0
            for f_id in fields:
                variant[f_id]= FilterEngine.parse_result(s[i])
                i += 1
            result.append(variant)
        return result



    @staticmethod
    def parse_result(value):
        if value is None:
            return ""
        if type(value) == psycopg2._range.NumericRange:
            return (value.lower, value.upper)
        return value












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# INIT OBJECTS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




annso = Core()