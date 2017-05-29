#!env/python3
# coding: utf-8
import ipdb

import os
import json
import datetime
import uuid
import psycopg2
import hashlib
import asyncio
import ped_parser



from config import *
from core.framework.common import *
from core.model import *
from core.annso import *


# =====================================================================================================================
# CORE OBJECT
# =====================================================================================================================

def notify_all_print(msg=None, src=None):
    """
        Default delegate used by the core for notification.
    """
    print(str(msg))


class Core:
    def __init__(self):
        self.annotations = AnnotationManager()
        self.analyses = AnalysisManager()
        self.samples = SampleManager()
        self.variants = VariantManager()
        self.filters = FilterEngine()
        self.files = FileManager()
        self.export_modules = {}
        self.import_modules = {}
        self.report_modules = {}

        # Load metada for activated modules
        for name in C.EXPORTS_MODULES:
            try:
                m = __import__('exports.{0}'.format(name))
                self.export_modules[name] = {
                    "info": eval('m.{0}.metadata'.format(name)),
                    "do": eval('m.{0}.export_data'.format(name))}
                self.export_modules[name].update({'id': name})
            except:
                err("Unable to load exports.{0} module".format(name))
        for name in C.IMPORTS_MODULES:
            try:
                m = __import__('imports.{0}'.format(name))
                self.import_modules[name] = {
                    "info": eval('m.{0}.metadata'.format(name)),
                    "do": eval('m.{0}.import_data'.format(name))}
                self.import_modules[name].update({'id': name})
            except:
                err("Unable to load imports.{0} module".format(name))
        for name in C.REPORTS_MODULES:
            try:
                m = __import__('reports.{0}.report'.format(name))
                self.report_modules[name] = {
                    "info": eval('m.{0}.report.metadata'.format(name)),
                    "do": eval('m.{0}.report.report_data'.format(name))}
                self.report_modules[name].update({'id': name})
            except Exception as error:
                ipdb.set_trace()
                err("Unable to load reports.{0} module".format(name))


        # method handler to notify all
        # according to api that will be pluged on the core, this method should be overriden 
        # to really do a notification. (See how api_rest override this method)
        self.notify_all = notify_all_print














# =====================================================================================================================
# INIT OBJECTS
# =====================================================================================================================


core = Core()
log('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
