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


# Config server app
app['websockets'] = []

# On shutdown, close all websockets
app.on_shutdown.append(on_shutdown)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ROUTES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
app.router.add_route('GET',    "/", website.home)                                                               # Get the html annso client
app.router.add_route('GET',    "/v1/config", website.get_config)                                                # Get configuration of the annso application
app.router.add_route('GET',    "/v1/ws", websocket.get)                                                         # Init a websockets connection


app.router.add_route('GET',    "/v1/db/ref", dbHandler.get_referencials)                                        # Get list of genom's referencials supported
app.router.add_route('GET',    "/v1/db/{ref_id}", dbHandler.get_databases)                                      # Get list of all annotation's databases and for each the list of availables versions and the list of their fields for the latest version
app.router.add_route('GET',    "/v1/db/fields", dbHandler.get_fields)                                           # Get flat list of all annotation's fields available
app.router.add_route('GET',    "/v1/db/{db_id}", dbHandler.get_database)                                        # Get the database description and the list of available versions
app.router.add_route('GET',    "/v1/db/{db_id}/{db_version}", dbHandler.get_database_fields)                    # Get the database details and the list of all its fields


app.router.add_route('GET',    "/v1/variant/{variant_id}", variantHandler.get_variant)                          # Get all available information about the given variant


app.router.add_route('GET',    "/v1/sample", sampleHandler.get_samples)                                         # Get list of all samples in database
app.router.add_route('GET',    "/v1/sample/{sample_id}", sampleHandler.get_sample)                              # Get specific sample's data


app.router.add_route('POST',   "/v1/analysis", analysisHandler.create_analysis)                                 # Create new analysis
app.router.add_route('GET',    "/v1/analysis/{analysis_id}", analysisHandler.get_analysis)                      # Get analysis metadata
app.router.add_route('PUT',    "/v1/analysis/{analysis_id}", analysisHandler.set_analysis)                      # Save analysis metadata
app.router.add_route('GET',    "/v1/analysis/{analysis_id}/setting", analysisHandler.get_setting)               # TODO : Get analysis setting (NEED ??)
app.router.add_route('GET',    "/v1/analysis/{analysis_id}/filter", analysisHandler.get_filters)                # Get list of available filter for the provided analysis
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/filter", analysisHandler.new_filter)                 # Create a new filter for the analisis
app.router.add_route('PUT',    "/v1/analysis/{analysis_id}/filter/{filter_id}", analysisHandler.set_filter)     # TODO : Update filter
app.router.add_route('DELETE', "/v1/analysis/{analysis_id}/filter/{filter_id}", analysisHandler.delete_filter)  # TODO : Delete a filter
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/filtering", analysisHandler.filtering)               # Get result (variants) of the provided filter
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/filtering/count", analysisHandler.filtering_count)   # Get total count of result of the provided filter
app.router.add_route('GET',    "/v1/analysis/{analysis_id}/selection", analysisHandler.get_selection)           # Get variants data for the provided selection
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/export/{export_id}", analysisHandler.get_export)     # Export selection of the provided analysis into the requested format
app.router.add_route('POST',   "/v1/analysis/{analysis_id}/report/{report_id}", analysisHandler.get_report)     # Generate report html for the provided analysis+report id





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# TUS ROUTES
# /!\ don't forget to also modify route mapping in handlers for the TUS manager
# (in handlers.py, search 'tus_manager.route_maping')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
app.router.add_route('POST',   "/v1/sample/upload",           sampleHandler.tus_upload_init)     # Init a new file transfert
app.router.add_route('OPTIONS',"/v1/sample/upload",           sampleHandler.tus_config)          # Get TUS protocol option supported by the application
app.router.add_route('HEAD',   "/v1/sample/upload/{file_id}", sampleHandler.tus_upload_resume)   # Try to retrieve/resume a file transfert
app.router.add_route('PATCH',  "/v1/sample/upload/{file_id}", sampleHandler.tus_upload_chunk)    # Send a file chunk to
app.router.add_route('DELETE', "/v1/sample/upload/{file_id}", sampleHandler.tus_upload_delete)   # Stop and delete a file transfert



# DEV/DEBUG - Routes that should be manages directly by NginX
app.router.add_static('/assets', TEMPLATE_DIR)

app.router.add_static('/cache', CACHE_DIR)