#!env/python3
# coding: utf-8




metadata = {
    "name" : "VCF",
    "input" :  ["vcf", "vcf.gz"],
    "description" : "Import variants from vcf file"
}



def import_data(file_id, filepath, core=None, db_ref_suffix="_hg19"):
    import ipdb

    import os
    import datetime
    import sqlalchemy
    import subprocess
    import multiprocessing as mp
    import reprlib
    from pysam import VariantFile


    from core.framework import get_or_create
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
            print ("unknow : " + str(infos['GT']) )
        return '?'



    def get_info(infos, key):
        if (key in infos):
            if infos[key] is None : return 'NULL'
            return infos[key]
        return 'NULL'




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

        if core is not None:
            core.notify_all({'msg':'import_vcf_start', 'data' : {'file_id' : file_id, 'samples' : [ {'id' : samples[s].id, 'name' : samples[s].name} for s in samples.keys()]}})

        # Associate sample to the file
        ipdb.set_trace()
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
        print("Importing file ", filepath, "\n\r\trecords  : ", records_count, "\n\r\tsamples  :  (", len(samples.keys()), ") ", reprlib.repr([s for s in samples.keys()]), "\n\r\tstart    : ", start)
        # bar = Bar('\tparsing  : ', max=records_count, suffix='%(percent).1f%% - %(elapsed_td)s')
        sql_head1 = "INSERT INTO variant{0} (chr, pos, ref, alt, is_transition) VALUES ".format(db_ref_suffix)
        sql_pattern2 = "INSERT INTO sample_variant" + db_ref_suffix + " (sample_id, variant_id, chr, pos, ref, alt, genotype, deepth) SELECT {0}, id, '{1}', {2}, '{3}', '{4}', '{5}', {6} FROM variant" + db_ref_suffix + " WHERE chr='{1}' AND pos={2} AND ref='{3}' AND alt='{4}' ON CONFLICT DO NOTHING;"
        sql_tail = " ON CONFLICT DO NOTHING;"
        sql_query1 = ""
        sql_query2 = ""
        count = 0
        for r in vcf_reader: 
            records_current += 1 
            if core is not None:
                core.notify_all({'msg':'import_vcf', 'data' : {'file_id' : file_id, 'progress_total' : records_count, 'progress_current' : records_current, 'progress_percent' : records_current / max(1,records_count)}})

            chrm = normalize_chr(str(r.chrom))
            
            for sn in r.samples:
                s = r.samples.get(sn)
                if (len(s.alleles) > 0) :
                    pos, ref, alt = normalize(r.pos, r.ref, s.alleles[0])

                    if alt != ref :
                        sql_query1 += "('{}', {}, '{}', '{}', {}),".format(chrm, str(pos), ref, alt, is_transition(ref, alt))
                        sql_query2 += sql_pattern2.format(str(samples[sn].id), chrm, str(pos), ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1

                    pos, ref, alt = normalize(r.pos, r.ref, s.alleles[1])
                    if alt != ref :
                        sql_query1 += "('{}', {}, '{}', '{}', {}),".format(chrm, str(pos), ref, alt, is_transition(ref, alt))
                        sql_query2 += sql_pattern2.format(str(samples[sn].id), chrm, str(pos), ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1

                    # manage split big request to avoid sql out of memory transaction
                    if count >= 50000:
                        count = 0
                        transaction1 = sql_head1 + sql_query1[:-1] + sql_tail
                        transaction2 = sql_query2

                        # if job_in_progress >= max_job_in_progress:
                        #     print ("\nto many job in progress, waiting... (" + datetime.datetime.now().ctime() + ")")
                        # while job_in_progress >= max_job_in_progress:
                        #     time.sleep(100)
                        # print ("\nStart new job " + str(job_in_progress) + "/" + str(max_job_in_progress) + " (" + datetime.datetime.now().ctime() + ")")
                        #threading.Thread(target=exec_sql_query, args=(transaction1 + transaction2, )).start() # both request cannot be executed in separated thread. sql2 must be executed after sql1
                        pool.apply_async(exec_sql_query, (transaction1 + transaction2, ))
                        sql_query1 = ""
                        sql_query2 = ""

        # bar.finish()
        end = datetime.datetime.now()
        # print("\tparsing done   : " , end, " => " , (end - start).seconds, "s")
        transaction1 = sql_head1 + sql_query1[:-1] + sql_tail
        transaction2 = sql_query2
        db_engine.execute(transaction1 + transaction2)

        current = 0
        while job_in_progress > 0:
            if current != job_in_progress:
                # print ("\tremaining sql job : ", job_in_progress)
                current = job_in_progress
            pass

        end = datetime.datetime.now()
        # print("\tdb import done : " , end, " => " , (end - start).seconds, "s")
        # print("")

    end = datetime.datetime.now()
    if core is not None:
        core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id}})
