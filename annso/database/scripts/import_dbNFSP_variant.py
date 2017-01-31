#!env/python3
# coding: utf-8


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Tiers code from vtools.  Bin index calculation 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


#
# Utility function to calculate bins.
#
# This function implements a hashing scheme that UCSC uses (developed by Jim Kent) to 
# take in a genomic coordinate range and return a set of genomic "bins" that your range
# intersects.  I found a Java implementation on-line (I need to find the URL) and I
# simply manually converted the Java code into Python code.  
    
# IMPORTANT: Because this is UCSC code the start coordinates are 0-based and the end 
# coordinates are 1-based!!!!!!
        
# BINRANGE_MAXEND_512M = 512 * 1024 * 1024
# binOffsetOldToExtended = 4681; #  (4096 + 512 + 64 + 8 + 1 + 0)

_BINOFFSETS = (
    512+64+8+1,   # = 585, min val for level 0 bins (128kb binsize)    
    64+8+1,       # =  73, min val for level 1 bins (1Mb binsize) 
    8+1,          # =   9, min val for level 2 bins (8Mb binsize)  
    1,            # =   1, min val for level 3 bins (64Mb binsize)  
    0)            # =   0, only val for level 4 bin (512Mb binsize)
     
#    1:   0000 0000 0000 0001    1<<0       
#    8:   0000 0000 0000 1000    1<<3
#   64:   0000 0000 0100 0000    1<<6
#  512:   0000 0010 0000 0000    1<<9
 
_BINFIRSTSHIFT = 17;            # How much to shift to get to finest bin.
_BINNEXTSHIFT = 3;              # How much to shift to get to next larger bin.
_BINLEVELS = len(_BINOFFSETS)
  
#
# IMPORTANT: the start coordinate is 0-based and the end coordinate is 1-based.
#
def getUcscBins(start, end):
    bins = []
    startBin = start >> _BINFIRSTSHIFT
    endBin = (end-1) >> _BINFIRSTSHIFT
    for i in range(_BINLEVELS):
        offset = _BINOFFSETS[i];
        if startBin == endBin:
            bins.append(startBin + offset)
        else:
            for bin in range(startBin + offset, endBin + offset):
                bins.append(bin);
        startBin >>= _BINNEXTSHIFT
        endBin >>= _BINNEXTSHIFT
    return bins

def getMaxUcscBin(start, end):
    bin = 0
    startBin = start >> _BINFIRSTSHIFT
    endBin = (end-1) >> _BINFIRSTSHIFT
    for i in range(_BINLEVELS):
        offset = _BINOFFSETS[i];
        if startBin == endBin:
            if startBin + offset > bin:
                bin = startBin + offset
        else:
            for i in range(startBin + offset, endBin + offset):
                if i > bin:
                    bin = i 
        startBin >>= _BINNEXTSHIFT
        endBin >>= _BINNEXTSHIFT
    return bin






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Compute bin index (hg18, hg19 and hg38) for all variants 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# DATABASE CONNECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def connect(user, password, db, host, port):
    '''Returns a connection and a metadata object'''
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8') #, strategy=ASYNCIO_STRATEGY)
    meta = sqlalchemy.MetaData(bind=con)
    return con, meta


# Connect and map the engine to the database
Base = automap_base()

# TODO / FIXME : why the format with config option doesn't work ...
# db_engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DATABASE_USER, DATABASE_PWD, DATABASE_HOST,  DATABASE_PORT, DATABASE_NAME))
db_engine = create_engine("postgresql://annso:annso@localhost/annso")

Base.prepare(db_engine, reflect=True)
Base.metadata.create_all(db_engine)






chrs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'Y']
step = 100
for chr in chrs:
    print ("counting row to process ...")
    records_count = db_engine.execute("SELECT COUNT(*) FROM dbnfsp_variant WHERE bin_hg38 IS NULL AND chr_hg38='{0}'".format(chr)).first()[0]
    records_done = 0

    print ("Start to compute bin index for the {0} chr : {1} rows".format(chr, records_count))
    print (datetime.datetime.now().ctime())

    loop_flag = True
    
    while loop_flag:
        query = ""

        result = db_engine.execute("SELECT bin_hg38, chr_hg38, pos_hg38, chr_hg19, pos_hg19, chr_hg18, pos_hg18, ref FROM dbnfsp_variant WHERE bin_hg38 IS NULL AND chr_hg38='{0}' LIMIT {1}".format(chr, step))
        if  result.rowcount == 0:
            loop_flag = False;
            break;

        for r in  result:

            if r.bin_hg38 is None: 
                length = len(r.ref) if r.ref is not None else 0
                bin_hg38 = getMaxUcscBin(r.pos_hg38-1, r.pos_hg38-1 + length) if r.pos_hg38 is not None else 'NULL'
                bin_hg19 = getMaxUcscBin(r.pos_hg19-1, r.pos_hg19-1 + length) if r.pos_hg19 is not None else 'NULL'
                bin_hg18 = getMaxUcscBin(r.pos_hg18-1, r.pos_hg18-1 + length) if r.pos_hg18 is not None else 'NULL'
                query += "UPDATE dbnfsp_variant SET bin_hg38={0}, bin_hg19={1}, bin_hg18={2} WHERE  bin_hg38 IS NULL AND chr_hg38='{3}' AND pos_hg38={4} AND ref='{5}'; ".format(bin_hg38, bin_hg19, bin_hg18, r.chr_hg38, r.pos_hg38, r.ref)

        if query is not "":
            db_engine.execute(query)

        records_done += result.rowcount
        percent = round(records_done / max(1,records_count), 2) * 100
        print("   {0} / {1} - {2}% Done".format(records_done, records_count, percent))
    print (datetime.datetime.now().ctime())
    print("finished")
