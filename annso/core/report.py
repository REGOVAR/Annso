#! /usr/bin/env python3

import collections
import csv
import glob
import gzip
import itertools
import json
import logging
import os
import pprint
import requests
import shutil
import subprocess
import tempfile
import wand.color
import wand.image

__version__ = '0.1.0'


cache = os.path.join(os.path.dirname(os.path.abspath(__file__)))


genemap_api = 'http://api.omim.org/api/search/geneMap'
omim_api = 'http://api.omim.org/api/entry'
omim_api_key_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'omim_api_key')

rvis_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rvis_v3_20160312.csv')

with open(omim_api_key_filename, 'rt') as omim_api_key_file:
    omim_api_key = omim_api_key_file.read()

id_genes_list = 'https://raw.githubusercontent.com/REGOVAR/GenesPanel/master/intellectual_disability.lst'
r = requests.get(id_genes_list)
if r.status_code == requests.codes.ok:
    id_genes = set(r.text.splitlines())
else:
    logger.warning('Unable to access the list of ID genes')
    id_genes = set()




# RVIS Shall be integrated into the SQL database directly (no more external file)
# rvis_score = {}
# with open(rvis_filename, 'rt', newline='') as rvis_file:
#     rvis_reader = csv.reader(rvis_file, delimiter=',', quotechar='"')
#     next(rvis_reader, None)  # skip the headers
#     for row in rvis_reader:
#         rvis_score[row[0]] = row[3], row[4]












def convert_doc(source, destination):
    subprocess.run(['pandoc', '-s', '-o', destination, source])



# Retrieve Humain brain transcriptom image for the gene
def get_hbt_image(gene_name):
    image_url  = 'http://hbatlas.org/hbtd/images/wholeBrain/{}.pdf'.format(gene_name)
    image_filename = os.path.join(cache, 'hbt_image_{}.png'.format(gene_name))
    missing_filename = os.path.join(cache, 'hbt_image_{}.missing'.format(gene_name))
    if os.path.exists(image_filename) :
        return image_filename
    elif os.path.exists(missing_filename):
        return None
    try:
        r = requests.get(image_url, stream=True)
        if r.status_code == requests.codes.ok:
            with tempfile.TemporaryFile() as image_file:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, image_file)
                image_file.seek(0)
                with wand.image.Image(file=image_file, resolution=200) as image:
                    with wand.image.Image(width=image.width, height=image.height, background=wand.color.Color('white')) as bg:
                        bg.composite(image, 0, 0)
                        bg.save(filename=image_filename)
            return image_filename
        else:
            logger.warning('Unable to find the HBT diagram for {}'.format(gene_name))
    except:
        logger.warning('Unable to convert PDF from HBT to PNG for the gene {}'.format(gene_name))
    with open(missing_filename, 'wb') as image:
        pass
    return None






# True or false : Is the gene in SFARI (db for authistic)
def get_SFARI_result(gene_name):
    sfari_url = 'https://gene.sfari.org/autdb/submitsearch?selfld_0=GENES_GENE_SYMBOL&selfldv_0=%s&numOfFields=1&userAction=search&tableName=AUT_HG&submit=Submit+Query' % gene_name
    sfari_scr = False
    r = requests.get(sfari_url)
    if r.status_code == requests.codes.ok:
        if gene_name in r.text:
            sfari_scr = True
    return sfari_scr


















# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NEED TO INSTALL CutyCapt on the server develop python tool to retrieve html code of the decipher grid to import data
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


def convert_html(source, destination, delay=0):
    subprocess.run(['CutyCapt', '--url={}'.format(source), '--out={}'.format(destination), '--delay={}'.format(delay)])


# DECIPHER
def get_decipher_image(gene_name, output_folder):
    dec_filename = output_folder + '/' + gene_name  + '_decipher.png'
    dec_url  = 'https://decipher.sanger.ac.uk/search?q=%s#consented-patients/results' % gene_name

    if os.path.isfile(dec_filename) :
        return dec_filename

    # 1- retrieve image
    convert_html(dec_url, '{}_source.png'.format(dec_filename), 3000)

    # 2- crop image
    if os.path.isfile(dec_filename + '_source.png'):
        with open(dec_filename + '_source.png', 'rb') as f:
            with wand.image.Image(file=f) as image:
                w = image.width - 10
                h = image.height - 315 - 360
                image.crop(5, 315, width=w, height=h)
                image.save(filename=dec_filename)
                os.remove(dec_filename + '_source.png')
                return dec_filename
    else:
        logger.warning('Unable to retrieve image from Decipher for the gene {}'.format(gene_name))

    return output_folder + '/error.png'






# HUMAN PROTEIN ATLAS
# Need some customisation to be able to request the website
import http.client
http.client._MAXHEADERS = 1000
from bs4 import BeautifulSoup


def get_ta_image(gene_name, output_folder):
    ta_filename = output_folder + '/' + gene_name + '_ta'
    ta_url  = 'http://www.proteinatlas.org/search/%s' % gene_name

    if os.path.isfile(ta_filename + '.png') :
        return ta_filename + '.png'

    # 1- Retrieve "true url" from TA "user website url"
    r = requests.get(ta_url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if (link.text==gene_name):
                ta_url = 'http://www.proteinatlas.org' + link.get('href')

    # 2- Retrieve html page with graphs
    r = requests.get(ta_url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
        <html>
            <head>
                <title>Tissue expression of DRD4 - Summary - The Human Protein Atlas</title>
                <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
                <meta name="description" content="Summary of DRD4 expression in human tissue. ">
                <link rel="icon" type="image/png" href="http://www.proteinatlas.org/images_static/favicon_anim.gif">
                <link rel="stylesheet" type="text/css" href="http://www.proteinatlas.org/common.css?version=15.0.0">
                <link rel="stylesheet" type="text/css" href="http://www.proteinatlas.org/search.css?version=15.0.0">
                <link rel="stylesheet" type="text/css" href="http://www.proteinatlas.org/image.css?version=15.0.0">
                <link rel="stylesheet" type="text/css" href="http://www.proteinatlas.org/image_stack.css?version=15.0.0">
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/utils/jquery.min.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/common.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/search.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/image.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/image_stack.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/utils/d3.min.js?version=15.0.0"></script>
                <script language="javascript" type="text/javascript" src="http://www.proteinatlas.org/utils/box.min.js?version=15.0.0"></script>
            </head>
            <body>
        """
        p = soup.find('p', text='RNA EXPRESSION OVERVIEW')
        html += p.findParent('table').prettify()
        html += '\n</body></html>'

    # 3- save into file
    with open(ta_filename + '.html', 'wt') as ta_file:
        ta_file.write(html)

    # 4- convert html into png
    convert_html('file://{}.html'.format(ta_filename), '{}.png'.format(ta_filename), 500)
    os.remove(ta_filename+'.html')
    return ta_filename + '.png'









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NEED TO DEVELOP SP manager to create "task" on the site and be able to retrieve then all generated files/images
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def get_sp_image(gene_name):
    image_url  = 'http://string-db.org/api/image/network?identifier={}_HUMAN'.format(gene_name)
    image_filename = os.path.join(cache, 'sp_image_{}.png'.format(gene_name))
    missing_filename = os.path.join(cache, 'sp_image_{}.missing'.format(gene_name))
    if os.path.exists(image_filename) :
        return image_filename
    elif os.path.exists(missing_filename):
        return None
    try:
        r = requests.get(image_url, stream=True)
        if r.status_code == requests.codes.ok:
            with open(image_filename, 'wb') as image_file:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, image_file)
        return image_filename
    except:
        logger.warning('Unable to retrieve image from String Pathway for the gene {}'.format(gene_name))
    with open(missing_filename, 'wb') as image:
        pass
    return None































def fill_omim_info(gene_data, gene_name):
    info_filename = os.path.join(cache, 'omim_info_{}'.format(gene_name))
    if os.path.exists(info_filename):
        with open(info_filename, 'rt') as info_file:
            info = json.load(info_file)
            gene_data.mim_number = info['mim_number']
            gene_data.name = info['name']
            gene_data.symbols = info['symbols']
            gene_data.text = info['text']
        return

    def get_gene_map_list(name):
        r = requests.get(genemap_api, params = {
            'search': name,
            'format': 'json',
            'apiKey': omim_api_key,
        })
        if r.status_code == requests.codes.ok:
            data = r.json()
            response = data['omim']['searchResponse']
            if response['totalResults'] == 0:
                if response['searchSpelling']:
                    return get_gene_map_list(response['searchSpelling'])
                return None
            return response['geneMapList']

    gene_map_list = get_gene_map_list(gene_name)
    if gene_map_list:
        for gene_map_list_entry in gene_map_list:
            gene_map = gene_map_list_entry['geneMap']
            gene_map['geneSymbols'] = [symbol.strip() for symbol in gene_map['geneSymbols'].split(',')]
            symbols = set([symbol.lower() for symbol in gene_map['geneSymbols']])
            if gene_name.lower() in symbols:
                gene_data.mim_number = gene_map['mimNumber']
                gene_data.name = gene_map['geneName']
                gene_data.symbols = gene_map['geneSymbols']
                gene_data.text = []
                r = requests.get(omim_api, params = {
                    'mimNumber': gene_data.mim_number,
                    'include': 'text',
                    'format': 'json',
                    'apiKey': omim_api_key,
                })
                if r.status_code == requests.codes.ok:
                    data = r.json()
                    gene_entry = data['omim']['entryList'][0]['entry']
                    for textSection in gene_entry['textSectionList']:
                        gene_data.text.append(textSection['textSection']['textSectionContent'])
                else:
                    logger.warning('Unable to get the OMIM entry for gene {}'.format(gene_name))
                break
        else:
            logger.warning('Unable to find the OMIM gene map for gene {}'.format(gene_name))
    else:
        logger.warning('Unable to find the OMIM gene map for gene {}'.format(gene_name))
    info = {
        'mim_number': gene_data.mim_number,
        'name': gene_data.name,
        'symbols': gene_data.symbols,
        'text': gene_data.text,
    }
    with open(info_filename, 'wt') as info_file:
        json.dump(info, info_file)

class GeneData:
    def __init__(self, name):
        self.mim_number = None
        self.name = None
        self.symbols = []
        self.text = []

        fill_omim_info(self, name)

        self.id_gene = (name in id_genes)
        self.id_gene_as = None
        if not self.id_gene:
            for symbol in self.symbols:
                self.id_gene = (symbol in id_genes)
                if self.id_gene:
                    self.id_gene_as = symbol
                    break

        self.rvis_score = rvis_score.get(name, None)
        self.rvis_score_as = None
        if not self.rvis_score:
            for symbol in self.symbols:
                self.rvis_score = rvis_score.get(symbol, None)
                if self.rvis_score:
                    self.rvis_score_as = symbol
                    break

        self.hbt_image = get_hbt_image(name)
        self.hbt_image_as = None
        if not self.hbt_image:
            for symbol in self.symbols:
                self.hbt_image = get_hbt_image(symbol)
                if self.hbt_image:
                    self.hbt_image_as = symbol
                    break

        self.sp_image = get_sp_image(name)
        self.sp_image_as = None
        if not self.sp_image:
            for symbol in self.symbols:
                self.sp_image = get_sp_image(symbol)
                if self.sp_image:
                    self.sp_image_as = symbol
                    break

class Gene:
    __cache = {}
    def __init__(self, name, variants):
        self.name = name
        self.variants = variants
        self.data = Gene.__cache.setdefault(name, GeneData(name))
        self.aliases = itertools.chain([self.name], sorted(set(self.data.symbols) - set([self.name])))

    def render_aliases(self, template):
        return ', '.join([template.format(alias, alias) for alias in self.aliases])

class PubmedEntry:
    def __init__(self, data):
        self.uid = data['uid']
        self.fulljournalname = data['fulljournalname']
        self.firstauthor = ''
        self.lastauthor = data['lastauthor']
        self.title = data['title']
        self.elocationid = data['elocationid']
        if len(data['authors']) > 0 :
            self.firstauthor  = data['authors'][0]['name']

def upper_first_letter(string):
    return string[:1].upper() + string[1:]











def get_pubmed(gene_name):
    info_filename = os.path.join('/home/olivier/', 'pubmed_info_{}'.format(gene_name))
    if os.path.exists(info_filename):
        with open(info_filename, 'rt') as info_file:
            data = json.load(info_file)
            return data['count'], [PubmedEntry(a) for a in data['articles']]

    pm_lst_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=20&term=%s' % gene_name
    pm_id_lst = []
    pm_total = 0
    r = requests.get(pm_lst_url)
    if r.status_code == requests.codes.ok:
        data = r.json()
        pm_id_lst = data['esearchresult']['idlist']
        pm_total = data['esearchresult']['count']

    articles = []
    pm_details_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&amp;retmode=json&amp;id=%s' % ','.join(pm_id_lst)
    r = requests.get(pm_details_url)
    if r.status_code == requests.codes.ok:
        data = r.json()
        for pmid in pm_id_lst:
            articles.append(PubmedEntry(data['result'][pmid]))

    info = {
        'count': pm_total,
        'articles': [{'uid':a.uid, 'fulljournalname':a.fulljournalname, 'authors':[{'name':a.firstauthor}], 'lastauthor':a.lastauthor, 'title':a.title, 'elocationid':a.elocationid} for a in articles]
    }
    with open(info_filename, 'wt') as info_file:
        json.dump(info, info_file)

    return pm_total, articles
