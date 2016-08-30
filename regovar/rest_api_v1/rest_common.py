#!env/python3
# coding: utf-8
import re

from flask import Flask, jsonify, session, request


from regovar.config import *
from regovar.common import *









def fmk_check_session():
	'''
		Check that the current session is valid and the user well identified
	'''
	pass





# 
# Building response ===============================================================================
#

def fmk_rest_success(response_data=None, pagination_data=None):
	"""
		Build the REST success response that will encapsulate the given data (in python dictionary format)

		:param response_data: 	The data to wrap in the JSON success response
		:param pagination_data:	The data regarding the pagination
	"""

	if response_data is None:
		results = {"success":True}
	else:
		results = {"success":True, "data":response_data}

	if pagination_data is not None:
		results.update(pagination_data)

	return jsonify(results)



def fmk_rest_error(message:str="Unknow", code:str="0", error_id:str=""):
	"""
		Build the REST error response

		:param message: 	The short "friendly user" error message
		:param code:		The code of the error type
		:param error_id:	The id of the error, to return to the end-user. 
							This code will allow admins to find in logs where exactly this error occure
	"""

	results = {
		"success":		False, 
		"msg":			message, 
		"error_code":	code, 
		"error_url":	ERROR_ROOT_URL + code,
		"error_id":		error_id
	}

	return jsonify(results)




# 
# Database helper ============================================================================
#

def db_request(connection, sql_req, ):
	if connection is None:
		return rest_error(ERRC_00001)





def fmk_row2dict(row):
    d = {}
    for column in row.keys():
        d[column] = str(getattr(row, column))

    return d




# 
# URL query string parsing ========================================================================
#


def fmk_get_query_multiset_parameter(f_name:str, f_default:str, f_allowed:object="*", f_type:object=object):
	"""
		Return a list a value for a provided query string attribute. 
		Manage default value, and check validity of values
	"""

	# 1- retrieve parameter or default value if doesn't exists
	fields = request.args.get(f_name, default=','.join(f_default), type=f_type)
	fields_t = fields.split(',')

	# 2- check that value are allowed
	result = []
	if f_allowed != "*":
		for entry in fields_t:
			entry = entry.strip()
			if entry in f_allowed:
				result.append(entry)
	else:
		result = fields_t

	return result;




def fmk_get_fields_to_sql(f_default:str, f_allowed:object="*", f_type:object=object):
	""" 
		Default fmk method to retrieve list of fields that shall be loaded. 

		:param f_default:	The list of default value that shall be used if nothing is found in the query string
		:param f_allowed:	The list of allowed value
		:param f_type:		The type of the value in the field (can be : int, str, object...)
		:return: 			The sql raw string and selected fields in an array
	"""

	fields = fmk_get_query_multiset_parameter('fields', f_default, f_allowed, f_type)
	return "SELECT " + ', '.join(fields), fields




def fmk_get_ordering_to_sql(o_default:str, o_allowed:object="*", f_type:object=object):
	"""
		Retrieve if exists query string attributes that specify the ordering.
		Otherwise return the provided default ordering

		:param o_default:	The list of default value that shall be used if nothing is found in the query string
		:param o_allowed:	The list of allowed value
		:param f_type:		The type of the value in the field (can be : int, str, object...)
		:return: 			The sql raw string
	"""

	asc  = fmk_get_query_multiset_parameter('order', f_default=['lastname', 'firstname'], f_allowed=o_allowed, f_type=str)
	desc = fmk_get_query_multiset_parameter('desc', f_default='', f_allowed=o_allowed, f_type=str)

	sql_ordering = ""
	if len(asc) > 0:
		sql_ordering = " ORDER BY "
		for i in range(0, len(asc)):
			sql_ordering += asc[i]
			if asc[i] in desc :
				sql_ordering += " DESC,"
			else:
				sql_ordering += " ASC,"

	return sql_ordering[:-1]




def fmk_get_pagination_to_sql(p_default:str):
	"""
		Retrieve if exists query string attributes that specify the pagination for the returned result.

		:param p_default: 	Default pagination to used if nothing found in the query
		:return:			The sql raw string
	"""

	pagination = request.args.get('range', default=p_default, type=str)

	# 4.1- checking that range provided by user is valid
	range_pattern = re.compile("^[0-9]*-[0-9]*$")
	check = range_pattern.match(pagination)

	if check is None:
		pagination = "0-" + str(REST_RANGE_DEFAULT)

	# 4.2- parsing range
	pagination = pagination.split("-")
	limit = min(int(pagination[1]) - int(pagination[0]), REST_RANGE_MAX)
	offset = pagination[0]

	# 4.3- building sql_raw
	return " LIMIT " + str(limit) + " OFFSET " + str(offset)








# 
# ERROR LIST =============================================================================
#

# Unknow error
# data error  : consistency, missing entry, ...
# db error    : structure, bad req (missing field,...), wrong db version, no connection to database, ...
# query error : error while parsing the url (bad format, 404, missing attributes, bad values, ...)
# 


# error code = "0"
ERRC_00000 = "Sorry, an unhandled error occure :s ... \nThanks to ask an admin to check what appened.\nDont hesitate to report this error to the dev@regovar.org team in order to fix it."
ERRC_00001 = "Requested data doesn't exists"
ERRC_00002 = "Wrong provided data"
ERRC_00003 = "Missing provided data"
ERRC_00004 = "You are not authenticated. Please log in."





