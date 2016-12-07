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
from core.annotation import AnnotationInterface






class RefGeneManager(AnnotationInterface):
    """ All other annotation extensions needed by this one shall be listed here """
    dependencies = []

    """ By default the extension is disabled, it will be enabled at the __init__ if all requierements are fullfilled """
    disabled = True


    type_details = {
        "name" : {
            "type" : "string",
            "form" : "text",
            "desc" : "The name of the referenced gene in USCIS"
        }, 
        "chrom" : {}, 
        "strand" : {}, 
        "tx" : {}, 
        "cds" : {}, 
        "exoncount" : {}, 
        "exons" : {}, 
        "score" : {}, 
        "name2"
        }



    def __init__(self):
        """ 
            In the init all check must be done if requierement are well installed
        """
        #if dependencies in annso.extensions:
        disabled = True



    def public_fields(self):
        return ["name", "chrom", "strand", "tx", "cds", "exoncount", "exons", "score", "name2"]


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



