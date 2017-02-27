#!env/python3
# coding: utf-8




metadata = {
    "name" : "VCF",
    "input" :  ["vcf", "vcf.gz"],
    "description" : "Import variants from vcf file"
}



def import_data(file_id, filepath, annso_core=None, reference_id = 2):
    import ipdb

    import os
    import datetime
    import sqlalchemy
    import subprocess
    import multiprocessing as mp
    import reprlib
    import gzip
    from pysam import VariantFile


    from core.framework import get_or_create, log, war, err
    from sqlalchemy.orm import Session
    from core.model import Sample, db_engine, db_session, create_session





    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Tools
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def count_vcf_row(filename):
        """
            Use linux OS commands to quickly count variant to parse in the vcf file
        """
        bashCommand = 'grep -v "^#" ' + str(filename) +' | wc -l'
        if filename.endswith("gz"):
            bashCommand = "z" + bashCommand
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd_out = process.communicate()[0]
        return int(cmd_out.decode('utf8'))


    def debug_clear_header(filename):
        """
            A workaround to fix a bug with GVCF header with pysam
        """
        bashCommand = "grep -v '^##GVCFBlock' {} | gzip --best > /var/regovar/downloads/tmp_workaround".format(filename)
        if filename.endswith("gz"):
            bashCommand = "z" + bashCommand
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        bashCommand = "mv /var/regovar/downloads/tmp_workaround  {} ".format(filename)
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)



    def prepare_vcf_parsing(filename):
        """
            Parse vf headers and return information about which data shall be parsed
            and stored in the database
        """
        # Extract headers
        debug_clear_header(filename)

        headers = {}
        samples = []
        _op = open
        if filename.endswith('gz') or filename.endswith('zip'):
            _op = gzip.open
        with _op(filename) as f:
            for line in f:
                if _op != open:
                    line = line.decode()
                if line.startswith('##'):
                    l = line[2:].strip()
                    l = [l[0:l.index('=')], l[l.index('=')+1:]]
                    if l[0] not in headers.keys():
                        if l[0] == 'INFO' :
                            headers[l[0]] = {}
                        else:
                            headers[l[0]] = []
                    if l[0] == 'INFO' :
                        data = l[1][1:-1].split(',')
                        info_id   = data[0][3:]
                        info_type = data[2][5:]
                        info_desc = data[3][13:-1]
                        headers['INFO'].update({info_id : {'type' : info_type, 'description' : info_desc}})
                    else:
                        headers[l[0]].append(l[1])
                elif line.startswith('#'):
                    samples = line[1:].strip().split('\t')[9:]
                else :
                    break;

        # Check for VEP
        vep = {'vep' : False}
        if 'VEP' in headers.keys() and 'CSQ' in headers['INFO'].keys():
            d = headers['INFO']['CSQ']['description'].split('Format:')
            vep = {
                'vep' : {
                    'version'     : headers['VEP'][0].split(' ')[0],
                    'flag'        : 'CSQ',
                    'columns'     : d[1].strip().split('|'),
                    'description' : d[0].strip(),
                    'name'        : 'VEP'
                }
            }

        # Check for SnpEff
        snpeff = {'snpeff' : False }
        if 'SnpEffVersion' in headers.keys() :
            if 'ANN' in headers['INFO'].keys():
                # TODO
                pass
            elif 'EFF' in headers['INFO'].keys():
                d = headers['INFO']['EFF']['description'].split('\'')
                snpeff = {
                    'snpeff' : {
                        'version'     : headers['SnpEffVersion'][0].strip().strip('"').split(' ')[0],
                        'flag'        : 'EFF',
                        'columns'     : [c.strip() for c in d[1].strip().split('|')],
                        'description' : d[0].strip(),
                        'name'        : 'SnpEff'
                    }
                }

        # Retrieve extension
        file_type = os.path.split(filename)[1].split('.')[-1]
        if not 'vcf' in file_type :
            file_type += os.path.split(filename)[1].split('.')[-2] + "."

        # Return result
        result = {
            'vcf_version' : headers['fileformat'][0],
            'name'  : os.path.split(filename)[1],
            'count' : count_vcf_row(filename),
            'size'  : os.path.getsize(filename),
            'type'  : file_type,
            'samples' : samples,
            'annotations' : {}
        }
        result['annotations'].update(vep)
        result['annotations'].update(snpeff)
        return result


    def normalise_annotation_name(name):
        """
            Tool to convert a name of a annotation tool/db/field/version into the corresponding valid name for the database
        """
        if name[0].isdigit():
            name = '_'+name
        def check_char(char):
            if char in ['.', '-', '_', '/']:
                return '_'
            elif char.isalnum():
                # TODO : remove accents
                return char.lower()
            else:
                return ''
        return ''.join(check_char(c) for c in name)


    def create_annotation_db(reference_id, reference_name, table_name, vcf_annotation_metadata):
        """
            Create an annotation database according to information retrieved from the VCF file with the prepare_vcf_parsing method
        """
        # Create annotation table
        session = Session(db_engine)
        pattern = "CREATE TABLE {0} (variant_id bigint, bin integer, chr integer, pos bigint, ref text, alt text, {1});" # DEBUG/FIXME : DROP only here for debug. !! don't do this in prodution
        query   = ""
        db_map = {}
        fields = []
        for col in vcf_annotation_metadata['columns']:
            col_name = normalise_annotation_name(col)
            fields.append("{} text".format(col_name))
            db_map[col_name] = { 'name' : col_name, 'type' : 'string', 'name_ui' : col } # By default, create a table with only text field... TODO : need to find a way to properly cast annotation's columns
        query += pattern.format(table_name, ', '.join(fields))
        query += "CREATE INDEX {0}_idx_vid ON {0} USING btree (variant_id);".format(table_name)
        query += "CREATE INDEX {0}_idx_var ON {0} USING btree (bin, chr, pos);".format(table_name)

        # Register annotation
        db_hasname = session.execute("SELECT MD5('{}')".format(table_name)).first()[0]
        query += "INSERT INTO public.annotation_database (uid, reference_id, name, version, name_ui, description, ord, jointure, type) VALUES "
        query += "('{0}', {1}, '{2}', '{3}', '{4}', '{5}', {6}, '{2} ON {2}.bin={{0}}.bin AND {2}.chr={{0}}.chr AND {2}.pos={{0}}.pos', 'variant');".format(db_hasname, reference_id, table_name, vcf_annotation_metadata['version'], vcf_annotation_metadata['name'], vcf_annotation_metadata['description'], 30)
        query += "INSERT INTO public.annotation_field (database_uid, ord, name, name_ui, type) VALUES "
        for idx, f in enumerate(vcf_annotation_metadata['columns']):
            query += "('{0}', {1}, '{2}', '{3}', 'string'),".format(db_hasname, idx, db_map[normalise_annotation_name(f)]['name'], f)
        
        session.execute(query[:-1])
        session.execute("UPDATE annotation_field SET uid=MD5(concat(database_uid, name)) WHERE uid IS NULL;")
        session.commit()
        session.commit()
        session.close()
        return db_map


    def prepare_annotation_db(reference_id, vcf_annotation_metadata):
        """
            Prepare database for import of custom annotation, and set the mapping between VCF info fields and DB schema
        """

        reference  = db_engine.execute("SELECT table_suffix FROM reference WHERE id={}".format(reference_id)).first()[0]
        table_name = normalise_annotation_name('{}_{}_{}'.format(vcf_annotation_metadata['flag'], vcf_annotation_metadata['version'], reference))
        
        # Get database schema (if available)
        table_cols = {}
        db_uid     = db_engine.execute("SELECT uid FROM annotation_database WHERE name='{}'".format(table_name)).first()

        if db_uid is None:
            # No table in db for these annotation : create new table
            table_cols = create_annotation_db(reference_id, reference, table_name, vcf_annotation_metadata)
        else:
            db_uid = db_uid[0]
            # Table already exists : retrieve columns already defined
            for col in db_engine.execute("SELECT name, name_ui, type FROM annotation_field WHERE database_uid='{}'".format(db_uid)):
                table_cols[col.name] = { 'name' : col.name, 'type' : col.type, 'name_ui' : col.name_ui }
        # TODO : Get diff between columns in vcf and columns in DB, and update DB schema (add missing column) if needed
        diff = []
        for col in vcf_annotation_metadata['columns']:
            if normalise_annotation_name(col) not in table_cols.keys():
                diff.append(col)
        if len(diff) > 0 :
            offset = len(vcf_annotation_metadata['columns'])
            query = ""
            for idx, col in enumerate(diff):
                name=normalise_annotation_name(col)
                query += "ALTER TABLE {0} ADD COLUMN {1} text; INSERT INTO public.annotation_field (database_uid, ord, name, name_ui, type) VALUES ('{2}', {3}, '{1}', '{4}', 'string');".format(table_name, name, db_uid, offset + idx, col)
                table_cols[name] = { 'name' : name, 'type' : 'string', 'name_ui' : col }

            # execute query
            session = Session(db_engine)
            session.execute(query)
            session.commit()
            session.commit()
            session.close()
        # Update vcf_annotation_metadata with database mapping
        vcf_annotation_metadata.update({ 'table' : table_name })
        vcf_annotation_metadata['db_map'] = {}
        for col in vcf_annotation_metadata['columns']:
            vcf_annotation_metadata['db_map'][col] = table_cols[normalise_annotation_name(col)]
        return vcf_annotation_metadata


    def normalize_chr(chrm):
        """
            Normalize chromosome number from VCF format into Database format
        """
        chrm = chrm.upper()
        if chrm.startswith("CHROM"):
            chrm = chrm[5:]
        if chrm.startswith("CHRM") and chrm != "CHRM":
            chrm = chrm[4:]
        if chrm.startswith("CHR"):
            chrm = chrm[3:]

        if chrm == "X":
            chrm = 23
        elif chrm == "Y":
            chrm = 24
        elif chrm == "M":
            chrm = 25
        else:
            try:
                chrm = int(chrm)
            except Exception as error:
                # TODO log /report error
                chrm = None
        return chrm


    def normalize(pos, ref, alt):
        """
            Normalize given (position, ref and alt) from VCF into Database format
             - Assuming that position in VCF are 1-based (0-based in Database)
             - triming ref and alt to get minimal alt (and update position accordingly)
        """
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


    def normalize_gt(infos):
        """
            Normalize GT sample informatin from VCF format into Database format
        """
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
        return -1


    def get_alt(alt):
        """
            Retrieve alternative values from VCF data
        """
        if ('|' in alt):
            return alt.split('|')
        else:
            return alt.split('/')


    def get_info(infos, key):
        """
            Retrieving info annotation from VCF data
        """
        if (key in infos):
            if infos[key] is None : return 'NULL'
            return infos[key]
        return 'NULL'



    def is_transition(ref, alt):
        """
            Return true if the variant is a transversion; false otherwise
        """
        tr = ref+alt
        if len(ref) == 1 and tr in ('AG', 'GA', 'CT', 'TC'):
            return True
        return False



    def escape_value_for_sql(value):
        if type(value) is str:
            value = value.replace('%', '%%')
            value = value.replace("'", "''")

        return value





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


    def exec_sql_query(q1, q2, q3):
        global job_in_progress, db_engine, log
        job_in_progress += 1

        session = Session(db_engine)
        try:
            session.execute(sql_query1)
            session.execute(sql_query2)
            session.execute(sql_query3)
            session.commit()
            session.commit() # Need a second commit to force session to commit :/ ... strange behavior when we execute(raw_sql) instead of using sqlalchemy's objects as query
            session.close()
        except Exception as err:
            ipdb.set_trace()
            log(err)
            if annso_core is not None:
                annso_core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id, 'msg' : 'Error occured : ' + str(err)}})
            session.close()
            return
        job_in_progress -= 1



    start_0 = datetime.datetime.now()
    max_job_in_progress = 6
    job_in_progress = 0
    pool = mp.Pool(processes=max_job_in_progress)

    ipdb.set_trace()
    vcf_metadata = prepare_vcf_parsing(filepath)
    db_ref_suffix="_hg19" # TODO/FIXME : retrieve data from annso core

    # Prepare database for import of custom annotation, and set the mapping between VCF info fields and DB schema
    for annotation in vcf_metadata['annotations'].keys():
        data = prepare_annotation_db(reference_id, vcf_metadata['annotations'][annotation])
        vcf_metadata['annotations'][annotation].update(data)


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
        db_engine.execute("INSERT INTO sample_file (sample_id, file_id) VALUES {0} ON CONFLICT DO NOTHING;".format( ','.join(["({0}, {1})".format(samples[sid].id, file_id) for sid in samples])))



        # parsing vcf file
        records_count = vcf_metadata['count']
        records_current = 0
        table = "variant" + db_ref_suffix
        log ("Importing file {0}\n\r\trecords  : {1}\n\r\tsamples  :  ({2}) {3}\n\r\tstart    : {4}".format(filepath, records_count, len(samples.keys()), reprlib.repr([s for s in samples.keys()]), start))
        # bar = Bar('\tparsing  : ', max=records_count, suffix='%(percent).1f%% - %(elapsed_td)s')
        
        sql_pattern1 = "INSERT INTO {0} (chr, pos, ref, alt, is_transition, bin, sample_list) VALUES ({1}, {2}, '{3}', '{4}', {5}, {6}, array[{7}]) ON CONFLICT (chr, pos, ref, alt) DO UPDATE SET sample_list=array_multi_remove({0}.sample_list, array[{7}])  WHERE {0}.chr={1} AND {0}.pos={2} AND {0}.ref='{3}' AND {0}.alt='{4}';"
        sql_pattern2 = "INSERT INTO sample_variant" + db_ref_suffix + " (sample_id, variant_id, bin, chr, pos, ref, alt, genotype, depth) SELECT {0}, id, {1}, '{2}', {3}, '{4}', '{5}', '{6}', {7} FROM variant" + db_ref_suffix + " WHERE bin={1} AND chr={2} AND pos={3} AND ref='{4}' AND alt='{5}' ON CONFLICT DO NOTHING;"
        sql_pattern3 = "INSERT INTO {0} (bin,chr,pos,ref,alt,{1}) VALUES ({3},{4},{5},'{6}','{7}',{2}) ON CONFLICT DO NOTHING;" # TODO : on conflict, shall update fields with value in the VCF ton complete database annotation with (maybe) new fields
        sql_tail = " ON CONFLICT DO NOTHING;"
        sql_query1 = ""
        sql_query2 = ""
        sql_query3 = ""
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
                    if pos is not None and alt != ref :
                        bin = getMaxUcscBin(pos, pos + len(ref))
                        sql_query1 += sql_pattern1.format(table, chrm, pos, ref, alt, is_transition(ref, alt), bin, samples_array)
                        sql_query2 += sql_pattern2.format(samples[sn].id, bin, chrm, pos, ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1

                    pos, ref, alt = normalize(r.pos, r.ref, s.alleles[1])
                    if pos is not None and alt != ref :
                        bin = getMaxUcscBin(pos, pos + len(ref))
                        sql_query1 += sql_pattern1.format(table, chrm, pos, ref, alt, is_transition(ref, alt), bin, samples_array)
                        sql_query2 += sql_pattern2.format(samples[sn].id, bin, chrm, pos, ref, alt, normalize_gt(s), get_info(s, 'DP'))
                        count += 1


                    # Import custom annotation for the variant
                    for ann_name, metadata in vcf_metadata['annotations'].items():
                        for info in r.info[metadata['flag']]:
                            data = info.split('|')
                            q_fields = []
                            q_values = []
                            allele   = ""
                            for col_pos, col_name in enumerate(metadata['columns']):
                                q_fields.append(metadata['db_map'][col_name]['name'])
                                val = escape_value_for_sql(data[col_pos])
                                if col_name == 'Allele':
                                    allele = val.strip().strip("-")
                                q_values.append('\'{}\''.format(val) if val != '' and val is not None else 'NULL')


                            pos, ref, alt = normalize(r.pos, r.ref, s.alleles[0])
                            # print(pos, ref, alt, allele)
                            if pos is not None and alt==allele:
                                # print("ok")
                                sql_query3 += sql_pattern3.format(metadata['table'], ','.join(q_fields), ','.join(q_values), bin, chrm, pos, ref, alt)
                                count += 1
                            pos, ref, alt = normalize(r.pos, r.ref, s.alleles[1])
                            # print(pos, ref, alt, allele)
                            if pos is not None and alt==allele:
                                # print("ok")
                                sql_query3 += sql_pattern3.format(metadata['table'], ','.join(q_fields), ','.join(q_values), bin, chrm, pos, ref, alt)
                                count += 1



                    # manage split big request to avoid sql out of memory transaction
                    if count >= 25000:
                        count = 0
                        log("VCF import : Execute query")
                        # transaction1 = sql_query1
                        # transaction2 = sql_query2
                        # transaction3 = sql_query3
                        # pool.apply_async(exec_sql_query, (transaction1, transaction2, transaction3))
                        session = Session(db_engine)
                        session.execute(sql_query1)
                        session.execute(sql_query2)
                        session.execute(sql_query3)
                        session.commit()
                        session.commit() # Need a second commit to force session to commit :/ ... strange behavior when we execute(raw_sql) instead of using sqlalchemy's objects as query
                        session.close()


                        sql_query1 = ""
                        sql_query2 = ""
                        sql_query3 = ""

        # Loop done, execute last pending query 
        session = Session(db_engine)
        try:
            session.execute(sql_query1)
            session.execute(sql_query2)
            session.execute(sql_query3)
            session.commit()
            session.commit() # Need a second commit to force session to commit :/ ... strange behavior when we execute(raw_sql) instead of using sqlalchemy's objects as query
            session.close()
        except Exception as err:
            ipdb.set_trace()
            log(err)
            if annso_core is not None:
                annso_core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id, 'msg' : 'Error occured : ' + str(err)}})
            session.close()
            return

    end = datetime.datetime.now()
    if annso_core is not None:
        annso_core.notify_all({'msg':'import_vcf_end', 'data' : {'file_id' : file_id, 'msg' : 'Import done without error.', 'samples': [ {'id' : samples[s].id, 'name' : samples[s].name} for s in samples.keys()]}})
