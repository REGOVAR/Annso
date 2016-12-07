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





from core.framework import *
from core.model import *
from core.core import annso



class AnnotationInterface:
    """ All other annotation extensions needed by this one shall be listed here """
    dependencies = []

    """ By default the extension is disabled, it will be enabled at the __init__ if all requierements are fullfilled """
    disabled = True


    def __init__(self):
        """ 
            In the init all check must be done if requierement are well installed
        """
        #if dependencies in annso.extensions:
        disabled = True



    def public_fields(self):


        
INSERT INTO public.annotation_fields(database_id, name) VALUES 
  (@id, 'name', 'string', '', NULL),
  (@id, 'chrom', 'string', '', NULL),
  (@id, 'strand', 'string', '', NULL),
  (@id, 'tx', 'range_int', '', NULL),
  (@id, 'cds', 'range_int', '', NULL),
  (@id, 'exoncount', 'int', '', NULL),
  (@id, 'exons', 'list_range_int', '', NULL),
  (@id, 'score', 'int', '', NULL),
  (@id, 'name2', 'string', '', NULL),
  (@id, 'score', 'int', '', NULL),
  (@id, 'score', 'int', '', NULL),
        return ["field 1", "field 2"]


    def total(self):
        """ Return total number of entry in database or None if not possible """
        return None


    def get(self, fields=None, query=None, order=None, offset=None, limit=None, sublvl=0):
        """ Generic method to request annotations """
        return None


    def get_form(self, fields=None):
        """ Return JSON that describes the form(s) to used to filter on provided fields """
        return None


    def get_type(self, fields=None):
        """ Return JSON that describes the type(s) of the provided field(s). This information should be used by the HMI to display properly annotation """
        return None



