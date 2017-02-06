-- 
-- CREATE ALL - V1.0.0
--

--
-- psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"
-- psql -U postgres -c "DROP DATABASE annso"
-- psql -U postgres -c "CREATE DATABASE annso OWNER annso"
-- psql -U postgres -d annso -f database/create_all.sql
--


CREATE TYPE field_type AS ENUM ('int', 'string', 'float', 'percent', 'enum', 'range', 'bool');





CREATE TABLE public.template
(
    id serial NOT NULL,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
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
    CONSTRAINT analysis_pkey PRIMARY KEY (id),
    CONSTRAINT analysis_template_id_fkey FOREIGN KEY (template_id)
        REFERENCES public."template" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.analysis OWNER TO annso;





CREATE TABLE public.filter
(
    id serial NOT NULL,
    analysis_id integer,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
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
    filename character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments character varying(255) COLLATE pg_catalog."C.UTF-8",
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
    caller_list character varying(50)[] COLLATE pg_catalog."C.UTF-8",
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
    genotype character varying(1),
    depth integer,
    info character varying(255)[][] COLLATE pg_catalog."C.UTF-8",
    mosaic real,
    CONSTRAINT sample_variant_hg19_pkey PRIMARY KEY (sample_id, chr, pos, ref, alt),
    CONSTRAINT sample_variant_hg19_variant_id_fkey FOREIGN KEY (variant_id)
        REFERENCES public."variant_hg19" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT sample_variant_hg19_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.variant_hg19 OWNER TO annso;






CREATE TABLE public.annotation_database
(
    id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name_ui character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text,
    reference_id integer,
    url character varying(255) COLLATE pg_catalog."C.UTF-8" ,
    update_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    jointure character varying(255) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT annotation_database_pkey PRIMARY KEY (id),
    CONSTRAINT annotation_database_reference_id_fkey FOREIGN KEY (reference_id)
        REFERENCES public."reference" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER TABLE public.annotation_database OWNER TO annso;





CREATE TABLE public.annotation_field
(
    id integer NOT NULL,
    database_id integer,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name_ui character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text,
    type field_type,
    meta character varying(1000) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT annotation_field_pkey PRIMARY KEY (id),
    CONSTRAINT annotation_field_database_id_fkey FOREIGN KEY (database_id)
        REFERENCES public."annotation_database" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
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
    






--
-- INIT DATA
--
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



INSERT INTO public.reference(name, description, url, table_suffix)
VALUES ('Human Genom 19', 'Human Genom version 19', 'http://hgdownload.cse.ucsc.edu/goldenpath/hg19/chromosomes/', 'hg19');



CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO public."parameter" (key, description, value) VALUES
    ('database_version',          'The current version of the database',           'V1.0.0'),
    ('heavy_client_last_version', 'Oldest complient version of the heavy client',  'V1.0.0'),
    ('backup_date',               'The date of the last database dump',            to_char(current_timestamp, 'YYYY-MM-DD')),
    ('stats_refresh_date',        'The date of the last refresh of statistics',    to_char(current_timestamp, 'YYYY-MM-DD'));




-- DB_id              : 1
-- Field ids reserved : 1-50

INSERT INTO public.annotation_database(id, name, name_ui, description, url, reference_id, update_date, jointure) VALUES
  (1, 'sample_variant_hg19', 
  'Variant', 
  'Basic information about the variant.', 
  '', 
  1, 
  CURRENT_TIMESTAMP, 
  'sample_variant_hg19');

INSERT INTO public.annotation_field(database_id, id, name, name_ui, type, description, meta) VALUES
  (1, 1, 'sample_id', 'sample', 'int',    'Sample that have the variant.', NULL),
  (1, 2, 'variant_id','id',     'int',    'Variant unique id in the database.', NULL),
  (1, 3, 'chr',       'chr',    'enum',   'Chromosome.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (1, 4, 'pos',       'pos',    'int',    'Position of the variant in the chromosome.', NULL),
  (1, 5, 'ref',       'ref',    'string', 'Reference sequence.', NULL),
  (1, 6, 'alt',       'alt',    'string', 'Alternative sequence of the variant.', NULL),
  (1, 7, 'genotype',  'GT',     'enum',   'Genotype.', '{"enum" : {"0":"ref/ref", "1":"alt/alt", "2":"ref/alt", "3":"alt1/alt2"}}'),
  (1, 8, 'depth',     'DP',     'float',  'Depth.', NULL);





