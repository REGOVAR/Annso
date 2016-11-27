#!env/python3
# coding: utf-8
import ipdb; 


import os
import json
import aiohttp

import aiohttp_jinja2
import tarfile
import datetime
import time
import uuid
import subprocess


from aiohttp import web, MultiDict
from urllib.parse import parse_qsl


from core import *
from api_rest.tus import tus_manager






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# COMMON TOOLS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def rest_success(response_data=None, pagination_data=None):
    """ 
        Build the REST success response that will encapsulate the given data (in python dictionary format)
        :param response_data:   The data to wrap in the JSON success response
        :param pagination_data: The data regarding the pagination
    """
    if response_data is None:
        results = {"success":True}
    else:
        results = {"success":True, "data":response_data}
    if pagination_data is not None:
        results.update(pagination_data)
    return web.json_response(results)



def rest_error(message:str="Unknow", code:str="0", error_id:str=""):
    """ 
        Build the REST error response
        :param message:         The short "friendly user" error message
        :param code:            The code of the error type
        :param error_id:        The id of the error, to return to the end-user. 
                                This code will allow admins to find in logs where exactly this error occure
    """
    results = {
        "success":              False, 
        "msg":                  message, 
        "error_code":   code, 
        "error_url":    ERROR_ROOT_URL + code,
        "error_id":             error_id
    }
    return web.json_response(results)



def notify_all(src, msg):
    for ws in WebsocketHandler.socket_list:
        if src != ws[1]:
            ws[0].send_str(msg)

# Give to the core the delegate to call to notify all via websockets
pirus.set_notify_all(notify_all)





def process_generic_get(query_string, allowed_fields):
        # 1- retrieve query parameters
        get_params = MultiDict(parse_qsl(query_string))
        r_range  = get_params.get('range', "0-" + str(RANGE_DEFAULT))
        r_fields = get_params.get('fields', None)
        r_order  = get_params.get('order_by', None)
        r_sort   = get_params.get('order_sort', None)
        r_filter = get_params.get('filter', None)

        # 2- fields to extract
        fields = allowed_fields
        if r_fields is not None:
            fields = []
            for f in r_fields.split(','):
                f = f.strip().lower()
                if f in allowed_fields:
                    fields.append(f)
        if len(fields) == 0:
            return rest_error("No valid fields provided : " + get_params.get('fields'))

        # 3- Build json query for mongoengine
        query = {}
        if r_filter is not None:
            query = {"$or" : []}
            for k in fields:
                query["$or"].append({k : {'$regex': r_filter}})

        # 4- Order
        order = ['-create_date', "name"]
        if r_sort is not None and r_order is not None:
            r_sort = r_sort.split(',')
            r_order = r_order.split(',')
            if len(r_sort) == len(r_order):
                order = []
                for i in range(0, len(r_sort)):
                    f = r_sort[i].strip().lower()
                    if f in allowed_fields:
                        if r_order[i] == "desc":
                            f = "-" + f
                        order.append(f)
        order = tuple(order)

        # 5- limit
        r_range = r_range.split("-")
        offset=0
        limit=RANGE_DEFAULT
        try:
            offset = int(r_range[0])
            limit = int(r_range[1])
        except:
            return rest_error("No valid range provided : " + get_params.get('range') )

        # 6- Return processed data
        return fields, query, order, offset, limit










# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MISC HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class WebsiteHandler:
    def __init__(self):
        pass

    @aiohttp_jinja2.template('home.html')
    def home(self, request):
        data = {
            "pipes_inprogress" : [p for p in pirus.pipelines.get(None, None, ['-name']) if p["status"] in ["UPLOADING", "PAUSE", "INSTALLING"]],
            "files_all"        :  pirus.files.get(None, None, ['-create_date']),
            "files_inprogress" : [f for f in pirus.files.get(None, None, ['-create_date']) if f["status"] in ["UPLOADING", "PAUSE"]],
            "pipes"            : pirus.pipelines.get(None, None, ['-name'], None, None, 2),
            "runs_done"        : [r for r in pirus.runs.get(None, None, ['-start']) if r["status"] in ["ERROR", "DONE", "CANCELED"]],
            "runs_inprogress"  : [r for r in pirus.runs.get(None, None, ['-start']) if r["status"] in ["WAITING", "PAUSE", "INITIALIZING", "RUNNING", "FINISHING"]], 
            "hostname"         : HOSTNAME
        }
        for f in data["files_all"]: 
            f.update({"size" : humansize(f["size"])})

        for f in data["files_inprogress"]: 
            f.update({"size" : humansize(f["size"]), "upload_offset": humansize(f["upload_offset"]) , "progress" : round(int(f["upload_offset"]) / int(f["size"]) * 100)})

        for r in data["runs_done"]:
            p = round(int(r["progress"]["value"]) / max(1, (int(r["progress"]["max"]) - int(r["progress"]["min"]))) * 100)
            r.update({"%" : p})

        for r in data["runs_inprogress"]:
            p = round(int(r["progress"]["value"]) / max(1, (int(r["progress"]["max"]) - int(r["progress"]["min"]))) * 100)
            r.update({"%" : p})

        data.update({"total_inprogress" : len(data["files_inprogress"]) + len(data["pipes_inprogress"]) + len(data["runs_inprogress"])})
        return data



    def get_config(self, request):
        return rest_success({
            "host" : HOST,
            "port" : PORT,
            "version" : VERSION,
            "base_url" : "http://" + HOSTNAME,
            "max_parallel_run " : LXD_MAX,
            "run_config " : LXD_HDW_CONF
        })




    def get_db(self, request):
        return rest_success([f for f in os.listdir(DATABASES_DIR) if os.path.isfile(os.path.join(DATABASES_DIR, f))])


 








# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# REST FILE API HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class FileHandler:

    def get(self, request):
        # Generic processing of the get query
        fields, query, order, offset, limit = process_generic_get(request.query_string, pirus.files.public_fields())
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        # Get range meta data
        range_data = {
            "range_offset" : offset,
            "range_limit"  : limit,
            "range_total"  : pirus.files.total(),
            "range_max"    : RANGE_MAX,
        }
        # Return result of the query for PirusFile 
        return rest_success(pirus.files.get(fields, query, order, offset, limit, sub_level_loading), range_data)




    def edit_infos(self, request):
        # TODO : implement PUT to edit file metadata (and remove the obsolete  "simple post" replaced by TUS upload )
        return rest_error("Not yet implemented")
        


    # UPLOAD is now manage using TUS.IO protocol
    # async def upload_simple(self, request):
    #     """
    #         "Simple" upload (synchrone and not resumable)
    #     """
    #     name = str(uuid.uuid4())
    #     path = os.path.join(FILES_DIR, name)
    #     plog.info('I: Start file uploading : ' + path)
    #     # 1- Retrieve file from post request
    #     data = await request.post()
    #     uploadFile = data['uploadFile']
    #     comments = None
    #     tags = None
    #     if "comments" in data.keys():
    #         comments = data['comments'].strip()
    #     if "tags" in data.keys():
    #         tmps = data['tags'].split(',')
    #         tags = []
    #         for i in tmps:
    #             i2 = i.strip()
    #             if i2 != "":
    #                 tags.append(i2)
    #     # 2- save file on the server 
    #     try:
    #         with open(path, 'bw+') as f:
    #             f.write(uploadFile.file.read())
    #     except:
    #         # TODO : manage error
    #         raise PirusException("Bad pirus pipeline format : Manifest file corrupted.")
    #     plog.info('I: File uploading done : ' + path)
    #     # 3- save file on the database
    #     pirusfile = pirus.files.register(uploadFile.filename, path, {
    #         "tags"          : tags,
    #         "comments"      : comments
    #     })
    #     return rest_success(pirusfile)



    def delete(self, request):
        file_id = request.match_info.get('file_id', "")
        try:
            return rest_success(pirus.files.delete(file_id))
        except Exception as err:
            return rest_error("Error occured : " + err)



    def get_details(self, request):
        file_id = request.match_info.get('file_id', -1)
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        try:
            return rest_success(pirus.files.get_from_id(file_id))
        except PirusException as err:
            return rest_error("Error occured : " + err)




    # Resumable download implement the TUS.IO protocol.
    def tus_config(self, request):
        return tus_manager.options(request)

    def tus_upload_init(self, request):
        return tus_manager.creation(request)

    def tus_upload_resume(self, request):
        return tus_manager.resume(request)

    async def tus_upload_chunk(self, request):
        result = await tus_manager.patch(request)
        return result

    def tus_upload_delete(self, request):
        return tus_manager.delete_file(request)







    async def dl_file(self, request):        
        # 1- Retrieve request parameters
        id = request.match_info.get('file_id', -1)
        pirus_file = pirus.files.get_from_id(id, 0, ["name", "path", "id"])
        if pirus_file == None:
            return rest_error("File with id " + str(id) + "doesn't exits.")
        file = None
        if os.path.isfile(pirus_file["path"]):
            with open(pirus_file["path"], 'br') as content_file:
                file = content_file.read()
        return web.Response(
            headers=MultiDict({'Content-Disposition': 'Attachment; filename='+pirus_file["name"]}),
            body=file
        )

    async def dl_pipe_file(self, request):
        # 1- Retrieve request parameters
        pipe_id = request.match_info.get('pipe_id', -1)
        filename = request.match_info.get('filename', None)
        pipeline = pirus.pipelines.get_from_id(pipe_id, 0, ["root_path"])
        if pipeline == None:
            return rest_error("No pipeline with id " + str(pipe_id))
        if filename == None:
            return rest_error("No filename provided")
        path = os.path.join(pipeline["root_path"], filename)
        file = None
        if os.path.isfile(path):
            with open(path, 'br') as content_file:
                file = content_file.read()
        return web.Response(
            headers=MultiDict({'Content-Disposition': 'Attachment; filename='+ filename}),
            body=file
        )

    async def dl_run_file(self, request):
        return rest_success({})











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# REST PIPELINE API HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class PipelineHandler:
    def __init__(self):
        pass

    def get(self, request):
        fields, query, order, offset, limit = process_generic_get(request.query_string, pirus.pipelines.public_fields())
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        # Get range meta data
        range_data = {
            "range_offset" : offset,
            "range_limit"  : limit,
            "range_total"  : pirus.pipelines.total(),
            "range_max"    : RANGE_MAX,
        }
        return rest_success(pirus.pipelines.get(fields, query, order, offset, limit, sub_level_loading), range_data)




    def delete(self, request):
        pipe_id = request.match_info.get('pipe_id', -1)
        try:
            pirus.pipelines.delete(pipe_id)
        except Exception as error:
            # TODO : manage error
            return rest_error("Unable to delete the pipeline with id " + str(pipe_id) + ". " + error.msg)
        return rest_success("Pipeline " + str(pipe_id) + " deleted.")


    def get_details(self, request):
        pipe_id = request.match_info.get('pipe_id', -1)
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        pipe = pirus.pipelines.get_from_id(pipe_id)
        if pipe == None:
            return rest_error("No pipeline with id " + str(pipe_id))
        print ("PipelineHandler.get_details('" + str(pipe_id) + "', sublvl=" + str(sub_level_loading) + ")")
        return rest_success(pipe.export_client_data(sub_level_loading))


    # Resumable download implement the TUS.IO protocol.
    def tus_config(self, request):
        return tus_manager.options(request)

    def tus_upload_init(self, request):
        return tus_manager.creation(request)

    def tus_upload_resume(self, request):
        return tus_manager.resume(request)

    async def tus_upload_chunk(self, request):
        result = await tus_manager.patch(request)
        return result

    def tus_upload_delete(self, request):
        return tus_manager.delete_file(request)











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# REST RUN API HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class RunHandler:
    def __init__(self):
        pass

    def get(self, request):
        fields, query, order, offset, limit = process_generic_get(request.query_string, pirus.runs.public_fields())
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        # Get range meta data
        range_data = {
            "range_offset" : offset,
            "range_limit"  : limit,
            "range_total"  : pirus.runs.total(),
            "range_max"    : RANGE_MAX,
        }
        return rest_success(pirus.runs.get(fields, query, order, offset, limit, sub_level_loading), range_data)


    def delete(self, request):
        run_id = request.match_info.get('run_id', "")
        try:
            return rest_success(pirus.runs.delete(pipe_id))
        except Exception as error:
            # TODO : manage error
            return rest_error("Unable to delete the runs with id " + str(pipe_id) + ". " + error.msg)


    def get_details(self, request):
        run_id = request.match_info.get('run_id', -1)
        sub_level_loading = int(MultiDict(parse_qsl(request.query_string)).get('sublvl', 0))
        run = pirus.runs.get_from_id(run_id)
        if run == None:
            return rest_error("Unable to find the run with id " + str(run_id))
        return rest_success(run.export_client_data(sub_level_loading))


    def download_file(self, run_id, filename, location=RUNS_DIR):
        run = pirus.runs.get_from_id(run_id)
        if run == None:
            return rest_error("No run with id " + str(run_id))
        path = os.path.join(location, run.lxd_container, filename)

        if not os.path.exists(path):
            return rest_error("File not found. " + filename + " doesn't exists for the run " + str(run_id))
        content = ""
        if os.path.isfile(path):
            with open(path, 'br') as content_file:
                file = content_file.read()
        return web.Response(
            headers=MultiDict({'Content-Disposition': 'Attachment; filename='+filename}),
            body=file
        )

    def get_olog(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/out.log")

    def get_elog(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/err.log")

    def get_plog(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/pirus.log")

    def get_olog_tail(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/out.log")

    def get_elog_tail(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/err.log")

    def get_plog_tail(self, request):
        run_id = request.match_info.get('run_id', -1)
        return self.download_file(run_id, "logs/pirus.log")

    def get_io(self, request):
        run_id  = request.match_info.get('run_id',  -1)
        if run_id == -1:
            return rest_error("Id not found")
        run = pirus.runs.get_from_id(run_id)
        if run == None:
            return rest_error("Unable to find the run with id " + str(run_id))
        result={
            "inputs" : pirus.files.get_from_ids([f["id"] for f in run["inputs"]]),
            "outputs": pirus.files.get_from_ids([f["id"] for f in run["outputs"]])
        }
        return rest_success(result)

    def get_file(self, request):
        run_id  = request.match_info.get('run_id',  -1)
        filename = request.match_info.get('filename', "")
        return self.download_file(run_id, filename)


    async def update_status(self, request):
        # 1- Retrieve data from request
        print("Handler.update_status", end="")
        data = await request.json()
        run_id = request.match_info.get('run_id', -1)
        try:
            print(" => pirus.runs.edit : ", data)
            run = pirus.runs.edit(run_id, data)
        except Exception as error:
            return rest_error("Unable to update information for the runs with id " + str(run_id) + ". " + error.msg)

        return rest_success(run)




    async def post(self, request):
        # 1- Retrieve data from request
        data = await request.json()
        pipe_id = data["pipeline_id"]
        config = data["config"]
        inputs = data["inputs"]
        # Create the run 
        run = pirus.runs.create(pipe_id, config, inputs)
        if run is None:
            return error
        # start run
        pirus.runs.start(run["id"])
        return rest_success(run)


    def get_pause(self, request):
        run_id  = request.match_info.get('run_id',  -1)
        if run_id == -1:
            return rest_error("Id not found")
        result, run = pirus.runs.pause(run_id)
        if result:
            return rest_success(run)
        return rest_error("Unable to pause the run " + run["id"])


    def get_play(self, request):
        run_id  = request.match_info.get('run_id', -1)
        if run_id == -1:
            return rest_error("Id not found")
        result, run = pirus.runs.play(run_id)
        if result:
            return rest_success(run)
        return rest_error("Unable to restart the run " + run["id"])


    def get_stop(self, request):
        run_id  = request.match_info.get('run_id',  -1)
        if run_id == -1:
            return rest_error("Id not found")
        result, run = pirus.runs.stop(run_id)
        if result:
            return rest_success(run.export_client_data())
        return rest_error("Unable to stop the run " + str(run_id))


    def get_monitoring(self, request):
        run_id  = request.match_info.get('run_id',  -1)
        try:
            result = pirus.runs.monitoring(run_id)
        except Exception as error:
            return rest_error("Unable to retrieve monitoring info for the runs with id " + str(run_id) + ". " + error.msg)
        return rest_success(result)











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# WEBSOCKET HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class WebsocketHandler:
    socket_list = []


    async def get(self, request):
        peername = request.transport.get_extra_info('peername')
        if peername is not None:
            host, port = peername

        ws_id = "{}:{}".format(host, port)
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        print('WS connection open by', ws_id)
        WebsocketHandler.socket_list.append((ws, ws_id))
        msg = '{"action":"online_user", "data" : [' + ','.join(['"' + _ws[1] + '"' for _ws in WebsocketHandler.socket_list]) + ']}'
        notify_all(None, msg)

        try:
            async for msg in ws:
                if msg.tp == aiohttp.MsgType.text:
                    if msg.data == 'close':
                        print ('CLOSE MESSAGE RECEIVED')
                        await ws.close()
                    else:
                        # Analyse message sent by client and send response if needed
                        data = msg.json()
                        if data["action"] == "user_info":
                            print("WebsocketHandler", data["action"])
                            pass
                        elif msg.tp == aiohttp.MsgType.error:
                            print('ws connection closed with exception %s' % ws.exception())
        finally:
            print('WS connection closed for', ws_id)
            WebsocketHandler.socket_list.remove((ws, ws_id))

        return ws











async def on_shutdown(app):
    print("SHUTDOWN SERVER... CLOSE ALL")
    for ws in WebsocketHandler.socket_list:
        await ws[0].close(code=999, message='Server shutdown')
