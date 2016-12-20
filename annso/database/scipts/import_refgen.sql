


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


COPY import_refgene_hg19 FROM '/tmp/hg19_db/refGene.txt' DELIMITER E'\t' CSV;









--
-- Create Annso tables for refgene data
--
DROP TABLE IF EXISTS public.refgene_hg19;
CREATE TABLE public.refgene_hg19_id_seq
(
  bin integer NOT NULL,
  name character varying(255),
  chr character varying(255),
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
  chr character varying(255),
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
SELECT bin, name, chrom, strand, txstart, txend, int8range(txstart, txend), cdsstart, cdsend, int8range(cdsstart, cdsend), exoncount, score, name2, cdsstartstat, cdsendstat
FROM import_refgene_hg19


INSERT INTO public.refgene_exon_hg19(bin, name, chr, strand, txstart, txend, txrange, cdsstart, cdsend, cdsrange, exoncount, i_exonstart, i_exonend, score, name2, cdsstartstat, cdsendstat)
SELECT bin, name, chrom, strand, txstart, txend, int8range(txstart, txend), cdsstart, cdsend, int8range(cdsstart, cdsend), exoncount, unnest(string_to_array(trim(trailing ',' from exonstarts), ',')), unnest(string_to_array(trim(trailing ',' from exonends), ',')), score, name2, cdsstartstat, cdsendstat
FROM import_refgene_hg19



UPDATE public.refgene_exon_hg19 SET 
  exonstart=CAST(coalesce(i_exonstart, '0') AS integer),
  exonend  =CAST(coalesce(i_exonend,   '0') AS integer),
  exonrange=int8range(CAST(coalesce(i_exonstart, '0') AS integer), CAST(coalesce(i_exonend, '0') AS integer)) 



ALTER TABLE public.refgene_exon_hg19 DROP COLUMN i_exonstart
ALTER TABLE public.refgene_exon_hg19 DROP COLUMN i_exonend






  
  
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
  USING btree
  (chr COLLATE pg_catalog."default", txrange);


DROP INDEX IF EXISTS public.refgene_hg19_txrange_idx;
CREATE INDEX refgene_hg19_txrange_idx
  ON public.refgene_hg19
  USING gist
  (txrange);




DROP INDEX IF EXISTS public.refgene_exon_hg19_chrom_exonange_idx;
CREATE INDEX refgene_exon_hg19_chrom_exonange_idx
  ON public.refgene_exon_hg19
  USING btree
  (chr COLLATE pg_catalog."default", exonrange);


DROP INDEX IF EXISTS public.refgene_exon_hg19_exonange_idx;
CREATE INDEX refgene_exon_hg19_exonange_idx
  ON public.refgene_exon_hg19
  USING gist
  (exonrange);



--
-- Register refGen into annso database
-- 
INSERT INTO public.annotation_database(name, name_ui, description, url, reference_id, update_date, jointure) VALUES
  ('refgene_hg19', 
  'refGene', 
  'Known human protein-coding and non-protein-coding genes taken from the NCBI RNA reference sequences collection (RefSeq). This database contains all exome regions of the refSeq genes.', 
  'http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz', 
  1, 
  CURRENT_TIMESTAMP, 
  'refgene_hg19 {1} ON {0}.chr == {1}.chr AND {1}.txrange @> int8({0}.pos)'),

  ('refgene_exon_hg19', 
  'refGeneExon', 
  'Known human protein-coding and non-protein-coding genes taken from the NCBI RNA reference sequences collection (RefSeq).', 
  'http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz', 
  1, 
  CURRENT_TIMESTAMP, 
  'refgene_exon_hg19 {1} ON {0}.chr == {1}.chr AND {1}.exonrange @> int8({0}.pos)');



INSERT INTO public.annotation_field(database_id, name, name_ui, type, description) VALUES
  (1, 'bin',          'bin',          'int',    ''),
  (1, 'name',         'name',         'string', 'Gene name.'),
  (1, 'chr',          'chr',          'string', 'Chromosome.'),
  (1, 'strand',       'strand',       'string', 'Which DNA strand contains the observed alleles.'),
  (1, 'txstart',      'txstart',      'int',    'Transcription start position.'),
  (1, 'txend',        'txend',        'int',    'Transcription end position.'),
  (1, 'txrange',      'txrange',      'range',  'Transcription region [start-end].'),
  (1, 'cdsstart',     'cdsstart',     'int',    'Coding region start.'),
  (1, 'cdsend',       'cdsend',       'int',    'Coding region end.'),
  (1, 'cdsrange',     'cdsrange',     'range',  'Coding region [start-end].'),
  (1, 'exoncount',    'exoncount',    'int',    'Number of exons in the gene.'),
  (1, 'score',        'score',        'int',    'Score ?'),
  (1, 'name2',        'name2',        'string', 'Alternative name.'),
  (1, 'cdsstartstat', 'cdsstartstat', 'string', 'Cds start stat, can be "non", "unk", "incompl" or "cmp1".'),
  (1, 'cdsendstat',   'cdsendstat',   'string', 'Cds end stat, can be "non", "unk", "incompl" or "cmp1".'),
  (2, 'bin',          'bin',          'int',    ''),
  (2, 'name',         'name',         'string', 'Gene name.'),
  (2, 'chr',          'chr',          'string', 'Chromosome.'),
  (2, 'strand',       'strand',       'string', 'Which DNA strand contains the observed alleles.'),
  (2, 'txstart',      'txstart',      'int',    'Transcription start position.'),
  (2, 'txend',        'txend',        'int',    'Transcription end position.'),
  (2, 'txrange',      'txrange',      'range',  'Transcription region [start-end].'),
  (2, 'cdsstart',     'cdsstart',     'int',    'Coding region start.'),
  (2, 'cdsend',       'cdsend',       'int',    'Coding region end.'),
  (2, 'cdsrange',     'cdsrange',     'range',  'Coding region [start-end].'),
  (2, 'exoncount',    'exoncount',    'int',    'Number of exons in the gene.'),
  (2, 'exonstart',    'exonstart',    'int',    'Exon start position.'),
  (2, 'exonend',      'exonend',      'int',    'Exon end position.'),
  (2, 'exonrange',    'exonrange',    'range',  'Exon region [start-end].'),
  (2, 'score',        'score',        'int',    'Score ?'),
  (2, 'name2',        'name2',        'string', 'Alternative name.'),
  (2, 'cdsstartstat', 'cdsstartstat', 'string', 'Cds start stat, can be "non", "unk", "incompl" or "cmp1".'),
  (2, 'cdsendstat',   'cdsendstat',   'string', 'Cds end stat, can be "non", "unk", "incompl" or "cmp1".')

  