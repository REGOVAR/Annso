#!env/python3
# coding: utf-8
from flask import Flask, jsonify, render_template, session, request
from flask.ext.session import Session
from flask.ext.login import LoginManager



# 
# Building response ===============================================================================
#

def build_success(response_data=None, pagination_data=None):
	if response_data is None:
		results = {"success":True}
	else:
		results = {"success":True, "data":response_data}

	if pagination_data is None:
		results.update(pagination_data)

	return jsonify(results)


def build_error(message="Unknown", code="0"):
	results = {"success":False, "msg":message, "error_code":code, "error_url":ERROR_ROOT_URL + code}
	return jsonify(results)




# 
# Database helper ============================================================================
#
def db_request(connection, sql_req, ):
	if connection is None:
		return build_error(ERROR.)






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
		"version" :         REST_VERSION
		"range_max" :       REST_RANGE_MAX
		"range_default" :   REST_RANGE_DEFAULT
	}

	result.update(db_data)

	return jsonify(result)





# 
# User authentication =============================================================================
#


'''  '''
def check_auth(f):
	def called(*args, **kargs):
		if 'user_id' in session:
			user = User.from_id(session["user_id"])
			if user is not None:
				return f(*args, **kargs)
		return error_response("Authentification is required", 403)
	return called

def current_user():
	if 'user_id' in session:
		user = User.from_id(session["user_id"])
		return user
	return None



''' check authent on all request '''
@app.before_request
def before_request():
	if session and "user_id" in session:
		print("Check auth : " + str(session))
		if 'user_id' in session:
			user = User.from_id(ObjectId(session["user_id"]))
			if user is not None:
				print ("Session Valid")
				session['username'] = user.fullname
				return

		print ("Session not valid")
		return error_response("Authentification is required", 403)
	else:
		if request.url_root == 'login_user' or request.url_root == 'login':
			print("Trying to connect, not checking session auth yet")
		else:
			print (request.url_root)
			print ("Session not valid -> need to login")
			#return error_response("Authentification is required", 403)

'''
	if request :
		print( "Endpoint : " + str(request))
	else:
		print("Endpoint : None")
    #if 'logged_in' not in session and request.endpoint != 'login':
'''



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




