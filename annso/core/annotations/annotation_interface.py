#!env/python3
# coding: utf-8
import ipdb

import os
import shutil
import json
import tarfile
import datetime
import time
import uuid
import subprocess
import requests





from core.framework import *
from core.model import *
from core.core import annso



class AnnotationInterface:
    """ All other annotation extensions needed by this one shall be listed here """
    dependencies = []

    """ By default the extension is disabled, it will be enabled at the __init__ if all requierements are fullfilled """
    disabled = True


    def __init__(self):
        """ 
            In the init all check must be done if requierement are well installed
        """
        if dependencies in annso.extensions
        pass



    def public_fields(self):
        return PirusFile.public_fields



    def total(self):
        return PirusFile.objects.count()