#!env/python3
# coding: utf-8




metadata = {
    "name" : "VCF",
    "input" :  ["vcf", "vcf.gz"],
    "description" : "Import variants from vcf file"
}



def import_data(file_id, filepath, annso_core=None, db_ref_suffix="_hg19"):
    import ipdb

    import os
    import datetime
    import sqlalchemy
    import subprocess
    import multiprocessing as mp
    import reprlib
    from pysam import VariantFile


    from core.framework import get_or_create, log, war, err
    from core.model import Sample, db_engine, db_session





    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Tools
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def normalize_chr(chrm):
        chrm = chrm.upper()
        if (chrm.startswith("CHROM")):
            chrm = chrm[5:]
        if (chrm.startswith("CHRM")):
            chrm = chrm[4:]
        if (chrm.startswith("CHR")):
            chrm = chrm[3:]
        return chrm


    def get_alt(alt):
        if ('|' in alt):
            return alt.split('|')
        else:
            return alt.split('/')


    def normalize(pos, ref, alt):
        # input pos comming from VCF are 1-based.
        # to be consistent with UCSC databases we convert it into 0-based
        pos -= 1

        if (ref == alt):
            return None,None,None
        if ref is None:
            ref = ''
        if alt is None:
            alt = ''
        while len(ref) > 0 and len(alt) > 0 and ref[0]==alt[0] :
            ref = ref[1:]
            alt = alt[1:]
            pos += 1
        if len(ref) == len(alt):
            while ref[-1:]==alt[-1:]:
                ref = ref[0:-1]
                alt = alt[0:-1]
        return pos, ref, alt


    def is_transition(ref, alt):
        tr = ref+alt
        if len(ref) == 1 and tr in ('AG', 'GA', 'CT', 'TC'):
            return True
        return False


    def normalize_gt(infos):
        gt = get_info(infos, 'GT')
        if gt != 'NULL':
            if infos['GT'][0] == infos['GT'][1]:
                # Homozyot ref
                if infos['GT'][0] in [None, 0] : 
                    return 0
                # Homozyot alt
                return '1'
            else :
                if 0 in infos['GT'] :
                    # Hetero ref
                    return '2'
                else :
                    return '3'
            log ("unknow : " + str(infos['GT']) )
        return '?'



    def get_info(infos, key):
        if (key in infos):
            if infos[key] is None : return 'NULL'
            return infos[key]
        return 'NULL'





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
    # Import 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def exec_sql_query(raw_sql):
        global job_in_progress, db_engine
        job_in_progress += 1
        db_engine.execute(raw_sql)
        job_in_progress -= 1



    global db_session

    start_0 = datetime.datetime.now()
    max_job_in_progress = 6
    job_in_progress = 0
    pool = mp.Pool(processes=max_job_in_progress)

    if filepath.endswith(".vcf") or filepath.endswith(".vcf.gz"):
        start = datetime.datetime.now()

        # Create vcf parser
        vcf_reader = VariantFile(filepath)

        # get samples in the VCF 
        samples = {i : get_or_create(db_session, Sample, name=i)[0] for i in list((vcf_reader.header.samples))}
        db_session.commit()
        if len(samples.keys()) == 0 : 
            war("VCF files without sample cannot be imported in the database.")
            if annso_core is not None:
                annso_core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id, 'msg' : "VCF files without sample cannot be imported in the database."}})
            return;

        if annso_core is not None:
            annso_core.notify_all({'msg':'import_vcf_start', 'data' : {'file_id' : file_id, 'samples' : [ {'id' : samples[s].id, 'name' : samples[s].name} for s in samples.keys()]}})


        # Associate sample to the file
        db_engine.execute("INSERT INTO sample_file (sample_id, file_id) VALUES {0};".format( ','.join(["({0}, {1})".format(samples[sid].id, file_id) for sid in samples])))


        # console verbose
        bashCommand = 'grep -v "^#" ' + str(filepath) +' | wc -l'
        if filepath.endswith(".vcf.gz"):
            bashCommand = "z" + bashCommand
        
        # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd_out = process.communicate()[0]
        records_count = int(cmd_out.decode('utf8'))
        records_current = 0

        # parsing vcf file
        table = "variant" + db_ref_suffix
        log ("Importing file {0}\n\r\trecords  : {1}\n\r\tsamples  :  ({2}) {3}\n\r\tstart    : {4}".format(filepath, records_count, len(samples.keys()), reprlib.repr([s for s in samples.keys()]), start))
        # bar = Bar('\tparsing  : ', max=records_count, suffix='%(percent).1f%% - %(elapsed_td)s')
        
        sql_pattern1 = "INSERT INTO {0} (chr, pos, ref, alt, is_transition, bin, sample_list) VALUES ('{1}', {2}, '{3}', '{4}', {5}, {6}, '{{{7}}}') ON CONFLICT (chr, pos, ref, alt) DO UPDATE SET sample_list=array_cat(array_remove({0}.sample_list, {7}), '{{{7}}}')  WHERE {0}.chr='{1}' AND {0}.pos={2} AND {0}.ref='{3}' AND {0}.alt='{4}';"
        sql_pattern2 = "INSERT INTO sample_variant" + db_ref_suffix + " (sample_id, variant_id, bin, chr, pos, ref, alt, genotype, depth) SELECT {0}, id, {1}, '{2}', {3}, '{4}', '{5}', '{6}', {7} FROM variant" + db_ref_suffix + " WHERE bin={1} AND chr='{2}' AND pos={3} AND ref='{4}' AND alt='{5}' ON CONFLICT DO NOTHING;"
        sql_tail = " ON CONFLICT DO NOTHING;"
        sql_query1 = ""
        sql_query2 = ""
        count = 0
        for r in vcf_reader: 
            records_current += 1 
            if annso_core is not None:
                annso_core.notify_all({'msg':'import_vcf', 'data' : {'file_id' : file_id, 'progress_total' : records_count, 'progress_current' : records_current, 'progress_percent' : round(records_current / max(1,records_count) * 100, 2)}})

            chrm = normalize_chr(str(r.chrom))
            samples_array = ','.join([str(samples[s].id) for s in r.samples])
            for sn in r.samples:
                s = r.samples.get(sn)
                if (len(s.alleles) > 0) :
                    pos, ref, alt = normalize(r.pos, r.ref, s.alleles[0])

                    if alt != ref :
                        bin = getMaxUcscBin(pos, pos + len(ref))
                        sql_query1 += sql_pattern1.format(table, chrm, str(pos), ref, alt, is_transition(ref, alt), bin, samples_array)
                        sql_query2 += sql_pattern2.format(str(samples[sn].id), bin, chrm, str(pos), ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1

                    pos, ref, alt = normalize(r.pos, r.ref, s.alleles[1])
                    if alt != ref :
                        bin = getMaxUcscBin(pos, pos + len(ref))
                        sql_query1 += sql_pattern1.format(table, chrm, str(pos), ref, alt, is_transition(ref, alt), bin, samples_array)
                        sql_query2 += sql_pattern2.format(str(samples[sn].id), bin, chrm, str(pos), ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1

                    # manage split big request to avoid sql out of memory transaction
                    if count >= 50000:
                        count = 0
                        transaction1 = sql_query1
                        transaction2 = sql_query2

                        # if job_in_progress >= max_job_in_progress:
                        #     log ("\nto many job in progress, waiting... (" + datetime.datetime.now().ctime() + ")")
                        # while job_in_progress >= max_job_in_progress:
                        #     time.sleep(100)
                        # log ("\nStart new job " + str(job_in_progress) + "/" + str(max_job_in_progress) + " (" + datetime.datetime.now().ctime() + ")")
                        #threading.Thread(target=exec_sql_query, args=(transaction1 + transaction2, )).start() # both request cannot be executed in separated thread. sql2 must be executed after sql1
                        pool.apply_async(exec_sql_query, (transaction1 + transaction2, ))
                        sql_query1 = ""
                        sql_query2 = ""

        # bar.finish()
        end = datetime.datetime.now()
        # log("\tparsing done   : " , end, " => " , (end - start).seconds, "s")
        transaction1 = sql_query1
        transaction2 = sql_query2
        db_engine.execute(transaction1 + transaction2)

        current = 0
        while job_in_progress > 0:
            if current != job_in_progress:
                # log ("\tremaining sql job : ", job_in_progress)
                current = job_in_progress
            pass

        end = datetime.datetime.now()
        # log("\tdb import done : " , end, " => " , (end - start).seconds, "s")
        # log("")

    end = datetime.datetime.now()
    if annso_core is not None:
        annso_core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id, 'msg' : 'Import done without error.', 'samples': [ {'id' : samples[s].id, 'name' : samples[s].name} for s in samples.keys()]}})
