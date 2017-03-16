#!env/python3
# coding: utf-8
import os
import datetime
import uuid
import sqlalchemy
import asyncio
import multiprocessing as mp


from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import config as C
import ipdb




def init_pg(user, password, host, port, db):
    '''Returns a connection and a metadata object'''
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    return con





# =====================================================================================================================
# INTERNAL
# =====================================================================================================================



# Connect and map the engine to the database
Base = automap_base()
__db_engine = init_pg(C.DATABASE_USER, C.DATABASE_PWD, C.DATABASE_HOST, C.DATABASE_PORT, C.DATABASE_NAME)
Base.prepare(__db_engine, reflect=True)
Base.metadata.create_all(__db_engine)
Session = sessionmaker(bind=__db_engine)
__db_session = Session()
__db_pool = mp.Pool()
__async_job_id = 0
__async_jobs = {}



def private_execute_async(async_job_id, query):
    """
        Internal method used to execute query asynchronously
    """
    # As execution done in another thread, use also another db session to avoid thread conflicts
    session = Session()
    result = None
    try:
        result = session.execute(query)
        session.commit()
        session.commit() # Need a second commit to force session to commit :/ ... strange behavior when we execute(raw_sql) instead of using sqlalchemy's objects as query
        session.close()
    except Exception as err:
        ipdb.set_trace()
        log(err)
        session.close()
        return (async_job_id, err)
    return (async_job_id, result)


def private_execute_callback(result):
    """
        Internal callback method for asynch query execution. 

    """
    job_id = result[0]
    result = result[1]
    # Storing result in dictionary
    __async_jobs[job_id]['result'] = result

    # Call callback if defined
    if __async_jobs[job_id]['callback']:
        __async_jobs[job_id]['callback'](job_id, result)

    # Delete job 
    del __async_jobs[async_job_id]







# =====================================================================================================================
# MODEL METHODS
# =====================================================================================================================


def get_or_create(session, model, defaults=None, **kwargs):
    if defaults is None:
        defaults = {}
    try:
        query = session.query(model).filter_by(**kwargs)

        instance = query.first()

        if instance:
            return instance, False
        else:
            session.begin(nested=True)
            try:
                params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
                params.update(defaults)
                instance = model(**params)

                session.add(instance)
                session.commit()

                return instance, True
            except IntegrityError as e:
                session.rollback()
                instance = query.one()

                return instance, False
    except Exception as e:
        raise e


def session():
    """
        Return the current pgsql session (SQLAlchemy)
    """
    return __db_session


def execute(query):
    """
        Synchrone execution of the query
    """
    result = None
    try:
        result = __db_session.execute(query)
        __db_session.commit()
        __db_session.commit() # Need a second commit to force session to commit :/ ... strange behavior when we execute(raw_sql) instead of using sqlalchemy's objects as query
    except Exception as err:
        ipdb.set_trace()
        err(err)
    return result


def execute_bw(query, callback=None):
    """
        execute in background worker:
        Asynchrone execution of the query in an other thread. An optional callback method that take 2 arguments (job_id, query_result) can be set.
        This method return a job_id for this request that allow you to cancel it if needed
    """
    global __async_job_id, __async_jobs, __db_pool
    __async_job_id += 1
    t = __db_pool.apply_async(private_execute_async, args = (__async_job_id, query,), callback=private_execute_callback)
    __async_jobs[__async_job_id] = {"task" : t, "callback": callback, "query" : query, "start": datetime.datetime.now}
    return __async_job_id
        


async def execute_aio(query):
    """
        execute as coroutine
        Asynchrone execution of the query as coroutine
    """

    # Execute the query in another thread via coroutine
    loop = asyncio.get_event_loop()
    futur = loop.run_in_executor(None, private_execute_async, None, query)


    # Aio wait the end of the async task to return result
    result = await futur
    return result[1]


def cancel(async_job_id):
    """
        Cancel an asynch job running in the threads pool
    """
    if async_job_id in __async_jobs.keys():
        __async_jobs.keys[async_job_id]["task"].terminate()
        __async_jobs.keys[async_job_id]["task"].join()
        log("Model async query (id:{}) canceled".format(async_job_id))
    else:
        log("Model unable to cancel async query (id:{}) because it doesn't exists".format(async_job_id))





# =====================================================================================================================
# MODEL DEFINITION - Build from the database (see sql scripts used to generate the database)
# =====================================================================================================================
SampleVariant = Base.classes.sample_variant_hg19
Attribute = Base.classes.attribute
AnnotationDatabase = Base.classes.annotation_database
AnnotationField = Base.classes.annotation_field



# =====================================================================================================================
# ANALYSIS
# =====================================================================================================================


def analysis_from_id(analysis_id):
    """
        Retrieve File with the provided id in the database
    """
    return __db_session.query(Analysis).filter_by(id=analysis_id).first()


def analysis_to_json(self, fields=None):
    """
        export the file into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Analysis.public_fields
    for f in fields:
        if f == "creation_date" or f == "update_date":
            result.update({f: eval("self." + f + ".ctime()")})
        else:
            result.update({f: eval("self." + f)})
    return result


Analysis = Base.classes.analysis
Analysis.public_fields = ["id", "name", "template_id", "creation_date", "update_date", "settings"]
Analysis.from_id = analysis_from_id
Analysis.to_json = analysis_to_json


# =====================================================================================================================
# TEMPLATE
# =====================================================================================================================


def template_from_id(template_id):
    """
        Retrieve Template with the provided id in the database
    """
    return __db_session.query(Template).filter_by(id=template_id).first()


Template = Base.classes.template
Template.public_fields = ["id", "name", "author", "description", "version", "creation_date", "update_date"]
Template.from_id = template_from_id


# =====================================================================================================================
# SAMPLE
# =====================================================================================================================


def sample_from_id(sample_id):
    """
        Retrieve Sample with the provided id in the database
    """
    return __db_session.query(Sample).filter_by(id=sample_id).first()


def sample_to_json(self, fields=None):
    """
        export the sample into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Sample.public_fields
    for f in fields:
        result.update({f: eval("self." + f)})
    return result


Sample = Base.classes.sample
Sample.public_fields = ["id", "name", "comments", "is_mosaic"]
Sample.from_id = sample_from_id
Sample.to_json = sample_to_json


# =====================================================================================================================
# Variant
# =====================================================================================================================


def variant_from_id(reference_id, variant_id):
    """
        Retrieve Sample with the provided id in the database
    """
    return __db_session.query(Variant).filter_by(id=variant_id).first()


Variant = Base.classes.variant_hg19
Variant.from_id = variant_from_id


# =====================================================================================================================
# FILE
# =====================================================================================================================


def file_from_id(file_id):
    """
        Retrieve File with the provided id in the database
    """
    return __db_session.query(File).filter_by(id=file_id).first()


def new_file_from_tus(filename, file_size):
    """
        Create a new File object (and entry in the database) with initial data for an upload with TUS protocol
    """
    def get_extension(filename):
        f = os.path.splitext(filename.strip().lower())
        t = f[1][1:]
        if t == "gz":
            return get_extension(f[0]) + f[1]
        return t
    global __db_session
    file = File()
    file.filename = filename
    file.type = get_extension(filename)
    file.path = os.path.join(C.TEMP_DIR, str(uuid.uuid4()))
    file.size = int(file_size)
    file.upload_offset = 0
    file.import_date = datetime.datetime.now()
    __db_session.add(file)
    __db_session.commit()
    return file


File = Base.classes.file
File.public_fields = ["id", "filename", "upload_offset", "size", "type", "import_date"]
File.new_from_tus = new_file_from_tus
File.from_id = file_from_id


# =====================================================================================================================
# FILTER
# =====================================================================================================================


def filter_from_id(filter_id):
    """
        Retrieve Filter with the provided id in the database
    """
    return __db_session.query(Filter).filter_by(id=filter_id).first()


def filter_to_json(self, fields=None):
    """
        export the filter into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Filter.public_fields
    for f in fields:
        result.update({f: eval("self." + f)})
    return result


Filter = Base.classes.filter
Filter.public_fields = ["id", "analysis_id", "name", "filter", "description"]
Filter.from_id = filter_from_id
Filter.to_json = filter_to_json
