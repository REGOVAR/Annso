#!env/python3
# coding: utf-8
import sys
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash


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








# generate_password_hash(password)
# check_password_hash(pw_hash, password)











@app.route('/users/help')
def api_get_users_help():
	return fmk_rest_success({
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
	})





@app.route('/users/')
def get_users():
	''' 
		Return list of user
		Customisation allowed via following attributes :
		 - fields
		 - filter
		 - order
		 - range
	'''

	# 1- Requested fields
	sql_select, fields = fmk_get_fields_to_sql(f_default=fields_default, f_allowed=fields_allowed, f_type=str)
	
	# 2- Filter ?
	sql_where = ""

	# 3- Ordering results
	sql_ordering = fmk_get_ordering_to_sql(o_default=ordering_default, o_allowed=ordering_fields)

	# 4- Pagination
	sql_limit = fmk_get_pagination_to_sql(p_default='0-' + str(REST_RANGE_DEFAULT))

	# 6- Retrieve data from SQL
	sql = sql_select + " FROM \"user\" " + sql_where + sql_ordering + sql_limit
	result = db_engine.execute(sql)
	order = 0
	if (result):
		d = {}
		for row in result:
			d[order] = fmk_row2dict(row)
			order += 1
	return fmk_rest_success(d)





@app.route('/users/<user_id>')
def get_user(user_id):
	"""
		Return the user with the given id if exists. Otherwise return an error.
		Customisation allowed via following attributes :
		 - fields
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
	# Retrieve POST data
	data = dict(request.form)

	# TODO check that post data exists
	if data is None :
		err("rest_api_v1.users.new_user() : no POST data found")
		return fmk_rest_error(ERRC_00003, "00003")

	email = data["email"][0]
	password = data["password"][0]

	if not email:
		err("rest_api_v1.users.new_user() : provided 'email' data is empty")
		return fmk_rest_error(ERRC_00003 + " : email", "00003")
	if not password:
		err("rest_api_v1.users.new_user() : provided 'password' data is empty")
		return fmk_rest_error(ERRC_00003 + " : password", "00003")

	print ("@:" + email + ":" + password)
	# Create new user
	user = None
	
	print(data)

	try:
		db_session = Session(db_engine)

		user = User()
		user.password		= password
		user.email 			= email
		user.firstname 		= data.get('firstname', 	[None])[0]
		user.lastname 		= data.get('lastname', 		[None])[0]
		user.function 		= data.get('function', 		[None])[0]
		user.location 		= data.get('location', 		[None])[0]
		user.last_activity	= data.get('last_activity', [None])[0]
		user.settings 		= data.get('settings', 		[None])[0]

		db_session.add(user)
		db_session.commit()
	except:
		user = None
		err("rest_api_v1.users.new_user() : Failed to create a user with provided data : " + str(data))
		return fmk_rest_error(ERRC_00002, "00002")
		

	return fmk_rest_success({"id":user.id})

	

	# Register in database

	# Return id of the new user



@app.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
	return '/users/<user_id>'





@app.route('/users/login', methods=['GET'])
def login_user():
	return '/users/login'





@app.route('/users/logout')
def logout_user():
	return '/users/logout'
