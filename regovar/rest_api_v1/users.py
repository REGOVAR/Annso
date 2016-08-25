#!env/python3
# coding: utf-8
from regovar.config import *
from regovar.common import *
from regovar.application import app

from regovar.rest_api_v1.rest_common import *



@app.route('/users/')
def get_users():
	''' route : /users/ '''
	return '/users/'


@app.route('/users/<user_id>')
def get_user(user_id):
	return jsonify({"results": User.objects.get(pk=user_id).export_data()})

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
