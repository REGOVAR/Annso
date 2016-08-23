 


CREATE SEQUENCE public.refgene_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.refgene_id_seq
  OWNER TO regovar;

ALTER TABLE refGene ADD id integer NOT NULL DEFAULT nextval('refgene_id_seq'::regclass)
ALTER TABLE refGene ADD variant_ids integer[][]


