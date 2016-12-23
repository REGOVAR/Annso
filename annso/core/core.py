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
    def __init__(self):
        pass

    # build the sql query according to the annso filtering parameter and return result as json data
    def get(self):
        query = "SELECT d.id, d.name_ui, d.description, a.id, a.name_ui, a.type, a.description FROM annotation_field a LEFT JOIN annotation_database d ON a.database_id=d.id ORDER BY d.name_ui, a.name_ui"

        result = {}
        for r in db_session.execute(query):
            if r[0] not in result:
                result[r[0]] = {"name" : r[1], "description" : r[2], "fields" : []}
            result[r[0]]["fields"].append({"id" : r[3], "name" : r[4], "type" : r[5], "description" : r[6]})
        return result





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
            raise PirusException("Unable to retrieve the pirus file with the provided id : " + file_id)
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
    def __init__(self):
        pass

    # build the sql query according to the annso filtering parameter and return result as json data
    def request(self, analysis_id, mode, filter_json, fields=None, limit=100, offset=0):
        # Check parameter
        if mode not in ["table", "list"]: mode = "table"

        # Get sample ids used for the analysis
        # TODO : retrieve sample ids with query : "select sample_id from analysis_sample where analysis_id = {0}"
        sample_ids = [1]
        reference = "hg19"
        variant_table = "sample_variant_{0}".format(reference)

        # Get fields to select
        if fields is None  or len(fields) == 0: fields = [0]
        query = "select d.id, d.name, d.jointure, f.id, f.name FROM annotation_field f LEFT JOIN annotation_database d ON d.id = f.database_id WHERE f.id IN ({0})".format(','.join([str(f) for f in fields]))
        fields = {}
        for r in db_session.execute(query):
            if r[0] not in fields:
                fields[r[0]] = {"join" : r[2], "fields" : [], "name": r[1]}
            fields[r[0]]["fields"].append({"id" : r[3], "name" : r[4]})

        # Get filter conditions
        # TODO


        for db in fields:
            fields[db]["join"] = fields[db]["join"].format(reference, variant_table) # TODO FIXME : remove reference in formart() + update sql scripts


        # Build SELECT
        select_fields = [fields[f]["name"] + "." + fn["name"] for f in fields for fn in fields[f]["fields"]]


        # Build FROM/JOIN
        from_table = [variant_table]
        join = " LEFT JOIN "
        from_table.extend([join + fields[db]["join"] for db in fields if fields[db]["name"] != variant_table])


        # Build WHERE
        where = variant_table + ".sample_id=1"
        # TODO add filter conditions

        # build query
        query = "SELECT {0} FROM {1} WHERE {2} LIMIT {3} OFFSET {4}".format(', '.join(select_fields), ' '.join(from_table), where, limit, offset)

        # Execute query and get result
        result = []
        for s in db_session.execute(query): 
            varariant = {}
            i=0
            for db_id in fields:
                for f in fields[db_id]['fields']:
                    varariant[f["id"]]= FilterEngine.parse_result(s[i])
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