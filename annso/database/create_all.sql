-- 
-- CREATE ALL - V1.0.0
--

--
-- psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"
-- psql -U postgres -c "DROP DATABASE annso"
-- psql -U postgres -c "CREATE DATABASE annso OWNER annso"
-- psql -U postgres -d annso -f database/create_all.sql
--


CREATE TYPE field_type AS ENUM ('int', 'string', 'float', 'percent', 'enum', 'range', 'bool', 'list_i', 'list_s', 'list_f', 'list_p', 'list_b');
CREATE TYPE annotation_db_type AS ENUM ('site', 'variant', 'transcript');


-- CREATE TYPE analysis_status AS ENUM ('SETTING', 'COMPUTING', 'READY', 'CLOSE');




CREATE TABLE public.template
(
    id serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."C.UTF-8",
    author character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text COLLATE pg_catalog."C.UTF-8",
    version character varying(20) COLLATE pg_catalog."C.UTF-8",
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    parent_id integer,
    configuration text COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT template_pkey PRIMARY KEY (id)
);
ALTER TABLE public.template OWNER TO annso;





CREATE TABLE public.analysis
(
    id serial NOT NULL,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments text COLLATE pg_catalog."C.UTF-8",
    template_id integer,
    settings text COLLATE pg_catalog."C.UTF-8",
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    total_variants integer DEFAULT 0,
    status character varying(20) COLLATE pg_catalog."C.UTF-8",
    reference_id integer DEFAULT 2,  -- 2 is for Hg19
    CONSTRAINT analysis_pkey PRIMARY KEY (id),
    CONSTRAINT analysis_template_id_fkey FOREIGN KEY (template_id)
        REFERENCES public."template" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.analysis OWNER TO annso;




CREATE TABLE public.report
(
    id serial NOT NULL,
    analysis_id integer,
    name character varying(255) COLLATE pg_catalog."C.UTF-8",
    path character varying(255) COLLATE pg_catalog."C.UTF-8",
    type character varying(50) COLLATE pg_catalog."C.UTF-8",
    module_id character varying(50) COLLATE pg_catalog."C.UTF-8",
    creation_date timestamp without time zone,
    CONSTRAINT report_pkey PRIMARY KEY (id)
);
ALTER TABLE public.report OWNER TO annso;




CREATE TABLE public.filter
(
    id serial NOT NULL,
    analysis_id integer,
    name character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text COLLATE pg_catalog."C.UTF-8",
    filter text COLLATE pg_catalog."C.UTF-8",
    total_variants integer,
    CONSTRAINT filter_pkey PRIMARY KEY (id),
    CONSTRAINT filter_analysis_id_fkey FOREIGN KEY (analysis_id)
        REFERENCES public."analysis" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.filter OWNER TO annso;













CREATE TABLE public."reference"
(
    id serial NOT NULL,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    description character varying(255) COLLATE pg_catalog."C.UTF-8",
    url character varying(255) COLLATE pg_catalog."C.UTF-8",
    table_suffix character varying(10) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT reference_pkey PRIMARY KEY (id)
);
ALTER TABLE public."reference" OWNER TO annso;





CREATE TABLE public.file
(
    id serial NOT NULL,
    filename character varying(255) COLLATE pg_catalog."C.UTF-8",
    comments text,
    type character varying(10) COLLATE pg_catalog."C.UTF-8",
    "path" character varying(255) COLLATE pg_catalog."C.UTF-8",
    size integer,
    upload_offset integer,
    reference_id integer,
    import_date timestamp without time zone,
    CONSTRAINT file_pkey PRIMARY KEY (id),
    CONSTRAINT file_reference_id_fkey FOREIGN KEY (reference_id)
        REFERENCES public."reference" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.file OWNER TO annso;







CREATE TABLE public.sample
(
    id serial NOT NULL,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments character varying(255) COLLATE pg_catalog."C.UTF-8",
    is_mosaic boolean,
    CONSTRAINT sample_pkey PRIMARY KEY (id)
);
ALTER TABLE public.sample OWNER TO annso;



CREATE TABLE public.sample_file
(
    sample_id integer NOT NULL,
    file_id integer NOT NULL,
    CONSTRAINT sample_file_pkey PRIMARY KEY (sample_id, file_id),
    CONSTRAINT sample_file_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT sample_file_file_id_fkey FOREIGN KEY (file_id)
        REFERENCES public."file" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.sample_file OWNER TO annso;



CREATE TABLE public.analysis_sample
(
    analysis_id integer NOT NULL,
    sample_id integer NOT NULL,
    nickname character varying(255) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT analysis_sample_pkey PRIMARY KEY (analysis_id, sample_id),
    CONSTRAINT analysis_sample_analysis_id_fkey FOREIGN KEY (analysis_id)
        REFERENCES public."analysis" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT analysis_sample_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.analysis_sample OWNER TO annso;


CREATE TABLE public.attribute
(
    analysis_id integer NOT NULL,
    sample_id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    value character varying(255) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT attribute_pkey PRIMARY KEY (analysis_id, sample_id, name),
    CONSTRAINT attribute_analysis_id_fkey FOREIGN KEY (analysis_id)
        REFERENCES public."analysis" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT attribute_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.attribute OWNER TO annso;







CREATE TABLE public.variant_hg19
(
    id bigserial NOT NULL,
    bin integer,
    chr integer,
    pos bigint NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    is_transition boolean,
    sample_list integer[],
    CONSTRAINT variant_hg19_pkey PRIMARY KEY (id),
    CONSTRAINT variant_hg19_ukey UNIQUE (chr, pos, ref, alt)
);
ALTER TABLE public.variant_hg19 OWNER TO annso;






CREATE TABLE public.sample_variant_hg19
(
    sample_id integer NOT NULL,
    bin integer,
    chr integer,
    pos bigint NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    variant_id bigint,
    genotype integer,
    depth integer,
    info character varying(255)[][] COLLATE pg_catalog."C.UTF-8",
    mosaic real,
    CONSTRAINT sample_variant_hg19_pkey PRIMARY KEY (sample_id, chr, pos, ref, alt),
    CONSTRAINT sample_variant_hg19_variant_id_fkey FOREIGN KEY (variant_id)
        REFERENCES public."variant_hg19" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT sample_variant_hg19_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT sample_variant_hg19_ukey UNIQUE (sample_id, variant_id)
);
ALTER TABLE public.sample_variant_hg19 OWNER TO annso;






CREATE TABLE public.annotation_database
(
    uid character varying(32) COLLATE pg_catalog."C.UTF-8",
    reference_id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    version character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name_ui character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text,
    type annotation_db_type,
    ord integer,
    url text ,
    update_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    jointure text,
    db_pk_field_uid character varying(32) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT annotation_database_pkey PRIMARY KEY (reference_id, name, version),
    CONSTRAINT annotation_database_reference_id_fkey FOREIGN KEY (reference_id)
        REFERENCES public."reference" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.annotation_database OWNER TO annso;

CREATE TABLE public.annotation_field
(
    uid character varying(32) COLLATE pg_catalog."C.UTF-8",
    database_uid character varying(32) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name_ui character varying(255) COLLATE pg_catalog."C.UTF-8",
    ord integer,
    description text,
    type field_type,
    meta text,
    wt_default boolean DEFAULT False,
    CONSTRAINT annotation_field_pkey PRIMARY KEY (database_uid, name)
);
ALTER TABLE public.annotation_field OWNER TO annso;





CREATE TABLE public."parameter"
(
    key character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL ,
    value character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    description character varying(255) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT parameter_pkey PRIMARY KEY (key)
);
ALTER TABLE public."parameter" OWNER TO annso;








--
-- INDEXES
--
DROP INDEX IF EXISTS public.sample_idx;
CREATE INDEX sample_idx
  ON public.sample
  USING btree
  (id);




DROP INDEX IF EXISTS public.sample_variant_hg19_idx_id;
CREATE INDEX sample_variant_hg19_idx_id
  ON public.sample_variant_hg19
  USING btree
  (variant_id);

DROP INDEX IF EXISTS public.sample_variant_hg19_idx_samplevar;
CREATE INDEX sample_variant_hg19_idx_samplevar
  ON public.sample_variant_hg19
  USING btree
  (sample_id);

DROP INDEX IF EXISTS public.sample_variant_hg19_idx_site;
CREATE INDEX sample_variant_hg19_idx_site
  ON public.sample_variant_hg19
  USING btree
  (sample_id, bin, chr, pos);


DROP INDEX IF EXISTS public.attribute_idx;
CREATE INDEX attribute_idx
  ON public.attribute
  USING btree
  (analysis_id, sample_id, name COLLATE pg_catalog."default");




DROP INDEX IF EXISTS public.variant_hg19_idx_id;
CREATE INDEX variant_hg19_idx_id
  ON public.variant_hg19
  USING btree
  (id);

DROP INDEX IF EXISTS public.variant_hg19_idx_site;
CREATE INDEX variant_hg19_idx_site
  ON public.variant_hg19
  USING btree
  (bin, chr, pos);


DROP INDEX IF EXISTS public.analysis_idx;
CREATE INDEX analysis_idx
  ON public.analysis
  USING btree
  (id);




DROP INDEX IF EXISTS public.filter_idx;
CREATE INDEX filter_idx
  ON public.filter
  USING btree
  (id);
    


DROP INDEX IF EXISTS public.annotation_database_idx;
CREATE INDEX annotation_database_idx
  ON public.annotation_database
  USING btree
  (reference_id, name, version);
DROP INDEX IF EXISTS public.annotation_database_idx2;
CREATE INDEX annotation_database_idx2
  ON public.annotation_database
  USING btree (uid);

DROP INDEX IF EXISTS public.annotation_field_idx;
CREATE INDEX annotation_field_idx
  ON public.annotation_field
  USING btree
  (database_uid, name);
DROP INDEX IF EXISTS public.annotation_field_idx2;
CREATE INDEX annotation_field_idx2
  ON public.annotation_field
  USING btree (uid);


--
-- INIT DATA
--
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



INSERT INTO public.reference(id, name, description, url, table_suffix) VALUES 
  (1, 'Hg18', 'Human Genom version 18', 'http://hgdownload.cse.ucsc.edu/goldenpath/hg18/chromosomes/', 'hg18'),
  (2, 'Hg19', 'Human Genom version 19', 'http://hgdownload.cse.ucsc.edu/goldenpath/hg19/chromosomes/', 'hg19'),
  (3, 'Hg38', 'Human Genom version 38', 'http://hgdownload.cse.ucsc.edu/goldenpath/hg19/chromosomes/', 'hg38');



CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO public."parameter" (key, description, value) VALUES
    ('database_version',          'The current version of the database',           'V1.0.0'),
    ('heavy_client_last_version', 'Oldest complient version of the heavy client',  'V1.0.0'),
    ('backup_date',               'The date of the last database dump',            to_char(current_timestamp, 'YYYY-MM-DD')),
    ('stats_refresh_date',        'The date of the last refresh of statistics',    to_char(current_timestamp, 'YYYY-MM-DD'));






-- 8beee586e1cd098bc64b48403ed7755d = SELECT MD5(concat(reference_id=1, name='Variant', version=NULL))
-- d9121852fc1a279b95cb7e18c976f112 = SELECT MD5(concat(reference_id=2, name='Variant', version=NULL))
-- 7363e34fee56d2cb43583f9bd19d3980 = SELECT MD5(concat(reference_id=3, name='Variant', version=NULL))
INSERT INTO public.annotation_database(uid, reference_id, name, version, name_ui, description, url, ord, update_date, jointure, type) VALUES
  ('8beee586e1cd098bc64b48403ed7755d', 1, 'sample_variant_hg18', '', 'Variant', 'Basic information about the variant.', '',  0, CURRENT_TIMESTAMP, 'sample_variant_hg18', 'variant'),
  ('d9121852fc1a279b95cb7e18c976f112', 2, 'sample_variant_hg19', '', 'Variant', 'Basic information about the variant.', '',  0, CURRENT_TIMESTAMP, 'sample_variant_hg19', 'variant'),
  ('7363e34fee56d2cb43583f9bd19d3980', 3, 'sample_variant_hg38', '', 'Variant', 'Basic information about the variant.', '',  0, CURRENT_TIMESTAMP, 'sample_variant_hg38', 'variant');


INSERT INTO public.annotation_field(database_uid, ord, wt_default, name, name_ui, type, description, meta) VALUES
  ('8beee586e1cd098bc64b48403ed7755d', 1,  True, 'variant_id','id',     'int',    'Variant unique id in the database.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 3,  True, 'chr',       'chr',    'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  ('8beee586e1cd098bc64b48403ed7755d', 4,  True, 'pos',       'pos',    'int',    'Position of the variant in the chromosome.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 5,  True, 'ref',       'ref',    'string', 'Reference sequence.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 6,  True, 'alt',       'alt',    'string', 'Alternative sequence of the variant.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 7,  True, 'sample_tlist',  'samples total',          'string', 'List of sample (whole database) that have the variant.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 8,  True, 'sample_tcount', 'samples total count',    'int',    'Number of sample (whole database) that have the variant.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 9,  True, 'sample_alist',  'samples analysis',       'string', 'List of sample (in the analysis) that have the variant.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 10, True, 'sample_acount', 'samples analysis count', 'int',    'Number of sample (in the analysis) that have the variant.', NULL),
  ('8beee586e1cd098bc64b48403ed7755d', 20, True, 's{}_gt',    'GT',     'enum',   'Genotype.', '{"enum" : {"0":"ref/ref", "1":"alt/alt", "2":"ref/alt", "3":"alt1/alt2"}}'),
  ('8beee586e1cd098bc64b48403ed7755d', 30, True, 's{}_dp',    'DP',     'float',  'Depth.', NULL);

INSERT INTO public.annotation_field(database_uid, ord, wt_default, name, name_ui, type, description, meta) VALUES
  ('d9121852fc1a279b95cb7e18c976f112', 1,  True, 'variant_id','id',     'int',    'Variant unique id in the database.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 3,  True, 'chr',       'chr',    'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  ('d9121852fc1a279b95cb7e18c976f112', 4,  True, 'pos',       'pos',    'int',    'Position of the variant in the chromosome.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 5,  True, 'ref',       'ref',    'string', 'Reference sequence.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 6,  True, 'alt',       'alt',    'string', 'Alternative sequence of the variant.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 7,  True, 'sample_tlist',  'samples total',          'string', 'List of sample (whole database) that have the variant.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 8,  True, 'sample_tcount', 'samples total count',    'int',    'Number of sample (whole database) that have the variant.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 9,  True, 'sample_alist',  'samples analysis',       'string', 'List of sample (in the analysis) that have the variant.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 10, True, 'sample_acount', 'samples analysis count', 'int',    'Number of sample (in the analysis) that have the variant.', NULL),
  ('d9121852fc1a279b95cb7e18c976f112', 20, True, 's{}_gt',    'GT',     'enum',   'Genotype.', '{"enum" : {"0":"ref/ref", "1":"alt/alt", "2":"ref/alt", "3":"alt1/alt2"}}'),
  ('d9121852fc1a279b95cb7e18c976f112', 30, True, 's{}_dp',    'DP',     'float',  'Depth.', NULL);

INSERT INTO public.annotation_field(database_uid, ord, wt_default, name, name_ui, type, description, meta) VALUES
  ('7363e34fee56d2cb43583f9bd19d3980', 1,  True, 'variant_id','id',     'int',    'Variant unique id in the database.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 3,  True, 'chr',       'chr',    'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  ('7363e34fee56d2cb43583f9bd19d3980', 4,  True, 'pos',       'pos',    'int',    'Position of the variant in the chromosome.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 5,  True, 'ref',       'ref',    'string', 'Reference sequence.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 6,  True, 'alt',       'alt',    'string', 'Alternative sequence of the variant.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 7,  True, 'sample_tlist',  'samples total',          'string', 'List of sample (whole database) that have the variant.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 8,  True, 'sample_tcount', 'samples total count',    'int',    'Number of sample (whole database) that have the variant.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 9,  True, 'sample_alist',  'samples analysis',       'string', 'List of sample (in the analysis) that have the variant.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 10, True, 'sample_acount', 'samples analysis count', 'int',    'Number of sample (in the analysis) that have the variant.', NULL),
  ('7363e34fee56d2cb43583f9bd19d3980', 20, True, 's{}_gt',    'GT',     'enum',   'Genotype.', '{"enum" : {"0":"ref/ref", "1":"alt/alt", "2":"ref/alt", "3":"alt1/alt2"}}'),
  ('7363e34fee56d2cb43583f9bd19d3980', 30, True, 's{}_dp',    'DP',     'float',  'Depth.', NULL);


UPDATE annotation_field SET uid=MD5(concat(database_uid, name));





















-- --------------------------------------------
-- FUNCTIONS
-- --------------------------------------------
-- Return array with element that occure in both input arrays
CREATE OR REPLACE FUNCTION array_intersect(anyarray, anyarray)
  RETURNS integer ARRAY
  LANGUAGE sql
AS $FUNCTION$
    SELECT ARRAY(
      SELECT UNNEST($1)
      INTERSECT
      SELECT UNNEST($2)
    );
$FUNCTION$;


-- Remove all occurence elements from an array into another one 
CREATE OR REPLACE FUNCTION array_multi_remove(integer[], integer[])
  RETURNS integer ARRAY
  LANGUAGE plpgsql
AS $FUNCTION$
  DECLARE
    source ALIAS FOR $1;
    to_remove ALIAS FOR $2;
  BEGIN
    FOR i IN array_lower(to_remove, 1)..array_upper(to_remove, 1) LOOP
      source := array_remove(source, to_remove[i]);
    END LOOP;
  RETURN source;
  END;
$FUNCTION$;


-- return index position (1-based) of an element into an array
CREATE OR REPLACE FUNCTION array_search(needle ANYELEMENT, haystack ANYARRAY)
RETURNS INT AS $$
    SELECT i
      FROM generate_subscripts($2, 1) AS i
     WHERE $2[i] = $1
  ORDER BY i
$$ LANGUAGE sql STABLE;



-- keep element in the first array if equivalent bool in the second array is true
CREATE OR REPLACE FUNCTION array_mask(anyarray, boolean[])
RETURNS anyarray AS $$ 
SELECT ARRAY(SELECT $1[i] 
  FROM generate_subscripts($1,1) g(i)
  WHERE $2[i])
$$ LANGUAGE sql;