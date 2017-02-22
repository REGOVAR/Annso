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
        self.variant = VariantManager()
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
                # Reload annotation's databases/fields metadata as some new annot db/fields may have been created during the import
                annso.annotation_db.load_annotation_metadata()
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
# Format of data
# ref_list   : contains the list of available genome referencial
#              { <ref_id> : <ref_name> }
# db_list    : contains the list of available annotation databases according to the referencial
#              { <ref_id> :  {
#                   'order' : [<db_name_ui>, ...],
#                   'db'    : { 
#                       <db_name_ui> : {
#                           'versions': { <version_name> : <db_uid>, ... }, 
#                           'desc': <db_description>
#              }}}
# db_map     : contains the data for all annotation databases
#              { <db_uid> : {
#                   'uid' : <db_uid>
#                   'fields' : 
#                   'name'
#                   'description'
#                   'order'
#                   ...
#               }}
# fields_map :
class AnnotationDatabaseManager:
    def __init__(self):
        self.load_annotation_metadata()



    def load_annotation_metadata(self):
        self.ref_list  = {}
        self.db_list = {}
        self.db_map = {}
        self.fields_map = {}

        query = "SELECT d.uid, d.reference_id, d.version, d.name_ui, d.description, d.url, r.name \
                 FROM annotation_database d INNER JOIN reference r ON r.id=d.reference_id \
                 ORDER BY r.name ASC, d.ord ASC, version DESC"
        for row in db_session.execute(query):
            self.ref_list.update({row.reference_id : row.name})
            if row.reference_id in self.db_list.keys():
                if row.name_ui in self.db_list[row.reference_id].keys():
                    self.db_list[row.reference_id][row.name_ui]["versions"][row.version] = row.uid
                else:
                    self.db_list[row.reference_id]['order'].append(row.name_ui)
                    self.db_list[row.reference_id]['db'][row.name_ui] = { "name" : row.name_ui, "description" : row.description, "versions" : { row.version : row.uid }}
            else:
                self.db_list[row.reference_id] = { 'order' : [row.name_ui], 'db' : { row.name_ui : { "name" : row.name_ui, "description" : row.description, "versions" : { row.version : row.uid }}}}



        query = "SELECT d.uid AS duid, d.reference_id AS ref, d.version, d.ord AS dord, d.name_ui AS dname, d.description AS ddesc, d.update_date AS ddate, a.uid AS fuid, a.name_ui AS name, a.ord AS ford, a.type AS type, a.description AS desc, a.meta AS meta \
                 FROM annotation_field a \
                 INNER JOIN annotation_database d ON a.database_uid=d.uid \
                 ORDER BY d.uid, a.ord"
        for row in db_session.execute(query):
            meta = None if row.meta is None else json.loads(row.meta)
            self.fields_map[row.fuid] = {"uid"   : row.fuid, "name"  : row.name, "description": row.desc, "type" : row.type, "meta": meta, "order" : row.ford, "dbuid" : row.duid}
            if row.duid in self.db_map.keys():
                self.db_map[row.duid]["fields"].append(row.fuid)
            else:
                self.db_map[row.duid] = {"uid"   : row.duid, "name"  : row.dname, "description": row.ddesc, "order" : row.dord, "update" : row.ddate, "fields" : [row.fuid], "version" : row.version, "ref" : row.ref }


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



    def create(self, name, ref_id, template_id=None):
        """
            Create a new analysis in the database.
        """
        global db_session
        instance = None
        db_session.begin(nested=True)
        try:
            if ref_id not in annso.annotation_db.ref_list.keys():
                ref_id = DEFAULT_REFERENCIAL_ID
            settings = {"fields" : [], "filter" : ['AND', []]}
            db_uid = annso.annotation_db.db_list[ref_id]['db']['Variant']['versions']['']
            for f in annso.annotation_db.db_map[db_uid]["fields"][1:]:
                settings["fields"].append(f)
            instance = Analysis(name=name, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now(), reference_id=ref_id, settings=json.dumps(settings))
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
            "reference_id" : 2, # TODO : reference_id shall be associated to the analysis and retrieved in the database
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



    def load_ped(self, analysis_id, file_path):
        # parse ped file
        if os.path.exists(file_path) :
            extension = os.path.splitext(file_path)[1][1:]
            parser = ped_parser.FamilyParser(open(file_path), "ped")
        else:
            # no ped file -_-
            return False
        # retrieve analysis samples
        samples = {}
        for row in db_engine.execute("SELECT a_s.sample_id, a_s.nickname, s.name FROM analysis_sample a_s INNER JOIN sample s ON a_s.sample_id=s.id WHERE analysis_id={0}".format(analysis_id)):
            samples[row.name] = row.sample_id
            if row.nickname is not '' and row.nickname is not None : samples[row.nickname] = row.sample_id
        # drop all old "ped" attributes to avoid conflict
        ped_attributes = ['FamilyId', 'SampleId', 'FatherId', 'MotherId', 'Sex', 'Phenotype']
        db_engine.execute("DELETE FROM attribute WHERE analysis_id={0} AND name IN ('{1}')".format(analysis_id, ''','''.join(ped_attributes)))
        # Insert new attribute's values according to the ped data
        sql = "INSERT INTO attribute (analysis_id, sample_id, name, value) VALUES "
        for sample in parser.individuals:
            if sample.individual_id in samples.keys():
                sql += "({}, {}, '{}', '{}'),".format(analysis_id, samples[sample.individual_id], 'FamilyId',  sample.family)
                sql += "({}, {}, '{}', '{}'),".format(analysis_id, samples[sample.individual_id], 'FatherId',  sample.father)
                sql += "({}, {}, '{}', '{}'),".format(analysis_id, samples[sample.individual_id], 'MotherId',  sample.mother)
                sql += "({}, {}, '{}', '{}'),".format(analysis_id, samples[sample.individual_id], 'Sex',       sample.sex)
                sql += "({}, {}, '{}', '{}'),".format(analysis_id, samples[sample.individual_id], 'Phenotype', sample.phenotype)
        db_engine.execute(sql[:-1])


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
# Samples MANAGER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VariantManager:
    def __init__(self):
        pass



    def get(self, reference_id, variant_id, analysis_id=None):
        """
            return all data available about a variant
        """
        ref_name = annso.annotation_db.ref_list[int(reference_id)]
        query = "SELECT * FROM (SELECT bin, chr, pos, ref, alt FROM variant_{} WHERE id={}) AS _var LEFT JOIN dbnfsp_variant ON _var.bin=dbnfsp_variant.bin_hg19 AND _var.chr=dbnfsp_variant.chr_hg19 AND _var.pos=dbnfsp_variant.pos_hg19 AND _var.ref=dbnfsp_variant.ref AND _var.alt=dbnfsp_variant.alt" 
        variant = db_engine.execute(query.format('hg19', variant_id)).first()
        chrm = {1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"11", 12:"12", 13:"13", 14:"14", 15:"15", 16:"16", 17:"17", 18:"18", 19:"19", 20:"20", 21:"21", 22:"22", 23:"X", 24:"Y", 25:"M"}[variant.chr]
        pos  = variant.pos + 1 # return result as 1-based coord
        ref  = variant.ref
        alt  = variant.alt
        gene = variant.genename
        result = {
            "id" : variant_id,
            "reference_id" : reference_id,
            "reference" : ref_name,
            "chr" : chrm,
            "pos" : pos,
            "ref" : ref,
            "alt" : alt,
            "annotations" : {

            },
            "online_tools_variant" : {
                "varsome"  : "https://varsome.com/variant/{0}/chr{1}-{2}-{3}".format(ref_name, chrm, pos, ref),
            },
            "stats": {

            }
        }
        if gene is not None and gene != "":
            result.update({"online_tools_gene" : {
                "genetest"    : "https://www.genetests.org/genes/?gene={0}".format(gene),
                "decipher"    : "https://decipher.sanger.ac.uk/search?q={0}".format(gene),
                "cosmic"      : "http://cancer.sanger.ac.uk/cosmic/gene/overview?ln={0}".format(gene),
                "nih_ghr"     : "https://ghr.nlm.nih.gov/gene/{0}".format(gene),
                "hgnc"        : "http://www.genenames.org/cgi-bin/gene_symbol_report?match={0}".format(gene),
                "genatlas"    : "http://genatlas.medecine.univ-paris5.fr/fiche.php?symbol={0}".format(gene),
                "genecards"   : "http://www.genecards.org/cgi-bin/carddisp.pl?gene={0}".format(gene),
                "gopubmed"    : "http://www.gopubmed.org/search?t=hgnc&q={0}".format(gene),
                "h_invdb"     : "http://biodb.jp/hfs.cgi?db1=HUGO&type=GENE_SYMBOL&db2=Locusview&id={0}".format(gene),
                "kegg_patway" : "http://www.kegg.jp/kegg-bin/search_pathway_text?map=map&keyword={0}&mode=1&viewImage=true".format(gene)
            }})
        if analysis_id != None:
            result.update({"analysis" : { 
                "id" : analysis_id
            }})


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
    sql_type_map = {'int' : 'integer', 'string' : 'text', 'float' : 'real', 'percent' : 'real', 'enum' : 'integer', 'range' : 'range8', 'bool' : 'boolean',
                    'list_i' : 'text', 'list_s' : 'text', 'list_f' : 'text', 'list_i' : 'text', 'list_pb' : 'text'}




    def __init__(self, reference=2):
        """
            Init Annso Filtering engine. (reference=2 mean "hg19", see database import script)
            Init mapping collection for annotations databases and fields
        """
        refname = db_session.execute("SELECT table_suffix FROM reference WHERE id="+str(reference)).first()["table_suffix"]
        self.reference = reference
        self.fields_map = {}
        self.db_map = {}
        self.variant_table = "sample_variant_{0}".format(refname)
        query = "SELECT d.uid AS duid, d.name AS dname, d.name_ui AS dname_ui, d.jointure, d.reference_id, a.uid AS fuid, a.name AS fname, a.type, a.wt_default FROM annotation_field a LEFT JOIN annotation_database d ON a.database_uid=d.uid"
        for row in db_session.execute(query):
            if row.duid not in self.db_map:
                self.db_map[row.duid] = {"name" : row.dname, "join": row.jointure, "fields" : {}, "reference_id" : row.reference_id}
            self.db_map[row.duid]["fields"][row.fuid] = {"name" : row.fname, "type" : row.type}
            self.fields_map[row.fuid] = {"name" : row.fname, "type" : row.type, "db_uid" : row.duid, "db_name_ui" : row.dname_ui, "db_name" : row.dname, "join": row.jointure, "wt_default" : row.wt_default}




    def create_working_table (self, analysis_id, sample_ids, field_uids, dbs_uids, filter_ids=[], attributes={}):
        """
            Create a working sql table for the analysis to improove speed of filtering/annotation.
            A Working table contains all variants used by the analysis, with all annotations used by filters or displayed
        """
        progress = { "msg" : "wt_processing", "start" : datetime.datetime.now().ctime(), "analysis_id" : analysis_id, "step" : 1 }
        annso.notify_all(progress)

        # Create schema
        w_table = 'wt_{}'.format(analysis_id)
        query  = "DROP TABLE IF EXISTS {0} CASCADE; CREATE TABLE {0} (\
            annotated boolean DEFAULT False, \
            sample_id integer, \
            variant_id bigint, \
            bin integer, \
            chr bigint, \
            pos integer, \
            ref text, \
            alt text,\
            genotype integer, \
            depth integer, \
            is_transition boolean, \
            sample_tlist integer[], \
            sample_tcount integer, \
            sample_alist integer[], \
            sample_acount integer);"
        db_engine.execute(query.format(w_table))
        
        # Insert variant without annotation first
        query = "INSERT INTO {0} (sample_id, variant_id, bin, chr, pos, ref, alt, genotype, depth, is_transition, sample_tlist, sample_tcount, sample_alist, sample_acount) \
            SELECT sample_variant_{1}.sample_id, sample_variant_{1}.variant_id, sample_variant_{1}.bin, sample_variant_{1}.chr, sample_variant_{1}.pos, sample_variant_{1}.ref, sample_variant_{1}.alt, \
            sample_variant_{1}.genotype, sample_variant_{1}.depth, variant_{1}.is_transition, \
            variant_{1}.sample_list, array_length(variant_{1}.sample_list,1), \
            array_intersect(variant_{1}.sample_list, array[{2}]), array_length(array_intersect(variant_{1}.sample_list, array[{2}]),1) \
            FROM sample_variant_{1} INNER JOIN variant_{1} ON sample_variant_{1}.variant_id=variant_{1}.id\
            WHERE sample_variant_{1}.sample_id IN ({2});"
        db_engine.execute(query.format(w_table, 'hg19', ','.join([str(i) for i in sample_ids])))

        # Create indexes
        query  = "CREATE INDEX {0}_idx_ann ON {0} USING btree (annotated);".format(w_table)
        query  = "CREATE INDEX {0}_idx_vid ON {0} USING btree (variant_id);".format(w_table)
        query += "CREATE INDEX {0}_idx_sid ON {0} USING btree (sample_id);".format(w_table)
        query += "CREATE INDEX {0}_idx_var ON {0} USING btree (bin, chr, pos);".format(w_table)
        query += "CREATE INDEX {0}_idx_gt ON {0}  USING btree (genotype);".format(w_table)
        query += "CREATE INDEX {0}_idx_dp ON {0}  USING btree (depth);".format(w_table)
        db_engine.execute(query)

        # Update count stat of the analysis
        query = "UPDATE analysis SET total_variants=(SELECT COUNT(*) FROM {}), status='ANNOTATING' WHERE id={}".format(w_table, analysis_id)
        db_engine.execute(query)

        # Update working table by computing annotation
        self.update_working_table(analysis_id, sample_ids, field_uids, dbs_uids, filter_ids, attributes)




    def update_working_table(self, analysis_id, sample_ids, field_uids, dbs_uids, filter_ids=[], attributes={}):
        """
            Update annotation of the working table of an analysis. The working table shall already exists
        """
        # Get list of fields to add in the wt
        analysis = Analysis.from_id(analysis_id)
        total = analysis.total_variants
        diff_fields = []
        diff_dbs = []
        progress = { "msg" : "wt_processing", "start" : datetime.datetime.now().ctime(), "analysis_id" : analysis_id, "step" : 2, "progress_total" : total, "progress_current" : 0 }
        annso.notify_all(progress)
        try:
            query = "SELECT column_name FROM information_schema.columns WHERE table_name='wt_{}'".format(analysis_id)
            current_fields = [row.column_name if row.column_name[0] != '_' else row.column_name[1:] for row in db_engine.execute(query)]
            for f_uid in field_uids:
                if f_uid not in current_fields and self.fields_map[f_uid]['db_name_ui'] != 'Variant' :
                    diff_fields.append('_{}'.format(f_uid))
                    if self.fields_map[f_uid]['db_uid'] not in diff_dbs:
                        diff_dbs.append(self.fields_map[f_uid]['db_uid'])
        except :
            # working table doesn't exist
            return false

        # Alter working table to add new fields
        pattern = "ALTER TABLE wt_{0} ADD COLUMN {1}{2} {3};"
        query = ""

        for f_uid in diff_fields:
            if f_uid[0] == '_':
                f_uid = f_uid[1:]
            query += pattern.format(analysis_id, '_', f_uid, self.sql_type_map[self.fields_map[f_uid]['type']])
        for a_name in attributes.keys():
            if 'attr_{}'.format(a_name.lower()) not in current_fields:
                query += pattern.format(analysis_id, 'attr_', a_name, 'character varying(255) COLLATE pg_catalog."C.UTF-8"')
        for f_id in filter_ids:
            if 'filter_{}'.format(f_id) not in current_fields:
                query += pattern.format(analysis_id, 'filter_', f_id, 'boolean')
        if query != "" :
            # Add new annotation columns to the working table
            db_engine.execute(query)
            # Mark all variant as not annotated (to be able to do a resumable update)
            db_engine.execute("UPDATE wt_{} SET annotated=False".format(analysis_id))
        progress.update({"step" : 3 })
        annso.notify_all(progress)


        # Create update query to retrieve annotation
        qset_ann = ', '.join(['{0}=_ann.{0}'.format(f_uid) for f_uid in diff_fields])
        qslt_ann = ','.join(['{0}.{1} AS {2}'.format(self.fields_map[f_uid[1:]]['db_name'], self.fields_map[f_uid[1:]]['name'], f_uid) for f_uid in diff_fields])
        qslt_var = 'SELECT variant_id, bin, chr, pos, ref, alt FROM wt_{0} WHERE annotated=False LIMIT {1}'.format(analysis_id, RANGE_DEFAULT)
        qjoin    = ' '.join(['LEFT JOIN {0} '.format(self.db_map[db_uid]['join'].format('_var'), self.db_map[db_uid]) for db_uid in diff_dbs])
 


        # Loop to update working table annotation
        if qset_ann != "":
            for page in range(0, total, RANGE_DEFAULT):
                query = "UPDATE wt_{0} SET annotated=True, {1} FROM (SELECT _var.variant_id, {2} FROM ({3}) AS _var {4}) AS _ann WHERE wt_{0}.variant_id=_ann.variant_id".format(analysis_id, qset_ann, qslt_ann, qslt_var, qjoin)
                db_engine.execute(query)
                progress.update({"progress_current" : page})
                annso.notify_all(progress)
        progress.update({"step" : 4, "progress_current" : total})
        annso.notify_all(progress)


        # Loop to update working table attributes
        query = ""
        for a_name in attributes:
            if 'attr_{}'.format(a_name.lower()) not in current_fields:
                for sid in attributes[a_name].keys():
                    query += "UPDATE wt_{} SET attr_{}='{}' WHERE sample_id={}; ".format(analysis_id, a_name, attributes[a_name][sid], sid)
                    query += "CREATE INDEX wt_{0}_idx_attr_{1} ON wt_{0} USING btree (filter_{1});".format(analysis_id, a_name)
        if query != "":
            db_engine.execute(query)


        # Loop to update working table filter
        progress.update({"step" : 5})
        annso.notify_all(progress)
        
        for f_id in filter_ids:
            if 'filter_{}'.format(f_id) not in current_fields:
                f_filter = json.loads(db_engine.execute("SELECT filter FROM filter WHERE id={}".format(f_id)).first().filter)
                q = self.build_query(analysis_id, analysis.reference_id, 'table', f_filter, [], None)
                queries = q[0]
                if len(queries) > 0:
                    query = ""
                    for q in queries[:-1]:
                        query += q
                    query += "UPDATE wt_{} SET filter_{}=True WHERE variant_id IN ({}); ".format(analysis_id, f_id, queries[-1].strip()[:-1] )
                    query += "CREATE INDEX wt_{0}_idx_filter_{1} ON wt_{0} USING btree (filter_{1});".format(analysis_id, f_id)
                    db_engine.execute(query)


        progress.update({"step" : 6})
        annso.notify_all(progress)

        # Update count stat of the analysis
        query = "UPDATE analysis SET status='READY' WHERE id={}".format(analysis_id)
        db_engine.execute(query)

        # 1- Finir Update Working table simple (ajout d'annotation existante)
        # 2- Avec upload async dans un thread a pars (notif realtime avec progress bar UI)
        # 3- Feature : Quick site search bar : Core+UI
        # 4- Gestion des attributs dans la working table
        # 5- Gestion des saved filters dans la working table


        # 6- Ajout notion de status pour les analysis (IMPORTING VCF, ANNOTATING, READY, CLOSED)
        #    Avec meta data (pour progress bar notament)






    def request(self, analysis_id, mode, filter_json, fields=None, limit=100, offset=0, count=False):
        # Check parameters : if no field, select by default the first field avalaible to avoir error
        if fields is None: fields = [next(iter(self.fields_map.keys()))]
        if type(analysis_id) != int or analysis_id <=0 : analysis_id = None
        if mode not in ["table", "list"]: mode = "table"

        # Get analysis data and check status if ok to do filtering
        analysis = Analysis.from_id(analysis_id)
        if analysis is None:
            raise AnnsoException("Not able to retrieve analysis with provided id : {}".format(analysis_id)) 

        # Parse data to generate sql query and retrieve list of needed annotations databases/fields
        query, field_uids, dbs_uids, sample_ids, filter_ids, attributes = self.build_query(analysis_id, analysis.reference_id, mode, filter_json, fields, limit, offset, count)

        # Prepare database working table
        if analysis.status is None or analysis.status == '':
            self.create_working_table(analysis_id, sample_ids, field_uids, dbs_uids, filter_ids, attributes)
        else:
            self.update_working_table(analysis_id, sample_ids, field_uids, dbs_uids, filter_ids, attributes)

        # Execute query
        sql_result = None
        with Timer() as t:
            sql_result = db_engine.execute(' '.join(query))
        log ("---\nFields :\n{0}\nFilter :\n{1}\nQuery :\n{2}\nRequest query : {3}".format(fields, filter_json, '\n'.join(query), t))
        
        # Save filter in analysis settings
        if not count and (analysis_id > 0):
            settings = {}
            try : 
                settings = json.loads(db_engine.execute("SELECT settings FROM analysis WHERE id={}".format(analysis_id)).first().settings)
                settings["filter"] = filter_json
                settings["fields"] = fields
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





    def build_query(self, analysis_id, reference_id, mode, filter, fields, limit=100, offset=0, count=False):
        """
            This method build the sql query according to the provided parameters, and also build several list  with ids of
            fields, databases, sample, etc... all information that could be used by the analysis to work.
        """
        # Data that will be computed and returned by this method !
        query      = [] # sql queries that correspond to the provided parameters (we will have several queries if need to create temp tables)
        field_uids = [] # list of annotation field's uids that need to be present in the analysis working table
        db_uids    = [] # list of annotation databases uids used for the analysis
        sample_ids = [] # list of sample's ids used for the analysis
        filter_ids = [] # list of saved filter's ids for this analysis
        attributes = {} # list of attributes (and their values by sample) defined for this analysis

        # Retrieve sample ids of the analysis 
        for row in db_session.execute("select sample_id from analysis_sample where analysis_id={0}".format(analysis_id)):
            sample_ids.append(str(row.sample_id))

        # Retrieve attributes of the analysis 
        for row in db_session.execute("select sample_id, value, name from attribute where analysis_id={0}".format(analysis_id)):
            if row.name not in attributes.keys():
                attributes[row.name] = {row.sample_id : row.value}
            else:
                attributes[row.name].update({row.sample_id : row.value})

        # Init fields uid and db uids with the defaults annotations fields according to the reference (hg19 by example)
        for row in db_session.execute("SELECT d.uid AS duid, f.uid FROM annotation_database d INNER JOIN annotation_field f ON d.uid=f.database_uid WHERE d.reference_id={} AND d.type='variant' AND f.wt_default=True".format(reference_id)):
            if row.duid not in db_uids:
                db_uids.append(row.duid)
            field_uids.append(row.uid)

        # Retrieve saved filter's ids of the analysis - and parse their filter to get list of dbs/fields used by filters
        for row in db_session.execute("select id, filter from filter where analysis_id={0} ORDER BY id ASC".format(analysis_id)): # ORDER BY is important as a filter can "called" an oldest filter to be build.
            filter_ids.append(row.id)
            q, f, d = self.parse_filter(analysis_id, mode, sample_ids, row.filter, fields, None)
            field_uids = array_merge(field_uids, f)
            db_uids = array_merge(db_uids, d)

        # Parse the current filter
        query, f, d = self.parse_filter(analysis_id, mode, sample_ids, filter, fields, limit, offset, count)
        field_uids = array_merge(field_uids, f)
        db_uids    = array_merge(db_uids, d)
        
        # return query and all usefulldata about annotations needed to execute the query
        return query, field_uids, db_uids, sample_ids, filter_ids, attributes





    def parse_filter(self, analysis_id, mode, sample_ids, filters, fields=[], limit=100, offset=0, count=False):
        # Get working table
        wt = 'wt_{}'.format(analysis_id)
        query = ""
        field_uids = []
        db_uids = []

        # Build SELECT
        fields_names = []
        for f_uid in fields:
            if self.fields_map[f_uid]["db_uid"] not in db_uids:
                db_uids.append(self.fields_map[f_uid]["db_uid"])
            field_uids.append(f_uid)
            if self.fields_map[f_uid]['db_name_ui'] == 'Variant':
                fields_names.append('{}.{}'.format(wt, self.fields_map[f_uid]["name"]))
            else:
                fields_names.append('{}._{}'.format(wt, f_uid))
        q_select = 'variant_id{} {}'.format(',' if len(fields_names)>0 else '', ', '.join(fields_names))

        # Build FROM/JOIN
        q_from = wt 

        # Build WHERE 
        temporary_to_import = {}

        def check_field_uid(data):
            if data[0] == 'field':
                if self.fields_map[data[1]]["db_uid"] not in db_uids:
                    db_uids.append(self.fields_map[data[1]]["db_uid"])
                field_uids.append(data[1])

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
                check_field_uid(data[1])
                check_field_uid(data[2])
                return '{0}{1}{2}'.format(parse_value(t, data[1]), FilterEngine.op_map[operator], parse_value(t, data[2]))
            elif operator in ['IN', 'NOTIN']:
                tmp_table = get_tmp_table(data[1], data[2])
                temporary_to_import[tmp_table]['where'] = FilterEngine.op_map[operator].format(tmp_table, wt)
                if data[1] == 'site' :
                    temporary_to_import[tmp_table]['from']  = " LEFT JOIN {1} ON {0}.bin={1}.bin AND {0}.chr={1}.chr AND {0}.pos={1}.pos".format(wt, tmp_table)
                else: #if data[1] == 'variant' :
                    temporary_to_import[tmp_table]['from']  = " LEFT JOIN {1} ON {0}.bin={1}.bin AND {0}.chr={1}.chr AND {0}.pos={1}.pos AND {0}.ref={1}.ref AND {0}.alt={1}.alt".format(wt, tmp_table)
                return temporary_to_import[tmp_table]['where']

        def get_tmp_table(mode, data):
            """ 
                Parse json data to build temp table for ensemblist operation IN/NOTIN 
                    mode : site or variant
                    data : json data about the temp table to create
            """
            ttable_quer_map = "CREATE TEMP TABLE IF NOT EXISTS {0} AS {1}; "
            if data[0] == 'sample' :
                tmp_table_name    = "tmp_sample_{0}_{1}".format(data[1], mode)
                if mode == 'site':
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos FROM {0} WHERE {0}.sample_id={1}".format(wt, data[1]))
                else : # if mode = 'variant' :
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos, {0}.ref, {0}.alt FROM {0} WHERE {0}.sample_id={1}".format(wt, data[1]))
            elif (data[0] == 'filter') :
                tmp_table_name  = "tmp_filter_{0}".format(data[1])
                if mode == 'site':
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos FROM {0} WHERE {0}.filter_{1}=True".format(wt, data[1]))
                else : # if mode = 'variant' :
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos, {0}.ref, {0}.alt FROM {0} WHERE {0}.filter_{1}=True".format(wt, data[1]))
            elif (data[0] == 'attribute') :
                key, value = data[1].split(':')
                tmp_table_name    = "tmp_attribute_{0}_{1}_{2}_{3}".format(analysis_id, key, value, mode)
                if mode == 'site':
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos FROM {0} WHERE {0}.attr_{1}='{2}'".format(wt, key, value))
                else : # if mode = 'variant' :
                    tmp_table_query = ttable_quer_map.format(tmp_table_name, "SELECT DISTINCT {0}.bin, {0}.chr, {0}.pos, {0}.ref, {0}.alt FROM {0} WHERE {0}.attr_{1}='{2}'".format(wt, key, value))
            temporary_to_import[tmp_table_name] = {'query' : tmp_table_query}
            return tmp_table_name

        def parse_value(ftype, data):
            if data[0] == 'field':
                if self.fields_map[data[1]]["type"] == ftype :
                    if self.fields_map[data[1]]['db_name_ui'] == 'Variant':
                        return "{0}".format(self.fields_map[data[1]]["name"])
                    else:
                        return "_{0}".format(data[1])
            if data[0] == 'value':
                if ftype in ['int', 'float', 'enum', 'percent']:
                    return str(data[1])
                elif ftype == 'string':
                    return "'{0}'".format(data[1])
                elif ftype == 'range' and len(data) == 3:
                    return 'int8range({0}, {1})'.format(data[1], data[2])
            raise AnnsoException("FilterEngine.request.parse_value - Unknow type : {0} ({1})".format(ftype, data))

        q_where = ""
        if len(sample_ids) == 1 :
            q_where = "{0}.sample_id={1}".format(wt, sample_ids[0])
        elif len(sample_ids) > 1:
            q_where = "{0}.sample_id IN ({1})".format(wt, ','.join(sample_ids))

        q_where2 = build_filter(filters)
        if q_where2 is not None and len(q_where2.strip()) > 0:
            q_where += " AND " + q_where2



        # Build FROM/JOIN according to the list of used annotations databases
        q_from += " ".join([t['from'] for t in temporary_to_import.values()])
        

        # build final query
        query_tpm = [t['query'] for t in temporary_to_import.values()]
        if count:
            query_req = "SELECT DISTINCT {0} FROM {1} WHERE {2}".format(q_select, q_from, q_where)
            query =  query_tpm + ['SELECT COUNT(*) FROM ({0}) AS sub;'.format(query_req)]
        else: 
            query_req = "SELECT DISTINCT {0} FROM {1} WHERE {2} {3} {4};".format(q_select, q_from, q_where, 'LIMIT {}'.format(limit) if limit is not None else '', 'OFFSET {}'.format(offset) if offset is not None else '')
            query =  query_tpm + [query_req]


        return query, field_uids, db_uids










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