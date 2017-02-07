


--
-- Import csv data
--
DROP TABLE IF EXISTS public.import_refgene_hg19;
CREATE TABLE public.import_refgene_hg19
(
  bin integer,
  name character varying(255),
  chrom character varying(255),
  strand character(1),
  txstart bigint,
  txend bigint,
  cdsstart bigint,
  cdsend bigint,
  exoncount bigint,
  exonstarts text,
  exonends text,
  score bigint,
  name2 character varying(255),
  cdsstartstat character varying(255),
  cdsendstat character varying(255),
  exonframes text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.import_refgene_hg19
  OWNER TO annso;


COPY import_refgene_hg19 FROM '/var/regovar/data/db/refgen/refGene.txt' DELIMITER E'\t' CSV;









--
-- Create Annso tables for refgene data
--
DROP TABLE IF EXISTS public.refgene_hg19;
CREATE TABLE public.refgene_hg19
(
  bin integer NOT NULL,
  name character varying(255),
  chr integer,
  strand character(1),
  txstart bigint,
  txend bigint,
  txrange int8range,
  cdsstart bigint,
  cdsend bigint,
  cdsrange int8range,
  exoncount bigint,
  score bigint,
  name2 character varying(255),
  cdsstartstat character varying(255),
  cdsendstat character varying(255)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.refgene_hg19
  OWNER TO annso;



DROP TABLE IF EXISTS public.refgene_exon_hg19;
CREATE TABLE public.refgene_exon_hg19
(
  bin integer NOT NULL,
  name character varying(255),
  chr integer,
  strand character(1),
  txstart bigint,
  txend bigint,
  txrange int8range,
  cdsstart bigint,
  cdsend bigint,
  cdsrange int8range,
  i_exonstart character varying(255),
  i_exonend character varying(255),
  exoncount bigint,
  exonstart bigint,
  exonend bigint,
  exonrange int8range,
  score bigint,
  name2 character varying(255),
  cdsstartstat character varying(255),
  cdsendstat character varying(255)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.refgene_exon_hg19
  OWNER TO annso;


-- DROP INDEX IF EXISTS public.refgene_hg19_id_seq;
-- CREATE SEQUENCE public.refgene_hg19_id_seq
--   INCREMENT 1
--   MINVALUE 1
--   MAXVALUE 9223372036854775807
--   START 1
--   CACHE 1;
-- ALTER TABLE public.refgene_hg19_id_seq
--   OWNER TO annso;

-- ALTER TABLE public.refgene_hg19 ADD txrange int8range;
-- ALTER TABLE public.refgene_hg19 ADD id integer NOT NULL DEFAULT nextval('refgene_hg19_id_seq'::regclass);
-- ALTER TABLE public.refgene_hg19 ADD variant_ids integer[][];








--
-- Migrate imported data to annso database
--
INSERT INTO public.refgene_hg19(bin, name, chr, strand, txstart, txend, txrange, cdsstart, cdsend, cdsrange, exoncount, score, name2, cdsstartstat, cdsendstat)
SELECT bin, name, 
  CASE WHEN chrom='chrX' THEN 23 WHEN chrom='chrY' THEN 24 WHEN chrom='chrM' THEN 25 ELSE CAST(substring(chrom from 4) AS INTEGER) END, 
  strand, txstart, txend, int8range(txstart, txend), cdsstart, cdsend, int8range(cdsstart, cdsend), exoncount, score, name2, cdsstartstat, cdsendstat
FROM import_refgene_hg19
WHERE char_length(chrom) <= 5;


INSERT INTO public.refgene_exon_hg19(bin, name, chr, strand, txstart, txend, txrange, cdsstart, cdsend, cdsrange, exoncount, i_exonstart, i_exonend, score, name2, cdsstartstat, cdsendstat)
SELECT bin, name,
  CASE WHEN chrom='chrX' THEN 23 WHEN chrom='chrY' THEN 24 WHEN chrom='chrM' THEN 25 ELSE CAST(substring(chrom from 4) AS INTEGER) END,
  strand, txstart, txend, int8range(txstart, txend), cdsstart, cdsend, int8range(cdsstart, cdsend), exoncount, unnest(string_to_array(trim(trailing ',' from exonstarts), ',')), unnest(string_to_array(trim(trailing ',' from exonends), ',')), score, name2, cdsstartstat, cdsendstat
FROM import_refgene_hg19
WHERE char_length(chrom) <= 5;



UPDATE public.refgene_exon_hg19 SET 
  exonstart=CAST(coalesce(i_exonstart, '0') AS integer),
  exonend  =CAST(coalesce(i_exonend,   '0') AS integer),
  exonrange=int8range(CAST(coalesce(i_exonstart, '0') AS integer), CAST(coalesce(i_exonend, '0') AS integer)) ;



ALTER TABLE public.refgene_exon_hg19 DROP COLUMN i_exonstart;
ALTER TABLE public.refgene_exon_hg19 DROP COLUMN i_exonend;






  
  
--
-- Compute/Set additional fields 
--
-- UPDATE public.refgene_hg19 SET variant_ids=ids
-- FROM (
--     SELECT rg.id as rid, array_agg(v.id) as ids
--     FROM public.variant_hg19 v
--     LEFT JOIN public.refgene_hg19 rg ON rg.txrange @> int8(v.pos)
--     GROUP BY rg.id
-- ) as SR
-- WHERE id=rid



--
-- Create indexes
--
DROP INDEX IF EXISTS public.refgene_hg19_chrom_txrange_idx;
CREATE INDEX refgene_hg19_chrom_txrange_idx
  ON public.refgene_hg19
  USING btree (bin, chr, txrange);


DROP INDEX IF EXISTS public.refgene_hg19_txrange_idx;
CREATE INDEX refgene_hg19_txrange_idx
  ON public.refgene_hg19
  USING gist (txrange);




DROP INDEX IF EXISTS public.refgene_exon_hg19_chrom_exonange_idx;
CREATE INDEX refgene_exon_hg19_chrom_exonange_idx
  ON public.refgene_exon_hg19
  USING btree (bin, chr, exonrange);


DROP INDEX IF EXISTS public.refgene_exon_hg19_exonange_idx;
CREATE INDEX refgene_exon_hg19_exonange_idx
  ON public.refgene_exon_hg19
  USING gist (exonrange);



--
-- Register refGen into annso database
-- 
-- DB_id              : 2 & 3
-- Field ids reserved : 51-100

INSERT INTO public.annotation_database(id, name, name_ui, description, url, reference_id, update_date, jointure) VALUES
  (2, 'refgene_hg19', 
  'refGene', 
  'Known human protein-coding and non-protein-coding genes taken from the NCBI RNA reference sequences collection (RefSeq).', 
  'http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz', 
  1, 
  CURRENT_TIMESTAMP, 
  'refgene_hg19 ON {0}.bin=refgene_hg19.bin AND {0}.chr=refgene_hg19.chr AND refgene_hg19.txrange @> int8({0}.pos)'),

  (3, 'refgene_exon_hg19', 
  'refGeneExon', 
  'Known human protein-coding and non-protein-coding genes taken from the NCBI RNA reference sequences collection (RefSeq). This database contains all exome regions of the refSeq genes.', 
  'http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz', 
  1, 
  CURRENT_TIMESTAMP, 
  'refgene_exon_hg19 ON {0}.bin=refgene_hg19.bin AND {0}.chr=refgene_exon_hg19.chr AND refgene_exon_hg19.exonrange @> int8({0}.pos)');



INSERT INTO public.annotation_field(database_id, id, name, name_ui, type, description, meta) VALUES
  (2, 51, 'name',         'name',         'string', 'Gene name.', NULL),
  (2, 52, 'chr',          'chr',          'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (2, 53, 'strand',       'strand',       'string', 'Which DNA strand contains the observed alleles.', NULL),
  (2, 54, 'txstart',      'txstart',      'int',    'Transcription start position.', NULL),
  (2, 55, 'txend',        'txend',        'int',    'Transcription end position.', NULL),
  (2, 56, 'txrange',      'txrange',      'range',  'Transcription region [start-end].', NULL),
  (2, 57, 'cdsstart',     'cdsstart',     'int',    'Coding region start.', NULL),
  (2, 58, 'cdsend',       'cdsend',       'int',    'Coding region end.', NULL),
  (2, 59, 'cdsrange',     'cdsrange',     'range',  'Coding region [start-end].', NULL),
  (2, 60, 'exoncount',    'exoncount',    'int',    'Number of exons in the gene.', NULL),
  (2, 61, 'score',        'score',        'int',    'Score ?', NULL),
  (2, 62, 'name2',        'name2',        'string', 'Alternative name.', NULL),
  (2, 63, 'cdsstartstat', 'cdsstartstat', 'string', 'Cds start stat, can be "non", "unk", "incompl" or "cmp1".', NULL),
  (2, 64, 'cdsendstat',   'cdsendstat',   'string', 'Cds end stat, can be "non", "unk", "incompl" or "cmp1".', NULL),
  (3, 65, 'name',         'name',         'string', 'Gene name.', NULL),
  (3, 66, 'chr',          'chr',          'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (3, 67, 'strand',       'strand',       'string', 'Which DNA strand contains the observed alleles.', NULL),
  (3, 68, 'txstart',      'txstart',      'int',    'Transcription start position.', NULL),
  (3, 69, 'txend',        'txend',        'int',    'Transcription end position.', NULL),
  (3, 70, 'txrange',      'txrange',      'range',  'Transcription region [start-end].', NULL),
  (3, 71, 'cdsstart',     'cdsstart',     'int',    'Coding region start.', NULL),
  (3, 72, 'cdsend',       'cdsend',       'int',    'Coding region end.', NULL),
  (3, 73, 'cdsrange',     'cdsrange',     'range',  'Coding region [start-end].', NULL),
  (3, 74, 'exoncount',    'exoncount',    'int',    'Number of exons in the gene.', NULL),
  (3, 75, 'exonstart',    'exonstart',    'int',    'Exon start position.', NULL),
  (3, 76, 'exonend',      'exonend',      'int',    'Exon end position.', NULL),
  (3, 77, 'exonrange',    'exonrange',    'range',  'Exon region [start-end].', NULL),
  (3, 78, 'score',        'score',        'int',    'Score ?', NULL),
  (3, 79, 'name2',        'name2',        'string', 'Alternative name.', NULL),
  (3, 80, 'cdsstartstat', 'cdsstartstat', 'string', 'Cds start stat, can be "non", "unk", "incompl" or "cmp1".', NULL),
  (3, 81, 'cdsendstat',   'cdsendstat',   'string', 'Cds end stat, can be "non", "unk", "incompl" or "cmp1".', NULL);
