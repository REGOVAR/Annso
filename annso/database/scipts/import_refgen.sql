--
-- Structure
--
DROP TYPE IF EXISTS refgene_hg19_cdsstat CASCADE;
CREATE TYPE refgene_hg19_cdsstat AS ENUM ('none','unk','incmpl','cmpl');

DROP TABLE IF EXISTS public.refgene_hg19;
CREATE TABLE public.refgene_hg19
(
  bin integer NOT NULL,
  name character varying(255) NOT NULL,
  chrom character varying(255) NOT NULL,
  strand character(1) NOT NULL,
  txstart bigint NOT NULL,
  txend bigint NOT NULL,
  cdsstart bigint NOT NULL,
  cdsend bigint NOT NULL,
  exoncount bigint NOT NULL,
  exonstarts text NOT NULL,
  exonends text NOT NULL,
  score bigint,
  name2 character varying(255) NOT NULL,
  cdsstartstat refgene_hg19_cdsstat NOT NULL,
  cdsendstat refgene_hg19_cdsstat NOT NULL,
  exonframes text NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.refgene_hg19
  OWNER TO annso;








--
-- Command to import data from csv
--
COPY refgene_hg19 FROM '/tmp/hg19_db/refGene.txt' DELIMITER E'\t' CSV;




--
-- Alter table to add annso additional fields
--
DROP INDEX IF EXISTS public.refgene_hg19_id_seq;
CREATE SEQUENCE public.refgene_hg19_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.refgene_hg19_id_seq
  OWNER TO annso;

ALTER TABLE public.refgene_hg19 ADD txrange int8range;
ALTER TABLE public.refgene_hg19 ADD id integer NOT NULL DEFAULT nextval('refgene_hg19_id_seq'::regclass);
ALTER TABLE public.refgene_hg19 ADD variant_ids integer[][];


--
-- Create indexes
--
DROP INDEX IF EXISTS public.refgene_hg19_chrom_txrange_idx;
CREATE INDEX refgene_hg19_chrom_txrange_idx
  ON public.refgene_hg19
  USING btree
  (chrom COLLATE pg_catalog."default", txrange);


DROP INDEX IF EXISTS public.refgene_hg19_txrange_idx;
CREATE INDEX refgene_hg19_txrange_idx
  ON public.refgene_hg19
  USING gist
  (txrange);
  
  
--
-- Compute/Set additional fields 
--
UPDATE public.refgene_hg19 SET txrange=int8range(txstart, txend);


UPDATE public.refgene_hg19 SET variant_ids=ids
FROM (
    SELECT rg.id as rid, array_agg(v.id) as ids
    FROM public.variant_hg19 v
    LEFT JOIN public.refgene_hg19 rg ON rg.txrange @> int8(v.pos)
    GROUP BY rg.id
) as SR
WHERE id=rid
