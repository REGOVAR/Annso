#!env/python3
# coding: utf-8 
import os

# Website config
DEBUG                     = True
SESSION_TYPE			  = "mongodb"
VERSION                   = "1.0"
SECRET_KEY				  = "regovar"

# Database parameters
DB_HOST                   = "localhost"
DB_PORT                   = 5432
DB_USER                   = "regovar"
DB_PWD                    = "regovar"
DB_NAME                   = "regovar"

# Folders
BASEDIR                   = os.path.abspath(os.path.dirname(__file__))
LOGDIR                    = os.path.join(BASEDIR, '../logs')

# Regovar files repository
REP_VCF                   = os.path.join(BASEDIR, '../files/vcf')
REP_BAM                   = os.path.join(BASEDIR, '../files/bam')
REP_INPUT                 = os.path.join(BASEDIR, '../files/user_input/')
UPLOAD_ALLOWED_EXTENSIONS = set(["vcf","gvcf","gz","bam"])




# Regovar REST API parameters
REST_DOMAIN               = "http://127.0.0.1:5000/api"
REST_VERSION              = "1"
REST_RANGE_MAX            = 1000
REST_RANGE_DEFAULT        = 50

# root urls shortcuts
REST_ROOT_URL             = REST_DOMAIN + "/v" + REST_VERSION + "/"
WWW_ROOT_URL              = "http://127.0.0.1:5000/www/"
ERROR_ROOT_URL            = "http://127.0.0.1:5000/www/error/"