#!env/python3
# coding: utf-8 
import os


DEBUG = True


# HOST (internal)
HOST = "127.0.0.1"
PORT = 8100
VERSION = "v1"
HOSTNAME = "{}:{}".format(HOST, PORT)  # This is the internal host on which aioHTTP will run the service.



# HOST (public)
HOST_P = "annso.absolumentg.fr"  # THIS url must be change if the annso server is reach via a public namespace that user
RANGE_DEFAULT = 100
RANGE_MAX = 1000


# DB
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_USER = "annso"
DATABASE_PWD = "annso"
DATABASE_NAME = "annso"
DATABASE_POOL_SIZE = 7


# FILESYSTEM
FILES_DIR = "/var/regovar/annso/files"
TEMP_DIR = "/var/regovar/annso/downloads"
CACHE_DIR = "/var/regovar/annso/cache"


# MODULES ACTIVATED
EXPORTS_MODULES = []
IMPORTS_MODULES = ["vcf"]
REPORTS_MODULES = []


# AUTOCOMPUTED VALUES
ANNSO_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ANNSO_DIR, "api_rest/templates/")
ERROR_ROOT_URL = "api.annso.org/errorcode/"


# INTERNAL CONSTANT
EXPORTS_MODULES_PATH = "exports.{0}"
IMPORTS_MODULES_PATH = "imports.{0}"
REPORTS_MODULES_PATH = "reports.{0}.report"


DEFAULT_REFERENCIAL_ID = 2 # hg19
