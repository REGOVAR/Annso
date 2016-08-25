#!env/python3
# coding: utf-8



# 
# Import modules ==================================================================================
#

# General packages
import os
import sys
import datetime
import reprlib
import time
import logging


# Specifi packages
from flask import Flask, session
from flask_session import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


# Regovar common packages
from regovar.config import *
from regovar.common import *





# 
# Log init ========================================================================================
#
if DEBUG :
	logging.basicConfig(filename='regovar.log',level=logging.DEBUG)
else:
	logging.basicConfig(filename='regovar.log',level=logging.INFO)


# 
# Server init =====================================================================================
#

# Initialization of application
app = Flask(__name__)


# Load configuration from config.py
app.config.from_pyfile("config.py")


# Connect and map the engine to the database
Base = automap_base()
db_engine = create_engine("postgresql://" + DB_USER + ":" + DB_PWD + "@" + DB_HOST + ":" + str(DB_PORT) + "/" + DB_NAME)
#engine = create_engine("postgresql://regovar:regovar@localhost:5432/regovar")
Base.prepare(db_engine, reflect=True)

db_session = Session(db_engine)



# Create/Check directories and permissions
# if not os.path.exists(app.config["UPLOAD_FOLDER"]):
# 	os.makedirs(app.config["UPLOAD_FOLDER"])


# Manage user session
Session(app)










# 
# Now that server app is created, we can import specific regovar packages =========================
#



# REST API used : V1
import regovar.rest_api_v1

# Web site
import regovar.www





# 
# OK Let's go ! ===================================================================================
#

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0")