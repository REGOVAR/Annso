#!env/python3
# coding: utf-8
from regovar.config import *
from regovar.common import *
from regovar.application import app

from regovar.rest_api_v1.rest_common import *
from regovar.application import Base, db_engine



# User resource :
# User
# {
#     "id" :                  1234
#     "email" :               "user@regovar.org"
#     "firstname" :           "Pierre"
#     "lastname" :            "Dupont"
#     "function" :            "Interne en génétique"
#     "location" :            "CHU Angers"
#     "last_activity" :       "2016-08-17"
#     "settings" :            { "key" : "value" }
# }


# User lazy loading (fields that are loaded if "fields" attribute is not specified in the query) :
# User
# {
#     "id" :                  1234
#     "firstname" :           "Pierre"
#     "lastname" :            "Dupont"
# }


# Global variables
fields_allowed 		= ['id', 'email', 'firstname', 'lastname', 'function', 'location', 'last_activity', 'settings']
fields_default 		= ['id', 'firstname', 'lastname']
filter_fields  		= ['email', 'firstname', 'lastname', 'function', 'location', 'last_activity']
ordering_fields  	= ['id', 'email', 'firstname', 'lastname', 'function', 'location', 'last_activity', 'settings']
ordering_default 	= ['lastname' 'firstname']

""" This globla variable to manipulate user database model object (SQLAlchemy) """
User = Base.classes.user



@app.route('/users/help')
def api_get_users_help():
	return {
		'GET /users/help/' : ['this help'],
		'GET /users/' : 
		{
			'description' : 			'Return the list of users',
			'lazy_loading_allowed' :	fields_allowed,
			'lazy_loading_default' :	fields_default,
			'filtering_fields_allowed':	filter_fields,
			'ordering_allowed' :		ordering_fields,
			'ordering_default' :		ordering_default
		}


	}





@app.route('/users/')
def get_users():
	''' 
		Return list of user (to use with filter and pagination attributes) 
	'''

	# 1- Requested fields
	sql_select = fmk_get_fields_to_sql(f_default=fields_default, f_allowed=fields_allowed, f_type=str)
	
	# 2- Filter ?
	sql_where = ""

	# 3- Ordering results
	sql_ordering = fmk_get_ordering_to_sql(o_default=ordering_default, o_allowed=ordering_fields)

	# 4- Pagination
	sql_limit = fmk_get_pagination_to_sql(p_default='0-' + str(REST_RANGE_DEFAULT))

	# 6- Retrieve data from SQL
	return fmk_rest_success(sql_select + " FROM \"user\" " + sql_where + sql_ordering + sql_limit)





@app.route('/users/<user_id>')
def get_user(user_id):
	"""
		Return the user with the given id if exists. Otherwise return an error
	"""
	result = db_engine.execute("SELECT * FROM \"user\" WHERE id=%s" % user_id).first()

	if result is None:
		return fmk_rest_error(ERRC_00001, "00001", )
	return fmk_rest_success(fmk_row2dict(result))




@app.route('/users/me')
def get_user_me():
	"""
		Return the currently logged in user
	"""

	me_id = 1; # TODO : retrieve it from session data
	result = db_engine.execute("SELECT * FROM \"user\" WHERE id=%s" % me_id).first()

	if result is None:
		return fmk_rest_error(ERRC_00001, "00001", )
	return fmk_rest_success(fmk_row2dict(result))




@app.route('/users/', methods=['POST'])
def new_user():
	return '/users/<user_id>'

@app.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
	return '/users/<user_id>'



@app.route('/users/login', methods=['GET'])
def login_user():
	return '/users/login'



@app.route('/users/logout')
def logout_user():
	return '/users/logout'
