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
from api_rest.tus import *








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









def process_generic_get(query_string, allowed_fields):
        # 1- retrieve query parameters
        get_params = MultiDict(parse_qsl(query_string))
        r_range    = get_params.get('range', "0-" + str(RANGE_DEFAULT))
        r_fields   = get_params.get('fields', None)
        r_sort     = get_params.get('sort_by', None)
        r_order    = get_params.get('sort_order', None)
        r_filter   = get_params.get('filter', None)

        # 2- fields to extract
        fields = allowed_fields
        if r_fields is not None:
            fields = []
            for f in r_fields.split(','):
                f = f.strip().lower()
                if f in allowed_fields:
                    fields.append(f)
        if len(fields) == 0:
            return rest_error("No valid fields provided: " + get_params.get('fields'))

        # 3- Build json query for mongoengine
        query = {}
        if r_filter is not None:
            query = {"$or": []}
            for k in fields:
                query["$or"].append({k: {'$regex': r_filter}})

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
            return rest_error("No valid range provided: " + get_params.get('range') )

        # 6- Return processed data
        return fields, query, order, offset, limit




def notify_all(data):
    msg = json.dumps(data)
    if 'msg' not in data.keys() or data['msg'] != 'hello':
        log ("API_rest Notify All: {0}".format(msg))
    for ws in WebsocketHandler.socket_list:
        ws[0].send_str(msg)

# Give to the core the delegate to call to notify all via websockets
annso.notify_all = notify_all






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MISC HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class WebsiteHandler:
    def __init__(self):
        pass

    @aiohttp_jinja2.template('home.html')
    def home(self, request):
        data = {
            "hostname": HOST_P,
            "templates": [], # return by default last 10 templates
            "analysis": annso.analysis.get(),  # return by default last 10 analyses
            "annotations_db_ref"    : annso.annotation_db.ref_list,
            "annotations_fields": json.dumps(annso.annotation_db.get_fields()),
            "export_modules": [annso.export_modules[m]['info'] for m in annso.export_modules], 
            "import_modules": [annso.import_modules[m]['info'] for m in annso.import_modules], 
            "report_modules": [annso.report_modules[m]['info'] for m in annso.report_modules], 
        }

        return data



    def get_config(self, request):
        return rest_success({
            "host": HOST_P,
            "pagination_default_range": RANGE_DEFAULT,
            "pagination_max_range": RANGE_MAX,
            "export_modules": annso.export_modules, 
            "import_modules": annso.import_modules,
            "report_modules": annso.report_modules
            })




    def get_db(self, request):
        return rest_success([])


 






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANNOTATION DATABASES HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnnotationDBHandler:
    def get_referencials(self, request):
        """ 
            Return list of genom's referencials supported
        """
        return rest_success(annso.annotation_db.ref_list)


    def get_ref_db(self, request):
        """ 
            Return list of all annotation's databases and, for each, the list of availables versions and the list of their fields for the latest version
        """
        ref_id = request.match_info.get('ref_id', None)
        if ref_id is None or ref_id not in annso.annotation_db.ref_list.keys():
            ref_id = DEFAULT_REFERENCIAL_ID 

        result = { "ref_id": ref_id, "ref_name": annso.annotation_db.ref_list[ref_id], "db": []}

        for db_name in annso.annotation_db.db_list[ref_id]["order"]:
            db_data = annso.annotation_db.db_list[ref_id]['db'][db_name]
            db_data.update({"selected": next(iter(db_data['versions'].keys()))})
            db_data['fields'] = []
            for fuid in annso.annotation_db.db_map[db_data['versions'][db_data['selected']]]['fields']:
                db_data['fields'].append(annso.annotation_db.fields_map[fuid])

            result["db"].append(db_data)
        #annso.annotation_db.db_list[2]['refGene']['versions'][max(annso.annotation_db.db_list[2]['refGene']['versions'].keys())]

        return rest_success(result)


    def get_database(self, request):
        """
            Return the database description and the list of available versions
        """
        db_id = request.match_info.get('db_id', -1)
        return rest_success(annso.annotation_db.db_map[db_id])








    






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANALYSIS HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VariantHandler:

    def get_variant(self, request):
        """
            Return all data available for the requested variant in the context of the analysis
        """
        reference_id = request.match_info.get('ref_id', -1)
        variant_id = request.match_info.get('variant_id', -1)
        analysis_id = request.match_info.get('analysis_id', None)

        variant = annso.variant.get(reference_id, variant_id, analysis_id)
        if variant is None:
            return rest_error('Variant not found')
        return rest_success(variant)
















# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANALYSIS HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AnalysisHandler:

    def get_analysis(self, request):
        """
            Return all data about the analysis with the provided id (analysis metadata: name, settings, template data, samples used, filters, ... )
        """
        analysis_id = request.match_info.get('analysis_id', -1)
        analysis = annso.analysis.load(analysis_id)
        if analysis is None:
            return rest_error("Unable to find the analysis with id=" + str(analysis_id))
        return rest_success(analysis)



    async def create_analysis(self, request):
        """
            Creae 
        """
        # 1- Retrieve data from request
        data = await request.json()
        name = data["name"]
        ref_id = data["ref_id"]
        template_id = data["template_id"]
        # Create the project 
        analysis, success = annso.analysis.create(name, ref_id, template_id)
        if not success or analysis is None:
            return rest_error("Unable to create an analysis with provided information.")
        return rest_success(analysis)


    def get_setting(self, request):
        # 1- Retrieve data from request
        analysis_id = request.match_info.get('analysis_id', -1)

        try:
            settings = Analysis.from_id(analysis_id).setting
        except Exception as err:
            return rest_error("Unable to get analysis settings with provided information. " + str(err))
        if settings is None: settings = {}
        return rest_success(settings)


    async def set_analysis(self, request):
        # 1- Retrieve data from request
        analysis_id = request.match_info.get('analysis_id', -1)
        data = await request.json()
        try:
            annso.analysis.update(analysis_id, data)
        except Exception as err:
            return rest_error("Error occured when trying to save settings for the analysis with id=" + str(analysis_id) + ". " + str(err))
        return rest_success() 

        

    async def filtering(self, request, count=False):
        # 1- Retrieve data from request
        data = await request.json()
        analysis_id = request.match_info.get('analysis_id', -1)
        filter_json = data["filter"] if "filter" in data else {}
        fields = data["fields"] if "fields" in data else None
        limit = data["limit"] if "limit" in data else 100
        offset = data["offset"] if "offset" in data else 0
        mode = data["mode"] if "mode" in data else "table"
        order = data["order"] if "order" in data else None

        # 2- Check parameters
        if "mode" in data: mode = data["mode"]
        if limit<0 or limit > RANGE_MAX: limit = 100
        if offset<0: offset = 0
        
        # 3- Execute filtering request
        try:
            result = annso.filter.request(int(analysis_id), mode, filter_json, fields, order, int(limit), int(offset), count)
        except Exception as err:
            return rest_error("Filtering error: " + str(err))
        return rest_success(result)




    async def filtering_count(self, request):
        return await self.filtering(request, True)




    def get_filters(self, request):
        analysis_id = request.match_info.get('analysis_id', -1)
        result = annso.analysis.get_filters(analysis_id)
        return rest_success(result)

    async def new_filter(self, request):
        analysis_id = request.match_info.get('analysis_id', -1)
        data = await request.json()
        result = annso.analysis.save_filter(analysis_id, data['name'], data['filter'])
        return rest_success(result)

    async def set_filter(self, request):
        filter_id = request.match_info.get('filter_id', -1)
        data = await request.json()
        annso.analysis.update_filter(filter_id, data['name'], data['filter'])
        return rest_success()

    def delete_filter(self, request):
        filter_id = request.match_info.get('filter_id', -1)
        annso.analysis.delete_filter(filter_id)
        return rest_success()


    async def get_selection(self, request):
        data = await request.json()
        analysis_id = request.match_info.get('analysis_id', -1)

        try:
            result = annso.analysis.get_selection(analysis_id, data)
        except Exception as err:
            return rest_error("AnalysisHandler.get_selection error: " + str(err))
        return rest_success(result)


    async def load_ped(self, request):
        ped = await request.content.read()
        analysis_id = request.match_info.get('analysis_id', -1)
        # write ped file in temporary cache directory
        file_path = os.path.join(DOWNLOAD_DIR, "tpm_{}.ped".format(analysis_id))
        with open(file_path, "w") as f:
            f.write(ped)
        # update model
        try:
            annso.analysis.load_ped(file_path)
        except Exception as err:
            os.remove(file_path)
            return rest_error("Error occured ! Wrong Ped file: " + str(err))
        os.remove(file_path)
        return rest_success(result)
        





    async def get_report(self, request):
        data = await request.json()
        analysis_id = request.match_info.get('analysis_id', -1)
        report_id = request.match_info.get('report_id', -1)

        try:
            cache_path = annso.analysis.report(analysis_id, report_id, data)
        except Exception as err:
            return rest_error("AnalysisHandler.get_report error: " + str(err))

        # create url to access to the report
        url = '{0}/cache{1}'.format(HOST_P, cache_path[len(CACHE_DIR):])
        return rest_success({'url': url})



    async def get_export(self, request):
        data = await request.json()
        analysis_id = request.match_info.get('analysis_id', -1)
        export_id = request.match_info.get('export_id', -1)

        try:
            result = annso.analysis.export(analysis_id, export_id, data)
        except Exception as err:
            return rest_error("AnalysisHandler.get_export error: " + str(err))
        return rest_success({"url": "http://your_export."+str(export_id)})




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# SAMPLE HANDLER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Customization of the TUS protocol for the download of sample files
# Sample TUS wrapper
class SampleFileWrapper (TusFileWrapper):
    def __init__(self, id):
        self.file = File.from_id(id)
        if self.file is not None:
            self.id = id
            self.name = self.file.filename
            self.upload_offset = self.file.upload_offset
            self.path = self.file.path
            self.size = self.file.size
            self.upload_url = "sample/upload/" + str(id)
        else:
            return TusManager.build_response(code=500, body="Unknow id: {}".format(id))


    def save(self):
        try:
            f = File.from_id(self.id)
            Model.session().add(f)
            f.upload_offset=self.upload_offset
            Model.session().commit()
        except Exception as error:
            return TusManager.build_response(code=500, body="Unexpected error occured: {}".format(error))


    async def complete(self, checksum=None, checksum_type="md5"):
        try:
            log ('Upload of the file (id={0}) is complete.'.format(self.id))
            await annso.file.upload_finish(self.id, checksum, checksum_type)
        except Exception as error:
            return TusManager.build_response(code=500, body="Unexpected error occured: {}".format(error))


    @staticmethod
    def new_upload(request, filename, file_size):
        """ 
            Create and return the wrapper to manipulate the uploading file
        """
        annso_file = annso.file.upload_init(filename, file_size)
        return SampleFileWrapper(annso_file.id)



# set mapping
tus_manager.route_maping["/sample/upload"] = SampleFileWrapper



class SampleHandler:
    def get_samples(self, request):
        # Generic processing of the get query
        fields, query, order, offset, limit = process_generic_get(request.query_string, Sample.public_fields)
        # Get range meta data
        range_data = {
            "range_offset": offset,
            "range_limit" : limit,
            "range_total" : annso.sample.total(),
            "range_max"   : RANGE_MAX,
        }
        # Return result of the query 
        return rest_success(annso.sample.get(fields, query, order, offset, limit), range_data)


    def get_sample(self, request):
        sid = request.match_info.get('sample_id', None)
        if sid is None:
            return rest_error("No valid sample id provided")
        sample = Sample.from_id(sid)
        if sample is None:
            return rest_error("No sample found with id="+str(sid))
        return rest_success(sample.to_json())


    def get_details(self, request):
        db_name = request.match_info.get('db_name', None)
        if db_name is None:
            return rest_error("No database name provided")

        return rest_success({"database": db_name})


    # Resumable download implement the TUS.IO protocol.
    def tus_config(self, request):
        return tus_manager.options(request)

    async def tus_upload_init(self, request):
        return tus_manager.creation(request)

    def tus_upload_resume(self, request):
        return tus_manager.resume(request)

    async def tus_upload_chunk(self, request):
        result = await tus_manager.patch(request)
        return result

    def tus_upload_delete(self, request):
        return tus_manager.delete_file(request)












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

        WebsocketHandler.socket_list.append((ws, ws_id))
        msg = {'msg':'hello', 'data': [[str(_ws[1]) for _ws in WebsocketHandler.socket_list]]}
        notify_all(msg)

        try:
            async for msg in ws:
                if msg.tp == aiohttp.MsgType.text:
                    if msg.data == 'close':
                        log ('CLOSE MESSAGE RECEIVED')
                        await ws.close()
                    else:
                        # Analyse message sent by client and send response if needed
                        data = msg.json()
                        if data['msg'] == 'user_info':
                            log('WebsocketHandler {0} '.format(data['msg']))
                            pass
                        elif msg.tp == aiohttp.MsgType.error:
                            log('ws connection closed with exception {0}'.format(ws.exception()))
        finally:
            WebsocketHandler.socket_list.remove((ws, ws_id))

        return ws











async def on_shutdown(app):
    log("SHUTDOWN SERVER... CLOSE ALL")
    for ws in WebsocketHandler.socket_list:
        await ws[0].close(code=999, message='Server shutdown')
