#!env/python3
# coding: utf-8
import sys
from sqlalchemy.orm import Session


from regovar.config import *
from regovar.common import *
from regovar.application import app

from regovar.rest_api_v1.rest_common import *
from regovar.application import Base, db_engine



# Project resource :
# Project
# {
#     "id" :                  56
#     "name" :                "X File"
#     "comments" :            "Top secret project"
#     "parent_id" :           NULL
#     "data" :                { "key" : "value" }

#	  "children" :			  *computed fields* => Array of Project / Analysis
#	  "parent" :			  *computed fields* => Resource Project
# }


# Global variables
fields_allowed 		= ['id', 'name', 'comments', 'parent_id', 'data']
fields_default 		= ['id', 'name', 'parent_id']
filter_fields  		= ['name', 'parent_id']
ordering_fields  	= ['id', 'name', 'parent_id']
ordering_default 	= ['name']


""" This globale variable to manipulate project database model object (SQLAlchemy) """
Project = Base.classes.project








@app.route('/projects/')
def get_projects():
	''' 
		Return list of project
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
	sql = sql_select + " FROM \"project\" " + sql_where + sql_ordering + sql_limit
	result = db_engine.execute(sql)
	order = 0
	if (result):
		d = {}
		for row in result:
			d[order] = fmk_row2dict(row)
			order += 1
	return fmk_rest_success(d)





@app.route('/projects/<project_id>')
def get_project(project_id):
	"""
		Return the project with the given id if exists. Otherwise return an error.
	"""
	result = db_engine.execute("SELECT * FROM \"project\" WHERE id=%s" % project_id).first()

	if result is None:
		logid = err("rest_api_v1.projects.get_project('" + project_id + "') : no project with this id found")
		return fmk_rest_error(ERRC_00001, "00001", logid)
	return fmk_rest_success(fmk_row2dict(result))








@app.route('/projects/', methods=['POST'])
def new_project():
	# Retrieve POST data
	data = dict(request.form)

	# TODO check that post data exists
	if data is None :
		err("rest_api_v1.projects.new_project() : no POST data found")
		return fmk_rest_error(ERRC_00003, "00003")

	name = data.get('name', [None])[0]
	parent_id = data.get('parent_id' [None])[0]

	if not name:
		err("rest_api_v1.projects.new_project() : provided 'name' data is empty")
		return fmk_rest_error(ERRC_00003 + " : email", "00003")

	# Create new project
	project = None
	try:
		db_session = Session(db_engine)

		project = Project()
		project.name		= name
		project.parent_id 	= parent_id
		project.comments 	= data.get('comments', 	[None])[0]
		project.data 		= data.get('data', 		[None])[0]

		# Register in database
		db_session.add(project)
		db_session.commit()
	except:
		project = None
		err("rest_api_v1.projects.new_project() : Failed to create a project with provided data : " + str(data))
		return fmk_rest_error(ERRC_00002, "00002")
		
	# Return id of the new project
	return fmk_rest_success({"id":project.id})

	

	



@app.route('/projects/<project_id>', methods=['PUT'])
def edit_project(project_id):
	# Retrieve PUT data
	data = dict(request.form)

	# check that post data exists
	if data is None :
		logid = err("rest_api_v1.projects.edit_project() : no PUT data found")
		return fmk_rest_error(ERRC_00003, "00003", logid)

	pid = data.get('pid', [None])[0]	

	if not pid:
		logid = err("rest_api_v1.projects.edit_project() : provided 'pid' is empty")
		return fmk_rest_error(ERRC_00003 + " : pid", "00003", logid)

	# Edit project
	db_session = Session(db_engine)
	project = db_session.query(project).get(int(pid))


	# Check that project exists
	if not project:
		logid = err("rest_api_v1.projects.edit_project() : project doesn't exists (pid="+pid+")")
		return fmk_rest_error(ERRC_00001 + " : pid", "00001", logid)


	

	try:
		project.name 		= data.get('name', 		[None])[0] or project.name
		project.comments 	= data.get('comments', 	[None])[0] or project.comments
		project.parent_id 	= data.get('parent_id', [None])[0] or project.parent_id
		project.data 		= data.get('data', 		[None])[0] or project.data
		

		# Register in database
		db_session.add(project)
		db_session.commit()
	except:
		project = None
		logid = err("rest_api_v1.projects.edit_project() : Failed to update a project with provided data : " + str(data))
		return fmk_rest_error(ERRC_00002, "00002", logid)

		
	# Return id of the new project
	return fmk_rest_success()















