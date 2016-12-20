#!env/python3
# coding: utf-8 
import os


DEBUG          = True


# HOST
HOST           = "0.0.0.0"
PORT           = "8100"
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
FILES_DIR     = "/tmp/annso_" + VERSION + "/files"
TEMP_DIR      = "/tmp/annso_" + VERSION + "/downloads"
CACHE_DIR     = "/tmp/annso_" + VERSION + "/cache"

# AUTOCOMPUTED VALUES
ANNSO_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR   = os.path.join(ANNSO_DIR, "api_rest/templates/")
ERROR_ROOT_URL = "api.pirus.org/errorcode/"


