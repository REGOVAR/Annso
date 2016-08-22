


@app.route('/users/')
def get_users():
	''' route : /users/ '''
	return jsonify({"results":[u.export_data() for u in User.objects.all()]})


@app.route('/users/<user_id>')
def get_user(user_id):
	return jsonify({"results": User.objects.get(pk=user_id).export_data()})

@app.route('/users/', methods=['POST'])
def new_user():
	user = User()
	user.import_data(request.json)
	user.objects.add(image)
	user.save()
	return jsonify({"results": user.export_data()})

@app.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
	image = Image.objects.get(pk=user_id)
	image.import_data(request.json)
	image.save()
	return {}



@app.route('/users/login', methods=['GET'])
def login_user():
	print ("LOGIN")
	data = request.get_json(force=False)
	login    = data.get("login")
	password = data.get("password")

	user = User.objects(login=login).first()

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
