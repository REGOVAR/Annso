-- 
-- CREATE ALL - V1.0.0
--

--
-- psql -U postgres -d annso -f database/create_all.sql
--


CREATE TYPE field_type AS ENUM ('int', 'string', 'float', 'range');






CREATE SEQUENCE public.template_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.template_id_seq OWNER TO annso;
CREATE TABLE public.template
(
    id integer NOT NULL DEFAULT nextval('template_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    author character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text COLLATE pg_catalog."C.UTF-8",
    version character varying(20) COLLATE pg_catalog."C.UTF-8",
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    parent_id integer,
    configuration text COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT template_pkey PRIMARY KEY (id)
)
WITH ( OIDS=FALSE );
ALTER TABLE public.template OWNER TO annso;





CREATE SEQUENCE public.analysis_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.analysis_id_seq OWNER TO annso;
CREATE TABLE public.analysis
(
    id integer NOT NULL DEFAULT nextval('analysis_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments text COLLATE pg_catalog."C.UTF-8",
    template_id integer,
    template_settings text COLLATE pg_catalog."C.UTF-8",
    creation_date timestamp without time zone,
    update_date timestamp without time zone,
    CONSTRAINT analysis_pkey PRIMARY KEY (id),
    CONSTRAINT analysis_template_id_fkey FOREIGN KEY (template_id)
        REFERENCES public."template" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH ( OIDS=FALSE );
ALTER TABLE public.analysis OWNER TO annso;




CREATE SEQUENCE public.selection_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.selection_id_seq OWNER TO annso;
CREATE TABLE public.selection
(
    id integer NOT NULL DEFAULT nextval('selection_id_seq'::regclass),
    analysis_id integer,
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    description text COLLATE pg_catalog."C.UTF-8",
    filter text COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT selection_pkey PRIMARY KEY (id),
    CONSTRAINT selection_analysis_id_fkey FOREIGN KEY (analysis_id)
        REFERENCES public."analysis" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH ( OIDS=FALSE );
ALTER TABLE public.selection OWNER TO annso;













CREATE SEQUENCE public.reference_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.reference_id_seq OWNER TO annso;
CREATE TABLE public."reference"
(
    id integer NOT NULL DEFAULT nextval('reference_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    description character varying(255) COLLATE pg_catalog."C.UTF-8",
    url character varying(255) COLLATE pg_catalog."C.UTF-8",
    table_suffix character varying(10) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT reference_pkey PRIMARY KEY (id)
)
WITH ( OIDS=FALSE );
ALTER TABLE public."reference" OWNER TO annso;




CREATE SEQUENCE public.file_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.file_id_seq OWNER TO annso;
CREATE TABLE public.file
(
    id integer NOT NULL DEFAULT nextval('file_id_seq'::regclass),
    filename character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments character varying(255) COLLATE pg_catalog."C.UTF-8",
    type character varying(10) COLLATE pg_catalog."C.UTF-8",
    reference_id integer,
    import_date timestamp without time zone,
    CONSTRAINT file_pkey PRIMARY KEY (id),
    CONSTRAINT file_reference_id_fkey FOREIGN KEY (reference_id)
        REFERENCES public."reference" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH ( OIDS=FALSE );
ALTER TABLE public.file OWNER TO annso;








CREATE SEQUENCE public.sample_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.sample_id_seq OWNER TO annso;
CREATE TABLE public.sample
(
    id integer NOT NULL DEFAULT nextval('sample_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."C.UTF-8",
    comments character varying(255) COLLATE pg_catalog."C.UTF-8",
    is_mosaic boolean,
    CONSTRAINT sample_pkey PRIMARY KEY (id)
)
WITH ( OIDS=FALSE );
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
)
WITH ( OIDS=FALSE );
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
)
WITH ( OIDS=FALSE );
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
)
WITH ( OIDS=FALSE );
ALTER TABLE public.attribute OWNER TO annso;






CREATE SEQUENCE public.variant_hg19_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.variant_hg19_id_seq OWNER TO annso;
CREATE TABLE public.variant_hg19
(
    id integer NOT NULL DEFAULT nextval('variant_hg19_id_seq'::regclass),
    bin integer,
    chr character varying(50) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    pos integer NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    is_transition boolean,

    sample_list integer[],
    caller_list character varying(50)[] COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT variant_hg19_pkey PRIMARY KEY (id),
    CONSTRAINT variant_hg19_ukey UNIQUE (chr, pos, ref, alt)
)
WITH ( OIDS=FALSE );
ALTER TABLE public.variant_hg19 OWNER TO annso;






CREATE TABLE public.sample_variant_hg19
(
    sample_id integer NOT NULL,
    bin integer,
    chr character varying(50) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    pos integer NOT NULL,
    ref text NOT NULL,
    alt text NOT NULL,
    variant_id integer,
    genotype character varying(1),
    deepth integer,
    info character varying(255)[][] COLLATE pg_catalog."C.UTF-8",
    mosaic real,
    CONSTRAINT sample_variant_hg19_pkey PRIMARY KEY (sample_id, chr, pos, ref, alt),
    CONSTRAINT sample_variant_hg19_variant_id_fkey FOREIGN KEY (variant_id)
        REFERENCES public."variant_hg19" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT sample_variant_hg19_sample_id_fkey FOREIGN KEY (sample_id)
        REFERENCES public."sample" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH ( OIDS=FALSE );
ALTER TABLE public.variant_hg19 OWNER TO annso;






CREATE SEQUENCE public.annotation_database_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;
ALTER TABLE public.annotation_database_id_seq OWNER TO annso;
CREATE TABLE public.annotation_database
(
    id integer NOT NULL DEFAULT nextval('annotation_database_id_seq'::regclass),
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
)
WITH ( OIDS=FALSE );
ALTER TABLE public.annotation_database OWNER TO annso;





CREATE TABLE public.annotation_field
(

    database_id integer,
    name character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    name_ui character varying(255) COLLATE pg_catalog."C.UTF-8",
    description text,
    type field_type,
    unity character varying(20) COLLATE pg_catalog."C.UTF-8" ,
    CONSTRAINT annotation_field_pkey PRIMARY KEY (database_id, name),
    CONSTRAINT annotation_field_database_id_fkey FOREIGN KEY (database_id)
        REFERENCES public."annotation_database" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH ( OIDS=FALSE );
ALTER TABLE public.annotation_field OWNER TO annso;











CREATE TABLE public."parameter"
(
    key character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL ,
    value character varying(255) COLLATE pg_catalog."C.UTF-8" NOT NULL,
    description character varying(255) COLLATE pg_catalog."C.UTF-8",
    CONSTRAINT parameter_pkey PRIMARY KEY (key)
)
WITH ( OIDS=FALSE );
ALTER TABLE public."parameter" OWNER TO annso;





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
    ('stats_refresh_date',        'The date of the last refresh of statistics',    to_char(current_timestamp, 'YYYY-MM-DD'))




