#!env/python3
# coding: utf-8
import os
import sys
import time
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

User = Base.classes.user
Project = Base.classes.project
Sample = Base.classes.sample
Variant = Base.classes.variant_hg19
SampleVariant = Base.classes.sample_variant_hg19
Analysis = Base.classes.analysis
Selection = Base.classes.selection
Template = Base.classes.template
Subject = Base.classes.subject
File = Base.classes.file













