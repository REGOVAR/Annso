#!env/python3
# coding: utf-8


from flask_script import Manager
from regovar.application import app


manager = Manager(app, description="manage regovar application")
#manager.add_command("dbtools", db.manager)

# @manager.command
# def hello():
# 	'''Says hello'''
# 	print ("hello")



if __name__ == "__main__":
    manager.run() 




