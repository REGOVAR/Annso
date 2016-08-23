#!env/python3
# coding: utf-8
from flask import Flask, jsonify, render_template, session, request
from flask_session import Session
from flask_login import LoginManager



# 
# Building response ===============================================================================
#

def rest_success(response_data=None, pagination_data=None):
	if response_data is None:
		results = {"success":True}
	else:
		results = {"success":True, "data":response_data}

	if pagination_data is None:
		results.update(pagination_data)

	return jsonify(results)


def rest_error(message="Unknown", code="0"):
	results = {"success":False, "msg":message, "error_code":code, "error_url":ERROR_ROOT_URL + code}
	return jsonify(results)




# 
# Database helper ============================================================================
#
def db_request(connection, sql_req, ):
	if connection is None:
		return rest_error(ERRC_00001)






# 
# Server configuration ============================================================================
#
def get_config(sql_connection=None):

	db_data = {}
	if sql_connection is None:
		db_data = {"db_version": ERRC_00001}
	else:
		sql_connection.execute("SELECT * FROM parameter")
		# TODO : Retrieve data from database with manage error methode

	result = { 
		"domain" :          REST_DOMAIN, 
		"version" :         REST_VERSION,
		"range_max" :       REST_RANGE_MAX,
		"range_default" :   REST_RANGE_DEFAULT
	}

	result.update(db_data)

	return jsonify(result)








# 
# ERROR LIST =============================================================================
#

# Unknow error
# data error  : consistency, missing entry, ...
# db error    : structure, bad req (missing field,...), wrong db version, no connection to database, ...
# 


# error code = "0"
ERRC_00000 = "Sorry, an unhandled error occure :s ... \nThanks to ask an admin to check what appened.\nDont hesitate to report this error to the dev@regovar.org team in order to fix it."
ERRC_00001 = "No Data"




