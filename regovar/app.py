#!env/python3
# coding: utf-8

import os
import sys
import datetime
import reprlib
import time
import logging


from config import *
from common import *

from rest_api_v1 import *



from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)

Base = declarative_base()
Base.metadata.reflect(engine)





app = Flask(__name__)

@app.route("/")
def welcom():
    return "Regovar Up !"

if __name__ == "__main__":
    app.run() 





class RestUser:







User
{
    "id" :                  1234
    "email" :               "user@regovar.org"
    "firstname" :           "Pierre"
    "lastname" :            "Dupont"
    "function" :            "Interne en génétique"
    "location" :            "CHU Angers"
    "last_activity" :       "2016-08-17"
    "settings" :            { "key" : "value" }
}

def rest_to_user():
	pass
def user_to_rest():
	pass



def rest_parse_url(url:str):
	# Get Domaine
	# Get Version
	# Get Resource
	# Get Action
	# Get params for Lazy Loading
	# Get params for Light Filtering
	# Get params for Ordering
	# Get params for Pagination

	# Build query for PostgreSQL database

	# Retrieve result

	# handle error

	# Return result : json_data, error_code, error_msg
	pass

def rest_parse_user():
	pass

