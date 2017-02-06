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
import hashlib


from core.framework import *
from core.model import *









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# CORE OBJECT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Core:
    def __init__(self):
        self.annotation_db = AnnotationDatabaseManager()
        self.analysis = AnalysisManager()
        self.sample = SampleManager()
        self.filter = FilterEngine()
        self.file = FileManager()
        
        self.export_modules = {}
        self.import_modules = {}
        self.report_modules = {}

        # Load metada for activated modules
        for name in EXPORTS_MODULES:
            try:
                m = __import__('exports.{0}'.format(name))
                self.export_modules[name] = {
                    "info" : eval ('m.{0}.metadata'.format(name)),
                    "do"   : eval ('m.{0}.export_data'.format(name)),
                }
                self.export_modules[name].update({'id' : name})
            except:
                err("Unable to load exports.{0} module".format(name))
        for name in IMPORTS_MODULES:
            try:
                m = __import__('imports.{0}'.format(name))
                self.import_modules[name] = {
                    "info" : eval ('m.{0}.metadata'.format(name)),
                    "do"   : eval ('m.{0}.import_data'.format(name)),
                }
                self.import_modules[name].update({'id' : name})
            except:
                err("Unable to load imports.{0} module".format(name))
        for name in REPORTS_MODULES:
            try:
                m = __import__('reports.{0}.report'.format(name))
                self.report_modules[name] = {
                    "info" : eval ('m.{0}.report.metadata'.format(name)),
                    "do"   : eval ('m.{0}.report.report_data'.format(name)),
                }
                self.report_modules[name].update({'id' : name})
            except Exception as error:
                ipdb.set_trace()
                err("Unable to load reports.{0} module".format(name))



    def init(self):
        """
            Do some verifications on the server to check that all is good.
             - check that config parameters are consistency
             - check that 
        """
        pass


    
    @staticmethod
    def notify_all(data):
        msg = json.dumps(data)
        log ("Core Notify All : {0}".format(msg))

 


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
        return sample_file



    def upload_finish(self, file_id, checksum=None, checksum_type="md5"):
        """ 
            When upload of a file is finish, we move it from the download temporary folder to the
            files folder. A checksum validation can also be done if provided. 
            Update finaly the status of the file to UPLOADED or CHECKED -> file ready to be used
        """
        # Retrieve file
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

        # Importing to the database according to the type (if an import module can manage it)
        for m in annso.import_modules.values():
            if file.type in m['info']['input']:
                log('Start import of the file (id={0}) with the module {1} ({2})'.format(file_id, m['info']['name'], m['info']['description']))
                m['do'](file.id, file.path, annso)
                break;

        # Notify all about the new status
        # msg = {"action":"file_changed", "data" : [pfile.to_json_data()] }
        # annso.notify_all(json.dumps(msg))
        # TODO : check if run was waiting the end of the upload to start


    def delete(self, file_id):
        db_engine.execute("DELETE FROM variant")



 


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANNOTATION DATABASE MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnnotationDatabaseManager:
    def __init__(self, reference=1):
        self.fields_map = {}
        self.db_map = {}
        query = "SELECT d.id AS did, d.name_ui AS dname, d.description AS ddesc, a.id, a.name_ui, a.type, a.description, a.meta FROM annotation_field a \
                 LEFT JOIN annotation_database d ON a.database_id=d.id \
                 WHERE d.reference_id={0}".format(reference)
        for row in db_session.execute(query):
            if row.did not in self.db_map:
                self.db_map[row.did] = {"name" : row.dname, "description": row.ddesc, "fields" : []}
            meta = None
            if row.meta is not None:
                meta = json.loads(row.meta)
            self.db_map[row.did]["fields"].append({"id" : row.id, "name" : row.name_ui, "type" : row.type, "description": row.description, "meta": meta})
            self.fields_map[row.id] = {"name" : row.name_ui, "type" : row.type, "db_id" : row.did, "db_name" : row.dname, "description": row.ddesc, "meta": meta}

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
            instance = Analysis(name=name, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now(), settings='{"fields" : [1,3,4,5,6,7,8], "filter":["AND", []]}')
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
        analysis = db_session.execute("SELECT a.id, a.name, a.update_date, a.creation_date, a.settings, t.name AS t_name, t.id AS t_id FROM analysis a LEFT JOIN template t ON a.template_id = t.id WHERE a.id = {0}".format(analysis_id)).first()
        result = {
            "id" : analysis.id, 
            "name" : analysis.name, 
            "update_date" : analysis.update_date.ctime() if analysis.update_date is not None else datetime.datetime.now().ctime(),
            "creation_date" : analysis.creation_date.ctime() if analysis.creation_date is not None else datetime.datetime.now().ctime(),
            "template_id" : analysis.t_id,
            "template_name" : analysis.t_name,
            "samples" : [],
            "attributes" : [],
            "filters" : {}}
        if analysis.settings is not None and analysis.settings.strip() is not "":
            result["settings"] = json.loads(analysis.settings)
        else:
            result["settings"] = '{"fields" : [1,3,4,5,6,7,8], "filter":["AND", []]}'

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
                "import_date" : r.import_date.ctime() if r.import_date is not None else datetime.datetime.now().ctime(),
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
            settings = {}
            try : 
                settings = json.loads(db_engine.execute("SELECT settings FROM analysis WHERE id={}".format(analysis_id)).first().settings)
            except : 
                # TODO : log error
                settings = {}
            if "fields" in data.keys():
                settings["fields"] = data["fields"]
            if "filter" in data.keys():
                settings["filter"] = data["filter"]
            if "selection" in data.keys():
                settings["selection"] = data["selection"]
            # update database
            main_query = "settings='{0}', ".format(json.dumps(settings))

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



    def report(self, analysis_id, report_id, report_data):
        # Working cache folder for the report generator
        cache = os.path.join(CACHE_DIR, 'reports/', report_id)
        if not os.path.isdir(cache):
            os.makedirs(cache)

        # Output path where the report shall be stored
        output_path = os.path.join(CACHE_DIR, 'reports/{}-{}-{:%Y%m%d.%H%M%S}.{}'.format(analysis_id, report_id, datetime.datetime.now(), report_data['output']))

        try:
            module = annso.report_modules[report_id]
            result = module['do'](analysis_id, report_data, cache, output_path, annso)
        except Exception as  error:
            # TODO : log error
            err ("Error occured : {0}".format(error))

        # Store report in database
        # Todo

        return output_path



    # def get_report(self, variants_ids, report_template=None, report_lang=None, report_option=None):
    #     # Importing to the database according to the type (if an import module can manage it)
    #     for m in annso.report_modules.values():
    #         if file.type in m['info']['input']:
    #             log('Start import of the file (id={0}) with the module {1} ({2})'.format(file_id, m['info']['name'], m['info']['description']))
    #             m['do'](file.id, file.path, annso)
    #             break;


    #     # Retrieve gene from variant ids list
    #     return Gene("GJB2", [])
    #     result = []
    #     sql =  "SELECT v.chr, v.pos, v.ref, v.alt, array_agg(rg.name) "
    #     sql += "FROM variant_hg19 v "
    #     sql += "INNER JOIN refgene_hg19 rg ON v.chr = rg.chrom AND rg.txrange @> int8(v.pos) "
    #     sql += "WHERE v.id IN (" + ','.join(variants_ids) + ") GROUP BY v.id"
    #     for r in db_engine.execute():
    #         result.append((r[1], r[0], r[3], r[4], r[5], r[6]))



    #     return Gene("GJB2", [])


    def export(self, analysis_id, export_id, report_data):
        return "<h1>Your export!</h1>"












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Samples MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SampleManager:
    def __init__(self):
        pass


    def total(self):
        return db_session.execute("SELECT count(*) FROM sample").first()[0]


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
            Drop all temporary table as are no more mapped 
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





    def request(self, analysis_id, mode, filter_json, fields=None, limit=100, offset=0, count=False):
        # Generate the temp hash name corresponding to the query
        hashname = FilterEngine.get_hasname(analysis_id, mode, fields, filter_json)
        query = ""
        sql_result = None

        

        # Do select query on the tmp table and update "last query time"
        query = self.build_query(analysis_id, mode, filter_json, fields, limit, offset, count)
        with Timer() as t:
            sql_result = db_engine.execute(query)
        log ("---\nFields :\n{0}\nFilter :\n{1}\nQuery :\n{2}\nRequest query : {3}".format(fields, filter_json, query, t))
        
        

        # Save filter in analysis settings
        if not count and (analysis_id > 0):
            settings = {}
            try : 
                settings = json.loads(db_engine.execute("SELECT settings FROM analysis WHERE id={}".format(analysis_id)).first().settings)
                settings["filter"] = filter_json
                db_engine.execute("UPDATE analysis SET {0}update_date=CURRENT_TIMESTAMP WHERE id={1}".format("settings='{0}', ".format(json.dumps(settings)), analysis_id))
            except : 
                # TODO : log error
                err ("Not able to save current filter")        



        # Get result
        if count:
            result = sql_result.first()[0]
        else:
            result = []
            with Timer() as t:
                if sql_result is not None:
                    for s in sql_result: 
                        variant = {'id' : s.variant_id}
                        i=1
                        for f_id in fields:
                            variant[f_id]= FilterEngine.parse_result(s[i])
                            i += 1
                        result.append(variant)
            log ("Result processing : {0}\nTotal result : {1}".format(t, "-"))
        return result










    def build_query(self, analysis_id, mode, filter_json, fields=None, limit=100, offset=0, count=False):
        """
            Build the sql query according to the annso filtering parameter and return the query and the name of the associated temps table
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
        q_select = 'variant_id, ' + ', '.join(["{0}.{1}".format(self.fields_map[f_id]["db_name"], self.fields_map[f_id]["name"]) for f_id in fields])


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
            ttable_quer_map = "CREATE TEMP TABLE IF NOT EXISTS {0} WITHOUT OIDS ON COMMIT DROP AS {1}; "

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
        

        # build final query
        query_tpm = "".join([t['query'] for t in temporary_to_import.values()])
        if count:
            query_req = "SELECT DISTINCT {0} FROM {1} WHERE {2}".format(q_select, q_from, q_where)
            return '{0} SELECT COUNT(*) FROM ({1}) AS sub;'.format(query_tpm, query_req)
        else: 
            query_req = "SELECT DISTINCT {0} FROM {1} WHERE {2} LIMIT {3} OFFSET {4};".format(q_select, q_from, q_where, limit, offset)
            return query_tpm + query_req







    @staticmethod
    def get_hasname(analysis_id, mode, fields, filter_json):
        # clean and sort fields list
        clean_fields = fields
        clean_fields.sort()
        clean_fields = list(set(clean_fields))

        string_id = "{0}{1}{2}{3}".format(analysis_id, mode, clean_fields, json.dumps(filter_json))
        return hashlib.md5(string_id.encode()).hexdigest()


    @staticmethod
    def parse_result(value):
        """
            Parse value returned by sqlAlchemy and cast it, if needed, into "simples" python types
        """
        if value is None:
            return ""
        if type(value) == psycopg2._range.NumericRange:
            return (value.lower, value.upper)
        return value











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# INIT OBJECTS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




annso = Core()
log('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')