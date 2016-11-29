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
# Base = automap_base()
# db_engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DATABASE_USER, DATABASE_PWD, DATABASE_HOST,  DATABASE_PORT, DB_NAME)
# Base.prepare(db_engine, reflect=True)
# Base.metadata.create_all(db_engine)
# db_session = Session(db_engine)







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MODEL DEFINITION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


class Analysis():
    id =                  23
    name =                "Analysis n°1"
    owner_id =            1234
    project_id =          56
    comments =            ""
    template_id =         1
    template_settings =   ""
    creation_date =       "2016-08-01"
    update_date =         "2016-08-17"
    status =              "ready"
    
    def __str__(self):
        return "Analysis"








class Template():
    id =                  2
    name =                "HugoDims"
    author_id =           1234
    description =         "Pipe for Hugo"
    version =             "V1.5"
    creation_date =       "2015-06-01"
    update_date =         "2016-04-12"
    parent_id =           1
    status =              "validated"
    configuration =       ""

    def __str__(self):
        return "Template"






class Selection():
    id =                  56432   
    analysis_id =         23
    name =                "Child DeNovo"
    order =               5
    comments =            "Selection of de novo variant of the child"
    query =               { "filters" : [{ "key" : "value"}] }

    def __str__(self):
        return "Selection"









class Sample():
    id =                  123456789
    name =                "Sample n°1"

    def __str__(self):
        return "Sample"





class Variant():
    id =                  123456789
    bin =                 156
    chr =                 2
    pos =                 54678231
    ref =                 "A"
    alt =                 ""
    annotations =         { }

    def __str__(self):
        return "Variant"












