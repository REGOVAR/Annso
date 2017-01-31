#!env/python3
# coding: utf-8 
import os


DEBUG          = True



# HOST (internal)
HOST            = "0.0.0.0"
PORT            = "8100"
VERSION         = "v1"
HOSTNAME        = HOST + ":" + PORT + "/" + VERSION



# HOST (public)
HOST_P          = "rego2.absolumentg.fr/" + VERSION
RANGE_DEFAULT   = 20
RANGE_MAX       = 1000



# DB
DATABASE_HOST   = "localhost"
DATABASE_PORT   = "5432"
DATABASE_USER   = "annso"
DATABASE_PWD    = "ansso"
DATABASE_NAME   = "annso"



# FILESYSTEM
FILES_DIR       = "/tmp/annso_" + VERSION + "/files"
TEMP_DIR        = "/tmp/annso_" + VERSION + "/downloads"
CACHE_DIR       = "/tmp/annso_" + VERSION + "/cache"



# MODULES ACTIVATED
EXPORTS_MODULES = ["csv"]
IMPORTS_MODULES = ["vcf"]
REPORTS_MODULES = ["dims"]



# AUTOCOMPUTED VALUES
ANNSO_DIR           = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR        = os.path.join(ANNSO_DIR, "api_rest/templates/")
ERROR_ROOT_URL      = "api.pirus.org/errorcode/"


# INTERNAL CONSTANT
EXPORTS_MODULES_PATH = "exports.{0}"
IMPORTS_MODULES_PATH = "imports.{0}"
REPORTS_MODULES_PATH = "reports.{0}.report"

