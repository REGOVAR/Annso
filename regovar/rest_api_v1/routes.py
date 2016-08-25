#!env/python3
# coding: utf-8
from regovar.rest_api_v1 import rest_common
from regovar.rest_api_v1 import users

from regovar.application import app 



@app.route('/config/')
def api_get_config():
	return rest_common.api_get_config()