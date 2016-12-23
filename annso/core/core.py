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









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# CORE OBJECT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Core:
    def __init__(self):
        self.annotation_db = AnnotationDatabaseManager()
        self.analysis = AnalysisManager()
        self.template = TemplateManager()
        self.sample = SampleManager()
        self.variant = VariantManager()
        self.filter = FilterEngine()
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



    def public_fields(self):
        return Analysis.public_fields




    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """
            Generic method to get analysis metadata according to provided filtering options
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
        global db_session
        instance = None
        db_session.begin(nested=True)
        try:
            instance = Analysis(name=name, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now())
            db_session.add(instance)
            db_session.commit() # commit the save point into the session (opened by the .begin() before the try:)
            db_session.commit() # commit into the database.
            return instance.export_client(), True
        except IntegrityError as e:
            db_session.rollback()
        return None, False
        

    def get_from_id(self, analysis_id):
        analysis = db_session.query(Analysis).filter_by(id=analysis_id).first()
        return analysis.export_client()


    def get_from_ids(self, file_ids, sublvl=0, fields=None):
        pass


    def get_setting(self, analysis_id):
        analysis = db_session.query(Analysis).filter_by(id=analysis_id).first()
        return analysis.setting







class TemplateManager:
    def __init__(self):
        pass



    def public_fields(self):
        return Template.public_fields




    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """
            Generic method to get analysis metadata according to provided filtering options
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
        return db_session.query(Template).filter_by(**query).offset(offset).limit(limit).all()



    def get_from_id(self, file_id, sublvl=0, fields=None):
        pass
        
    

    def get_from_ids(self, file_ids, sublvl=0, fields=None):
        pass







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Variant MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VariantManager:
    def __init__(self):
        pass



    def public_fields(self):
        return Sample.public_fields



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


    def get_from_id(self, file_id, sublvl=0, fields=None):
        pass
        
    

    def get_from_ids(self, file_ids, sublvl=0, fields=None):
        pass










# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Samples MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SampleManager:
    def __init__(self):
        pass



    def public_fields(self):
        return Sample.public_fields



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



    def get_from_id(self, sample_id, fields=None):
        global db_session
        sample = db_session.query(Sample).filter_by(id=sample_id).first()
        return sample.export_client()



    def upload_init(self, filename, file_size, metadata={}):
        """ 
            Create an entry for the file in the database and return the id of the file in annso
            This method shall be used to init a resumable upload of a file 
            (the file is not yet available, but we can manipulate its annso metadata)
        """
        sample_file = File.new_from_tus(filename, file_size)
        return sample_file.export_client(["id", "name", "upload_offset", "path", "size"])



    def upload_finish(self, file_id, checksum=None, checksum_type="md5"):
        """ 
            When upload of a file is finish, we move it from the download temporary folder to the
            files folder. A checksum validation can also be done if provided. 
            Update finaly the status of the file to UPLOADED or CHECKED -> file ready to be used
        """
        # Retrieve file
        pfile = PirusFile.from_id(file_id)
        if pfile == None:
            raise AnnsoException("Unable to retrieve the pirus file with the provided id : " + file_id)
        # Move file
        old_path = pfile.path
        new_path = os.path.join(FILES_DIR, str(uuid.uuid4()))
        os.rename(old_path, new_path)
        # If checksum provided, check that file is correct
        file_status = "UPLOADED"
        if checksum is not None:
            if checksum_type == "md5" and md5(fullpath) != checksum : 
                raise error
            file_status = "CHECKED"            
        # Update file data in database
        pfile.upload_offset = pfile.size
        pfile.status = file_status
        pfile.path = new_path
        pfile.save()
        # Notify all about the new status
        msg = {"action":"file_changed", "data" : [pfile.export_client_data()] }
        pirus.notify_all(json.dumps(msg))
        # TODO : check if run was waiting the end of the upload to start











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# FILTER ENGINE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class FilterEngine:
    op_map = {'AND' : ' AND ', 'OR': ' OR ', '==' : '=', '!=': '<>', '>':'>', '<':'<', '>=':'>=', '<=':'<='}

    def __init__(self, reference=1):
        """
            Init Annso Filtering engine. (reference=1 mean "hg19", see database import script)
            Init mapping collection for annotations databases and fields
        """
        refname = db_session.execute("SELECT table_suffix FROM reference WHERE id="+str(reference)).first()["table_suffix"]


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
        if analysis_id is None : 
            # No implicit constraint on sample. (filter on all variant in database)
            sample_ids = []
        else :
            # TODO : retrieve sample ids with query : "select sample_id from analysis_sample where analysis_id = {0}"
            sample_ids = [1]



        # Build SELECT
        q_select = ["{0}.{1}".format(self.fields_map[f_id]["db_name"], self.fields_map[f_id]["name"]) for f_id in fields]

        # Build FROM/JOIN
        tables_to_import = [1] # 1 is for the sample_variant_{ref} table. We always need this table as it's used for the join with other tables
        for f_id in fields:
            if self.fields_map[f_id]["db_id"] not in tables_to_import :
                tables_to_import.append(self.fields_map[f_id]["db_id"])

        # Build WHERE 
        def build_filter(data):
            operator = data[0]
            if operator in ['AND', 'OR']:
                return ' (' + FilterEngine.op_map[operator].join([build_filter(f) for f in data[1]]) + ') '

            elif operator in ['==', '!=', '>', '<', '>=', '<=']:
                if (data[1][0] == 'field') :
                    t = self.fields_map[data[1][1]]["type"]
                elif (data[2][0] == 'field') :
                    t = self.fields_map[data[2][1]]["type"]
                else:
                    t = 'string'
                return '{0}{1}{2}'.format(parse_value(t, data[1]), FilterEngine.op_map[operator], parse_value(t, data[2]))

                


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
            q_where = "{0}.sample_id={1} AND ".format(self.variant_table, sample_ids[0])
        elif len(sample_ids) > 1:
            q_where = "{0}.sample_id IN ({1}) AND ".format(self.variant_table, ','.join(sample_ids))

        q_where += build_filter(filter_json)


        
        # Build FROM/JOIN according to the list of used annotations databases
        q_from = " LEFT JOIN ".join([self.db_map[d_id]["join"] for d_id in tables_to_import])



        # build query
        query = "SELECT {0} FROM {1} WHERE {2} LIMIT {3} OFFSET {4}".format(', '.join(q_select), q_from, q_where, limit, offset)
        print (query)

        # Execute query and get result
        result = []
        for s in db_session.execute(query): 
            varariant = {}
            i=0
            for f_id in fields:
                varariant[f_id]= FilterEngine.parse_result(s[i])
                i += 1
            result.append(varariant)
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