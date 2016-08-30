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


# Global variables
fields_allowed 		= ['id', 'email', 'firstname', 'lastname', 'function', 'location', 'last_activity', 'settings']
fields_default 		= ['id', 'firstname', 'lastname']
filter_fields  		= ['email', 'firstname', 'lastname', 'function', 'location', 'last_activity']
ordering_fields  	= ['id', 'email', 'firstname', 'lastname', 'function', 'location', 'last_activity', 'settings']
ordering_default 	= ['lastname' 'firstname']


""" This globale variable to manipulate user database model object (SQLAlchemy) """
User = Base.classes.user








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
	result = db_engine.execute("SELECT id, firstname, lastname, email, location, function, last_activity_date, settings FROM \"user\" WHERE id=%s" % user_id).first()

	if result is None:
		logid = err("rest_api_v1.users.get_user('" + user_id + "') : no user with this id found")
		return fmk_rest_error(ERRC_00001, "00001", logid)
	return fmk_rest_success(fmk_row2dict(result))




@app.route('/users/me')
def get_user_me():
	"""
		Return the currently logged in user
	"""

	me_id = session.get('user_id', -1);
	result = db_engine.execute("SELECT id, firstname, lastname, email, location, function, last_activity_date, settings FROM \"user\" WHERE id=%s" % me_id).first()

	if result is None:
		return fmk_rest_error(ERRC_00004, "00004", )
	return fmk_rest_success(fmk_row2dict(result))






@app.route('/users/', methods=['POST'])
def new_user():
	"""
		Create a new user with provided data.
	"""

	# Retrieve POST data
	data = dict(request.form)

	# TODO check that post data exists
	if data is None :
		logid = err("rest_api_v1.users.new_user() : no POST data found")
		return fmk_rest_error(ERRC_00003, "00003", logid)

	email = data["email"][0]
	password = data["password"][0]

	if not email:
		logid = err("rest_api_v1.users.new_user() : provided 'email' data is empty")
		return fmk_rest_error(ERRC_00003 + " : email", "00003", logid)
	if not password:
		logid = err("rest_api_v1.users.new_user() : provided 'password' data is empty")
		return fmk_rest_error(ERRC_00003 + " : password", "00003", logid)

	# Check if a user already exists in database with the provided email
	db_session = Session(db_engine)
	user = db_session.query(User).filter(User.email.like(email))

	if user is None:
		logid = logid = err("rest_api_v1.users.new_user() : another user already exists in database with the provided email.")
		return fmk_rest_error(ERRC_00003 + " : email (already exists)", "00003", logid)


	# Create new user
	user = None
	try:
		user = User()
		user.password		= generate_password_hash(password)
		user.email 			= email
		user.firstname 		= data.get('firstname', 			[None])[0]
		user.lastname 		= data.get('lastname', 				[None])[0]
		user.function 		= data.get('function', 				[None])[0]
		user.location 		= data.get('location', 				[None])[0]
		user.last_activity	= data.get('last_activity_date', 	[None])[0]
		user.settings 		= data.get('settings', 				[None])[0]

		# Register in database
		db_session.add(user)
		db_session.commit()
	except:
		user = None
		data['password'] = ['****']
		logid = err("rest_api_v1.users.new_user() : Failed to create a user with provided data : " + str(data))
		return fmk_rest_error(ERRC_00002, "00002", logid)
		
	# Return id of the new user
	return fmk_rest_success({"id":user.id})

	

	



@app.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
	# Retrieve PUT data
	data = dict(request.form)

	# check that post data exists
	if data is None :
		logid = err("rest_api_v1.users.edit_user() : no PUT data found")
		return fmk_rest_error(ERRC_00003, "00003", logid)

	uid = data.get('uid', [None])[0]	

	if not uid:
		logid = err("rest_api_v1.users.edit_user() : provided 'uid' data is empty")
		return fmk_rest_error(ERRC_00003 + " : uid", "00003", logid)

	# Edit user
	db_session = Session(db_engine)
	user = db_session.query(User).get(int(uid))


	# Check that user exists
	if not user:
		logid = err("rest_api_v1.users.edit_user() : user doesn't exists (uid="+uid+")")
		return fmk_rest_error(ERRC_00001 + " : uid", "00001", logid)

	# Check that connected user is allowed to edit data
	session_uid = session.get('user_id', -1)
	if (session_uid == uid or session.get('user_admin', False)):
		pass

	# Need to reset password
	if (data.get('newpassword', [False])[0]):
		oldpwd  = data.get('oldpassword',  [''])[0]
		newpwd1 = data.get('newpassword1', [''])[0]
		newpwd2 = data.get('newpassword2', [''])[0]

		if newpwd1 != newpwd2 :
			log_id = err("rest_api_v1.users.edit_user() : provided 'new password' and 'confirmation password' are different. No data have been updated.")
			return fmk_rest_error(ERRC_00003 + " : uid", "00003", log_id)
			ERRC_00002

		# if (check_password_hash(pw_hash, newpwd1)
		#user.password		= generate_password_hash(newpwd1)


		
	try:
		user.email 			= data.get('email', 				[None])[0] or user.email
		user.firstname 		= data.get('firstname', 			[None])[0] or user.firstname
		user.lastname 		= data.get('lastname', 				[None])[0] or user.lastname
		user.function 		= data.get('function', 				[None])[0] or user.function
		user.location 		= data.get('location', 				[None])[0] or user.location
		user.last_activity	= data.get('last_activity_date', 	[None])[0] or user.last_activity_date
		user.settings 		= data.get('settings', 				[None])[0] or user.settings

		# Register in database
		db_session.add(user)
		db_session.commit()
	except:
		user = None
		data['oldpassword']  = ['****']
		data['newpassword1'] = ['****']
		data['newpassword2'] = ['****']

		logid = err("rest_api_v1.users.edit_user() : Failed to update a user with provided data : " + str(data))
		return fmk_rest_error(ERRC_00002, "00002", logid)

		
	# Return id of the new user
	return fmk_rest_success()









@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):

	# Check that user exists user
	db_session = Session(db_engine)
	user = db_session.query(User).get(int(user_id))


	# Check that user exists
	if not user:
		logid = err("rest_api_v1.users.delete_user() : user doesn't exists (user_id="+user_id+")")
		return fmk_rest_error(ERRC_00001 + " : user_id", "00001", logid)

	# Check that connected user is allowed to edit data
	session_uid = session.get('user_id', -1)
	if (session_uid == user_id or session.get('user_admin', False)):
		pass


	# Check that user is not link to a template or an alaysis
	# TODO


	# Delete user
	try:
		db_engine.execute("DELETE FROM \"user\" WHERE id=%s" % user_id)
	except:
		logid = err("rest_api_v1.users.delete_user() : Unespected error : " + str(sys.exc_info()[1]))
		return fmk_rest_error(ERRC_00000, "00000", logid)

		
	# Return id of the new user
	return fmk_rest_success()










@app.route('/users/login', methods=['GET'])
def login_user():
	print ("LOGIN")
	data = request.get_json(force=False)
	email    = data.get("email")
	password = data.get("password")

	user = db_session.query(User).filter(User.email.like(email)).filter(User.password.like(generate_password_hash(password)))

	if user is None:
		return error_response("Bad login or password")
	else:
		session['user_id'] = str(user.id)

	print("Login user ", login, " : ", session["user_id"])
	return success_response(session['user_id'])








@app.route('/users/logout')
def logout_user():
	print("Logout - delete session : ", session["user_id"])
	session.pop("user_id", None)
	return success_response()






