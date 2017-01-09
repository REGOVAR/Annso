#!env/python3
# coding: utf-8

import aiohttp_jinja2
import jinja2
from aiohttp import web

from config import *
from core import annso
from api_rest.handlers import *




app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR))	


# Handlers instances
websocket = WebsocketHandler()
website = WebsiteHandler()
dbHandler = AnnotationDBHandler()
analysisHandler = AnalysisHandler()
sampleHandler = SampleHandler()
variantHandler = VariantHandler()
reportHandler = ReportHandler()

# Config server app
app['websockets'] = []

# On shutdown, close all websockets
app.on_shutdown.append(on_shutdown)




# Routes
app.router.add_route('GET',    "/",          website.home)
app.router.add_route('GET',    "/v1/www",    website.home)
app.router.add_route('GET',    "/v1/config", website.get_config)
app.router.add_route('GET',    "/v1/ws",     websocket.get)


app.router.add_route('GET',    "/v1/db",        dbHandler.get_databases)
app.router.add_route('GET',    "/v1/db/fields", dbHandler.get_fields)


app.router.add_route('GET',    "/v1/sample",             sampleHandler.get_samples)
app.router.add_route('GET',    "/v1/sample/{sample_id}", sampleHandler.get_sample)
app.router.add_route('GET',    "/v1/variant",            variantHandler.get_variants)
app.router.add_route('GET',    "/v1/report",             reportHandler.get_html_report)



# app.router.add_route('GET',  "/v1/analysis",     analysisHandler.get_analyses)
app.router.add_route('POST',   "/v1/analysis",  analysisHandler.create_analysis)
app.router.add_route('GET',    "/v1/analysis/{analysis_id}",  analysisHandler.get_analysis)
app.router.add_route('PUT',    "/v1/analysis/{analysis_id}",  analysisHandler.set_analysis)
app.router.add_route('GET',    "/v1/analysis/{analysis_id}/setting",  analysisHandler.get_setting) # TODO
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/filtering",  analysisHandler.filtering)
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/savefilter",  analysisHandler.set_filter)
app.router.add_route('DELETE', "/v1/filter/{filter_id}",  analysisHandler.delete_filter)



# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/sample",     analysisHandler.get_analyses)
# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/sample/{sample_id}",     analysisHandler.get_analyses)
# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/sample/{sample_id}/variant",     analysisHandler.get_analyses)
# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/selection",     analysisHandler.get_analyses)
# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/selection/{selection_id}",     analysisHandler.get_analyses)
# app.router.add_route('GET',  "/v1/analysis/{analysis_id}/selection/{selection_id}/variant",     analysisHandler.get_analyses)



# app.router.add_route('GET',    "/v1/field",                fieldsHandler.get_fields)
# app.router.add_route('GET',    "/v1/field/{field_id}",     fieldsHandler.get_field)


app.router.add_route('POST',   "/v1/sample/upload",           SampleHandler.tus_upload_init)
app.router.add_route('OPTIONS',"/v1/sample/upload",           SampleHandler.tus_config)
app.router.add_route('HEAD',   "/v1/sample/upload/{file_id}", SampleHandler.tus_upload_resume)
app.router.add_route('PATCH',  "/v1/sample/upload/{file_id}", SampleHandler.tus_upload_chunk)
app.router.add_route('DELETE', "/v1/sample/upload/{file_id}", SampleHandler.tus_upload_delete)



# DEV/DEBUG - Routes that should be manages directly by NginX
app.router.add_static('/assets', TEMPLATE_DIR)
app.router.add_static('/cache', CACHE_DIR)