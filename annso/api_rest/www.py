#!env/python3
# coding: utf-8
import os
import jinja2
from flask import Flask, jsonify, render_template, session, request
from flask_session import Session
from flask_login import LoginManager

from regovar.application import app
from regovar.application import Base, db_session



# 
# CONFIG parameters for the website package =======================================================
#

# Flask Folders
WWWDIR			= os.path.abspath(os.path.dirname(__file__))
TPL_FOLDER 		= os.path.join(WWWDIR, 'templates/')
ASSET_FOLDER 	= os.path.join(WWWDIR, 'statics/')




# 
# Customise flask app with package path ===========================================================
#
my_loader = jinja2.ChoiceLoader([
	app.jinja_loader, 						# first is default template path
	jinja2.FileSystemLoader(TPL_FOLDER),	# second, regovar templates custom folder
	jinja2.FileSystemLoader(ASSET_FOLDER),	# third, regovar assets custom folder
])
app.jinja_loader = my_loader



@app.route('/')
def index():
	Parameter = Base.classes.parameter
	params = db_session.query(Parameter)
	return render_template('welcom.html', params=params)


# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.user


# 
# Authentication management =======================================================================
#
'''
@app.before_request
def before_request():
	# check authent on all request
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


	if request :
		print( "Endpoint : " + str(request))
	else:
		print("Endpoint : None")
    #if 'logged_in' not in session and request.endpoint != 'login':

'''
