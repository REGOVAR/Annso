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
from flask.ext.session import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# Regovar common packages
from regovar.config import *
from regovar.common import *



# 
# Server init =====================================================================================
#

# Initialization of application
app = Flask(__name__)


# Load configuration from config.py
app.config.from_pyfile("config.py")


# Creat/connect database
# connect(app.config["DATABASE"])
# engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
# Base = declarative_base()
# Base.metadata.reflect(engine)


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