#!env/python3
# coding: utf-8


from flask_script import Manager
from regovar.application import app


manager = Manager(app, description="manage regovar application")
#manager.add_command("runtests", db.manager)




if __name__ == "__main__":
    manager.run() 




