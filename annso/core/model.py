#!env/python3
# coding: utf-8
import os
import sys
import time
import datetime
import logging
import json
import yaml
import subprocess
import tarfile
import shutil

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from core.framework import *




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# DATABASE CONNECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




# Connect and map the engine to the database
Base = automap_base()
#db_engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DATABASE_USER, DATABASE_PWD, DATABASE_HOST,  DATABASE_PORT, DATABASE_NAME))
db_engine = create_engine("postgresql://annso:annso@localhost/annso")
Base.prepare(db_engine, reflect=True)
Base.metadata.create_all(db_engine)
db_session = Session(db_engine)







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MODEL DEFINITION - Build from the database (see sql scripts used to generate the database)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


Analysis = Base.classes.analysis
Template = Base.classes.template
Sample = Base.classes.sample
Variant = Base.classes.variant_hg19
SampleVariant = Base.classes.sample_variant_hg19
Selection = Base.classes.selection

Attribute = Base.classes.attribute

File = Base.classes.file



Analysis.public_fields = ["id", "name", "template_id", "creation_date", "update_date"]
Template.public_fields = ["id", "name", "author", "description", "version", "creation_date", "update_date"]
Sample.public_fields   = ["id", "name", "comments", "is_mosaic"]
File.public_fields     = ["id", "filename", "upload_offset", "size", "type", "import_date"]




def export_client_sample(self, fields=None):
    result = {}
    if fields is None:
        fields = Sample.public_fields
    for f in fields:
        result.update({f : eval("self." + f)})
    return result



def export_client_analysis(self, fields=None):
    result = {}
    if fields is None:
        fields = Analysis.public_fields
    for f in fields:
        if f == "creation_date" or f == "update_date":
            result.update({f : eval("self." + f + ".ctime()")})
        else:
            result.update({f : eval("self." + f)})
    return result



def new_sample_file_from_tus(filename, file_size):
    global db_session
    sfile = File()
    sfile.filename = filename
    sfile.type = os.path.splitext(filename)[1][1:].strip().lower()
    sfile.path = os.path.join(TEMP_DIR, str(uuid.uuid4()))
    sfile.size = int(file_size)
    sfile.upload_offset = 0
    sfile.import_date = str(datetime.datetime.now().timestamp())
    db_session.add(sfile)
    db_session.commit()
    return sfile



Analysis.export_client = export_client_analysis 
Sample.new_from_tus = new_sample_file_from_tus
Sample.export_client = export_client_sample