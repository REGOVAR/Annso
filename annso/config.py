#!env/python3
# coding: utf-8 
import os


DEBUG          = True


# HOST
HOST           = "dev1.absolumentg.fr"
PORT           = "8080"
VERSION        = "v1"
HOSTNAME       = HOST + ":" + PORT + "/" + VERSION


RANGE_DEFAULT = 20
RANGE_MAX     = 1000

# DB
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_USER = "annso"
DATABASE_PWD  = "ansso"
DATABASE_NAME = "annso"



# FILESYSTEM
FILES_DIR     = "/tmp/pirus_" + VERSION + "/files"
TEMP_DIR      = "/tmp/pirus_" + VERSION + "/downloads"


# AUTOCOMPUTED VALUES
ANNSO_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR   = os.path.join(ANNSO_DIR, "api_rest/templates/")
ERROR_ROOT_URL = "api.pirus.org/errorcode/"


