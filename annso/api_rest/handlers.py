#!env/python3
# coding: utf-8
import ipdb; 


import os
import json
import aiohttp
import aiohttp_jinja2
import datetime
import time


from aiohttp import web, MultiDict
from urllib.parse import parse_qsl

from config import *
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
        "success":      False, 
        "msg":          message, 
        "error_code":   code, 
        "error_url":    ERROR_ROOT_URL + code,
        "error_id":     error_id
    }
    return web.json_response(results)



def notify_all(src, msg):
    for ws in WebsocketHandler.socket_list:
        if src != ws[1]:
            ws[0].send_str(msg)







def process_generic_get(query_string, allowed_fields):
        # 1- retrieve query parameters
        get_params = MultiDict(parse_qsl(query_string))
        r_range  = get_params.get('range', "0-" + str(RANGE_DEFAULT))
        r_fields = get_params.get('fields', None)
        r_sort  = get_params.get('sort_by', None)
        r_order = get_params.get('sort_order', None)
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
            "hostname" : "annso.absolumentg.fr/v1",
            "templates" : annso.template.get(), # return by default last 10 templates
            "analysis" : annso.analysis.get(),  # return by default last 10 analyses
            "annotations_db" :     annso.annotation_db.get_databases(),
            "annotations_fields" : json.dumps(annso.annotation_db.get_fields()),
        }
        return data



    def get_config(self, request):
        return rest_success({})




    def get_db(self, request):
        return rest_success([])


 






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANNOTATION DATABASES HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnnotationDBHandler:
    def get_databases(self, request):
        """ 
            Return list of annotation databases and for each, available fields
        """
        return rest_success(annso.annotation_db.get_databases())

    def get_fields(self, request):
        """
            Return flat list of all fields with their meta data (description, database id, ...)
        """
        return rest_success(annso.annotation_db.get_fields())









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANALYSIS HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnalysisHandler:

    def get_analysis(self, request):
        analysis_id = request.match_info.get('analysis_id', -1)
        analysis = annso.analysis.get_from_id(analysis_id)
        if analysis is None:
            return rest_error("Unable to find the analysis with id=" + str(analysis_id))
        return rest_success(analysis)



    async def create_analysis(self, request):
        # 1- Retrieve data from request
        data = await request.json()
        name = data["name"]
        template_id = None # data["template_id"] # TODO
        # data["samples"] # TODO ?
        # data["attributes"] # TODO ?
        # Create the project 
        analysis, success = annso.analysis.create(name, template_id)
        if not success or analysis is None:
            return rest_error("Unable to create an analsis with provided information.")
        return rest_success(analysis)


    def get_setting(self, request):
        # 1- Retrieve data from request
        analysis_id = request.match_info.get('analysis_id', -1)

        try :
            settings = annso.analysis.get_setting(analysis_id)
        except Exception as err :
            return rest_error("Unable to get analsis settings with provided information. " + str(err))
        if settings is None : settings = {}
        return rest_success(settings)


    async def set_setting(self, request):
        # 1- Retrieve data from request
        analysis_id = request.match_info.get('analysis_id', -1)
        data = await request.json()
        try:
            annso.analysis.set_setting(analysis_id, data)
        except Exception as err :
            return rest_error("Error occured when trying to save settings for the analysis with id=" + str(analysis_id) + ". " + str(err))
        return rest_success(result) 

        

    async def filtering(self, request):
        # 1- Retrieve data from request
        data = await request.json()
        analysis_id = request.match_info.get('analysis_id', -1)
        filter_json = data["filter"] if "filter" in data else {}
        fields = data["fields"] if "fields" in data else None
        limit = data["limit"] if "limit" in data else 100
        offset = data["offset"] if "offset" in data else 0
        mode = data["mode"] if "mode" in data else "table"

        # 2- Check parameters
        if "mode" in data: mode = data["mode"]
        if limit<0 or limit > RANGE_MAX : limit = 100
        if offset<0 : offset = 0

        # 3- Execute filtering request
        # try :
        result = annso.filter.request(int(analysis_id), mode, filter_json, fields, int(limit), int(offset))
        # except Exception as err :
        #     return rest_error("Filtering error : " + str(err))
        return rest_success(result)







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# REPORT HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


class ReportHandler:

    async def get_omim_data(self, request):
        try:
            return rest_success(annso.report.get_omim_data(gene_name))
        except Exception as err:
            return rest_error("Unexpected error occured when trying to retrieve OMOM information for the gene : " + str(gene_name) + ". " + str(err))

    @aiohttp_jinja2.template('report.html')
    async def get_html_report(self, request):
        from core.report import get_ta_image, get_hbt_image, get_decipher_image, get_sp_image
        # 1- Retrieve data from request
        #data = await request.json()
        data = { "variants" : [1,212,342], "lang" : "EN-en"}

        # 2- Get report data thanks to the core
        gene = annso.get_report(data["variants"])

        # 3- Return html template
        return {
            "gene" : gene
        }




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# SAMPLE HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SampleHandler:
    def get_samples(self, request):
        # Generic processing of the get query
        fields, query, order, offset, limit = process_generic_get(request.query_string, annso.sample.public_fields())
        # Get range meta data
        range_data = {
            "range_offset" : offset,
            "range_limit"  : limit,
            "range_total"  : annso.sample.total(),
            "range_max"    : RANGE_MAX,
        }
        # Return result of the query for PirusFile 
        return rest_success(annso.sample.get(fields, query, order, offset, limit), range_data)

    def get_sample(self, request):
        # 1- Retrieve request parameters
        sid = request.match_info.get('sample_id', None)
        if sid is None:
            return rest_error("No valid sample id provided")
        sample = annso.sample.get_from_id(sid)
        if sample is None:
            return rest_error("No sample found with id="+str(sid))
        return rest_success(sample)


    def get_details(self, request):
        # 1- Retrieve request parameters
        db_name = request.match_info.get('db_name', None)
        if db_name is None:
            return rest_error("No database name provided")

        return rest_success({"database" : db_name})



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
# VARIANT HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VariantHandler:
    def get_variants(self, request):
        # Generic processing of the get query
        fields, query, order, offset, limit = process_generic_get(request.query_string, annso.variant.public_fields())
        # Get range meta data
        range_data = {
            "range_offset" : offset,
            "range_limit"  : limit,
            "range_total"  : annso.variant.total(),
            "range_max"    : RANGE_MAX,
        }
        # Return result of the query for PirusFile 
        return rest_success(annso.variant.get(fields, query, order, offset, limit), range_data)



    def get_details(self, request):
        # 1- Retrieve request parameters
        db_name = request.match_info.get('db_name', None)
        if db_name is None:
            return rest_error("No database name provided")

        return rest_success({"database" : db_name})













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
