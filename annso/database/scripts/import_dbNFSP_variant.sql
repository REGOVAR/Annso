

--
-- This script is to import data from dbNSFP 3.3a only
--



--
-- Import csv data
--

DROP TABLE IF EXISTS public.import_dbnfsp_variant;
CREATE TABLE public.import_dbnfsp_variant
(
    chr text,
    pos text,
    ref text,
    alt text,
    aaref text,
    aaalt text,
    rs_dbSNP147 text,
    hg19_chr text,
    hg19_pos text,
    hg18_chr text,
    hg18_pos text,
    genename text,
    cds_strand text,
    refcodon text,
    codonpos text,
    codon_degeneracy text,
    Ancestral_allele text,
    AltaiNeandertal text,
    Denisova text,
    Ensembl_geneid text,
    Ensembl_transcriptid text,
    Ensembl_proteinid text,
    aapos text,
    SIFT_score text,
    SIFT_converted_rankscore text,
    SIFT_pred text,
    Uniprot_acc_Polyphen2 text,
    Uniprot_id_Polyphen2 text,
    Uniprot_aapos_Polyphen2 text,
    Polyphen2_HDIV_score text,
    Polyphen2_HDIV_rankscore text,
    Polyphen2_HDIV_pred text,
    Polyphen2_HVAR_score text,
    Polyphen2_HVAR_rankscore text,
    Polyphen2_HVAR_pred text,
    LRT_score text,
    LRT_converted_rankscore text,
    LRT_pred text,
    LRT_Omega text,
    MutationTaster_score text,
    MutationTaster_converted_rankscore text,
    MutationTaster_pred text,
    MutationTaster_model text,
    MutationTaster_AAE text,
    MutationAssessor_UniprotID text,
    MutationAssessor_variant text,
    MutationAssessor_score text,
    MutationAssessor_rankscore text,
    MutationAssessor_pred text,
    FATHMM_score text,
    FATHMM_converted_rankscore text,
    FATHMM_pred text,
    PROVEAN_score text,
    PROVEAN_converted_rankscore text,
    PROVEAN_pred text,
    Transcript_id_VEST3 text,
    Transcript_var_VEST3 text,
    VEST3_score text,
    VEST3_rankscore text,
    MetaSVM_score text,
    MetaSVM_rankscore text,
    MetaSVM_pred text,
    MetaLR_score text,
    MetaLR_rankscore text,
    MetaLR_pred text,
    Reliability_index text,
    M_CAP_score text,
    M_CAP_rankscore text,
    M_CAP_pred text,
    CADD_raw text,
    CADD_raw_rankscore text,
    CADD_phred text,
    DANN_score text,
    DANN_rankscore text,
    fathmm_MKL_coding_score text,
    fathmm_MKL_coding_rankscore text,
    fathmm_MKL_coding_pred text,
    fathmm_MKL_coding_group text,
    Eigen_coding_or_noncoding text,
    Eigen_raw text,
    Eigen_phred text,
    Eigen_PC_raw text,
    Eigen_PC_phred text,
    Eigen_PC_raw_rankscore text,
    GenoCanyon_score text,
    GenoCanyon_rankscore text,
    integrated_fitCons_score text,
    integrated_fitCons_rankscore text,
    integrated_confidence_value text,
    GM12878_fitCons_score text,
    GM12878_fitCons_rankscore text,
    GM12878_confidence_value text,
    H1_hESC_fitCons_score text,
    H1_hESC_fitCons_rankscore text,
    H1_hESC_confidence_value text,
    HUVEC_fitCons_score text,
    HUVEC_fitCons_rankscore text,
    HUVEC_confidence_value text,
    GERPpp_NR text,
    GERPpp_RS text,
    GERPpp_RS_rankscore text,
    phyloP100way_vertebrate text,
    phyloP100way_vertebrate_rankscore text,
    phyloP20way_mammalian text,
    phyloP20way_mammalian_rankscore text,
    phastCons100way_vertebrate text,
    phastCons100way_vertebrate_rankscore text,
    phastCons20way_mammalian text,
    phastCons20way_mammalian_rankscore text,
    SiPhy_29way_pi text,
    SiPhy_29way_logOdds text,
    SiPhy_29way_logOdds_rankscore text,
    _1000Gp3_AC text,
    _1000Gp3_AF text,
    _1000Gp3_AFR_AC text,
    _1000Gp3_AFR_AF text,
    _1000Gp3_EUR_AC text,
    _1000Gp3_EUR_AF text,
    _1000Gp3_AMR_AC text,
    _1000Gp3_AMR_AF text,
    _1000Gp3_EAS_AC text,
    _1000Gp3_EAS_AF text,
    _1000Gp3_SAS_AC text,
    _1000Gp3_SAS_AF text,
    TWINSUK_AC text,
    TWINSUK_AF text,
    ALSPAC_AC text,
    ALSPAC_AF text,
    ESP6500_AA_AC text,
    ESP6500_AA_AF text,
    ESP6500_EA_AC text,
    ESP6500_EA_AF text,
    ExAC_AC text,
    ExAC_AF text,
    ExAC_Adj_AC text,
    ExAC_Adj_AF text,
    ExAC_AFR_AC text,
    ExAC_AFR_AF text,
    ExAC_AMR_AC text,
    ExAC_AMR_AF text,
    ExAC_EAS_AC text,
    ExAC_EAS_AF text,
    ExAC_FIN_AC text,
    ExAC_FIN_AF text,
    ExAC_NFE_AC text,
    ExAC_NFE_AF text,
    ExAC_SAS_AC text,
    ExAC_SAS_AF text,
    ExAC_nonTCGA_AC text,
    ExAC_nonTCGA_AF text,
    ExAC_nonTCGA_Adj_AC text,
    ExAC_nonTCGA_Adj_AF text,
    ExAC_nonTCGA_AFR_AC text,
    ExAC_nonTCGA_AFR_AF text,
    ExAC_nonTCGA_AMR_AC text,
    ExAC_nonTCGA_AMR_AF text,
    ExAC_nonTCGA_EAS_AC text,
    ExAC_nonTCGA_EAS_AF text,
    ExAC_nonTCGA_FIN_AC text,
    ExAC_nonTCGA_FIN_AF text,
    ExAC_nonTCGA_NFE_AC text,
    ExAC_nonTCGA_NFE_AF text,
    ExAC_nonTCGA_SAS_AC text,
    ExAC_nonTCGA_SAS_AF text,
    ExAC_nonpsych_AC text,
    ExAC_nonpsych_AF text,
    ExAC_nonpsych_Adj_AC text,
    ExAC_nonpsych_Adj_AF text,
    ExAC_nonpsych_AFR_AC text,
    ExAC_nonpsych_AFR_AF text,
    ExAC_nonpsych_AMR_AC text,
    ExAC_nonpsych_AMR_AF text,
    ExAC_nonpsych_EAS_AC text,
    ExAC_nonpsych_EAS_AF text,
    ExAC_nonpsych_FIN_AC text,
    ExAC_nonpsych_FIN_AF text,
    ExAC_nonpsych_NFE_AC text,
    ExAC_nonpsych_NFE_AF text,
    ExAC_nonpsych_SAS_AC text,
    ExAC_nonpsych_SAS_AF text,
    clinvar_rs text,
    clinvar_clnsig text,
    clinvar_trait text,
    clinvar_golden_stars text,
    Interpro_domain text,
    GTEx_V6_gene text,
    GTEx_V6_tissue text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.import_dbnfsp_variant
  OWNER TO annso;



COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr1' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr2' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr3' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr4' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr5' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr6' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr7' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr8' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr9' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr10' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr11' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr12' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr13' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr14' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr15' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr16' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr17' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr18' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr19' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr20' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr21' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chr22' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chrX' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chrY' DELIMITER E'\t' CSV HEADER;
COPY import_dbnfsp_variant FROM '/var/regovar/data/db/dbNSFP3.3a_variant.chrM' DELIMITER E'\t' CSV HEADER;




--
-- Create Annso tables for dbNFSP data
--

DROP TABLE IF EXISTS public.dbnfsp_variant;
CREATE TABLE public.dbnfsp_variant
(
    bin_hg38 integer,
    chr_hg38 integer,
    pos_hg38 bigint,
    bin_hg19 integer,
    chr_hg19 integer,
    pos_hg19 bigint,
    bin_hg18 integer,
    chr_hg18 integer,
    pos_hg18 bigint,
    ref text,
    alt text,
    aaref text,
    aaalt text,
    rs_dbSNP147 text,
    genename text,
    cds_strand text, -- char(1) but multiple value
    refcodon text,
    codonpos text, -- integer but multiple value !!,
    codon_degeneracy text, -- integer but multiple value !!
    Ancestral_allele character varying(1),
    AltaiNeandertal text,
    Denisova text,

    Ensembl_geneid text,
    Ensembl_transcriptid text,
    Ensembl_proteinid text,
    aapos text,
    SIFT_score text,
    SIFT_converted_rankscore real,
    SIFT_pred text,
    FATHMM_score text,
    FATHMM_converted_rankscore real,
    FATHMM_pred text,
    PROVEAN_score text,
    PROVEAN_converted_rankscore real,
    PROVEAN_pred text,

    Uniprot_acc_Polyphen2 text,
    Uniprot_id_Polyphen2 text,
    Uniprot_aapos_Polyphen2 text,
    Polyphen2_HDIV_score text,
    Polyphen2_HDIV_rankscore text,
    Polyphen2_HDIV_pred text,
    Polyphen2_HVAR_score text,
    Polyphen2_HVAR_rankscore text,
    Polyphen2_HVAR_pred text,

    LRT_score real,
    LRT_converted_rankscore real,
    LRT_pred character varying(1),
    LRT_Omega real,

    MutationTaster_score text,
    MutationTaster_converted_rankscore real,
    MutationTaster_pred text,
    MutationTaster_model text,
    MutationTaster_AAE text,
    MutationAssessor_UniprotID text,
    MutationAssessor_variant text,
    MutationAssessor_score real,
    MutationAssessor_rankscore real,
    MutationAssessor_pred character varying(1),

    Transcript_id_VEST3 text,
    Transcript_var_VEST3 text,
    VEST3_score text,
    VEST3_rankscore real,

    MetaSVM_score real,
    MetaSVM_rankscore real,
    MetaSVM_pred character varying(1),
    MetaLR_score real,
    MetaLR_rankscore real,
    MetaLR_pred character varying(1),

    Reliability_index integer,

    M_CAP_score real,
    M_CAP_rankscore real,
    M_CAP_pred character varying(1),

    CADD_raw real,
    CADD_raw_rankscore real,
    CADD_phred real,

    DANN_score real,
    DANN_rankscore real,

    fathmm_MKL_coding_score real,
    fathmm_MKL_coding_rankscore real,
    fathmm_MKL_coding_pred text,
    fathmm_MKL_coding_group text,

    Eigen_coding_or_noncoding boolean,
    Eigen_raw real,
    Eigen_phred real,
    Eigen_PC_raw real,
    Eigen_PC_phred real,
    Eigen_PC_raw_rankscore real,

    GenoCanyon_score real,
    GenoCanyon_rankscore real,

    integrated_fitCons_score real,
    integrated_fitCons_rankscore real,
    integrated_confidence_value integer,

    GM12878_fitCons_score real,
    GM12878_fitCons_rankscore real,
    GM12878_confidence_value integer,

    H1_hESC_fitCons_score real,
    H1_hESC_fitCons_rankscore real,
    H1_hESC_confidence_value integer,

    HUVEC_fitCons_score real,
    HUVEC_fitCons_rankscore real,
    HUVEC_confidence_value integer,

    GERPpp_NR real,
    GERPpp_RS real,
    GERPpp_RS_rankscore real,

    phyloP100way_vertebrate real,
    phyloP100way_vertebrate_rankscore real,
    phyloP20way_mammalian real,
    phyloP20way_mammalian_rankscore real,

    phastCons100way_vertebrate real,
    phastCons100way_vertebrate_rankscore real,
    phastCons20way_mammalian real,
    phastCons20way_mammalian_rankscore real,

    SiPhy_29way_pi text,
    SiPhy_29way_logOdds text,
    SiPhy_29way_logOdds_rankscore text,

    _1000Gp3_AC integer,
    _1000Gp3_AF real,
    _1000Gp3_AFR_AC integer,
    _1000Gp3_AFR_AF real,
    _1000Gp3_EUR_AC integer,
    _1000Gp3_EUR_AF real,
    _1000Gp3_AMR_AC integer,
    _1000Gp3_AMR_AF real,
    _1000Gp3_EAS_AC integer,
    _1000Gp3_EAS_AF real,
    _1000Gp3_SAS_AC integer,
    _1000Gp3_SAS_AF real,
    TWINSUK_AC integer,
    TWINSUK_AF real,
    ALSPAC_AC integer,
    ALSPAC_AF real,
    ESP6500_AA_AC integer,
    ESP6500_AA_AF real,
    ESP6500_EA_AC integer,
    ESP6500_EA_AF real,
    ExAC_AC integer,
    ExAC_AF real,
    ExAC_Adj_AC integer,
    ExAC_Adj_AF real,
    ExAC_AFR_AC integer,
    ExAC_AFR_AF real,
    ExAC_AMR_AC integer,
    ExAC_AMR_AF real,
    ExAC_EAS_AC integer,
    ExAC_EAS_AF real,
    ExAC_FIN_AC integer,
    ExAC_FIN_AF real,
    ExAC_NFE_AC integer,
    ExAC_NFE_AF real,
    ExAC_SAS_AC integer,
    ExAC_SAS_AF real,
    ExAC_nonTCGA_AC integer,
    ExAC_nonTCGA_AF real,
    ExAC_nonTCGA_Adj_AC integer,
    ExAC_nonTCGA_Adj_AF real,
    ExAC_nonTCGA_AFR_AC integer,
    ExAC_nonTCGA_AFR_AF real,
    ExAC_nonTCGA_AMR_AC integer,
    ExAC_nonTCGA_AMR_AF real,
    ExAC_nonTCGA_EAS_AC integer,
    ExAC_nonTCGA_EAS_AF real,
    ExAC_nonTCGA_FIN_AC integer,
    ExAC_nonTCGA_FIN_AF real,
    ExAC_nonTCGA_NFE_AC integer,
    ExAC_nonTCGA_NFE_AF real,
    ExAC_nonTCGA_SAS_AC integer,
    ExAC_nonTCGA_SAS_AF real,
    ExAC_nonpsych_AC integer,
    ExAC_nonpsych_AF real,
    ExAC_nonpsych_Adj_AC integer,
    ExAC_nonpsych_Adj_AF real,
    ExAC_nonpsych_AFR_AC integer,
    ExAC_nonpsych_AFR_AF real,
    ExAC_nonpsych_AMR_AC integer,
    ExAC_nonpsych_AMR_AF real,
    ExAC_nonpsych_EAS_AC integer,
    ExAC_nonpsych_EAS_AF real,
    ExAC_nonpsych_FIN_AC integer,
    ExAC_nonpsych_FIN_AF real,
    ExAC_nonpsych_NFE_AC integer,
    ExAC_nonpsych_NFE_AF real,
    ExAC_nonpsych_SAS_AC integer,
    ExAC_nonpsych_SAS_AF real,
    clinvar_rs text,
    clinvar_clnsig text,
    clinvar_trait text,
    clinvar_golden_stars text,
    Interpro_domain text,
    GTEx_V6_gene text,
    GTEx_V6_tissue text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dbnfsp_variant
  OWNER TO annso;







--
-- Create indexes
--

DROP INDEX IF EXISTS public.dbnfsp_variant_hg19_idx;
CREATE INDEX dbnfsp_variant_hg19_idx
  ON public.dbnfsp_variant
  USING btree
  (bin_hg19, chr_hg19, pos_hg19);


DROP INDEX IF EXISTS public.dbnfsp_variant_hg18_idx;
CREATE INDEX dbnfsp_variant_hg18_idx
  ON public.dbnfsp_variant
  USING btree
  (bin_hg18, chr_hg18, pos_hg18);

DROP INDEX IF EXISTS public.dbnfsp_variant_hg38_idx;
CREATE INDEX dbnfsp_variant_hg38_idx
  ON public.dbnfsp_variant
  USING btree
  (bin_hg38, chr_hg38, pos_hg38);






--
-- Migrate imported data to annso database
--
INSERT INTO public.dbnfsp_variant(
    chr_hg38, pos_hg38, chr_hg19, pos_hg19, chr_hg18, pos_hg18,
    ref, alt, aaref, aaalt, 
    rs_dbSNP147, genename, cds_strand,
    refcodon, codonpos, codon_degeneracy,
    Ancestral_allele, AltaiNeandertal, Denisova,
  
    Ensembl_geneid, Ensembl_transcriptid, Ensembl_proteinid, aapos,
    SIFT_score, SIFT_converted_rankscore, SIFT_pred,
    FATHMM_score, FATHMM_converted_rankscore, FATHMM_pred,
    PROVEAN_score, PROVEAN_converted_rankscore, PROVEAN_pred,
  
    Uniprot_acc_Polyphen2, Uniprot_id_Polyphen2, Uniprot_aapos_Polyphen2,
    Polyphen2_HDIV_score, Polyphen2_HDIV_rankscore, Polyphen2_HDIV_pred, Polyphen2_HVAR_score, Polyphen2_HVAR_rankscore, Polyphen2_HVAR_pred,
    LRT_score, LRT_converted_rankscore, LRT_pred, LRT_Omega,
    MutationTaster_score, MutationTaster_converted_rankscore, MutationTaster_pred, MutationTaster_model, MutationTaster_AAE, MutationAssessor_UniprotID, MutationAssessor_variant, 
    MutationAssessor_score, MutationAssessor_rankscore, MutationAssessor_pred,
  
    Transcript_id_VEST3, Transcript_var_VEST3, VEST3_score, VEST3_rankscore,
    MetaSVM_score, MetaSVM_rankscore, MetaSVM_pred, MetaLR_score, MetaLR_rankscore, MetaLR_pred,
    Reliability_index,
    M_CAP_score, M_CAP_rankscore, M_CAP_pred,
    CADD_raw, CADD_raw_rankscore, CADD_phred,
    DANN_score, DANN_rankscore,
    fathmm_MKL_coding_score, fathmm_MKL_coding_rankscore, fathmm_MKL_coding_pred, fathmm_MKL_coding_group,
    Eigen_coding_or_noncoding, Eigen_raw, Eigen_phred, Eigen_PC_raw, Eigen_PC_phred, Eigen_PC_raw_rankscore,
    GenoCanyon_score, GenoCanyon_rankscore,
    integrated_fitCons_score, integrated_fitCons_rankscore, integrated_confidence_value,
    GM12878_fitCons_score, GM12878_fitCons_rankscore, GM12878_confidence_value,
    H1_hESC_fitCons_score, H1_hESC_fitCons_rankscore, H1_hESC_confidence_value,
    HUVEC_fitCons_score, HUVEC_fitCons_rankscore, HUVEC_confidence_value,
    GERPpp_NR, GERPpp_RS, GERPpp_RS_rankscore,
    phyloP100way_vertebrate, phyloP100way_vertebrate_rankscore, phyloP20way_mammalian, phyloP20way_mammalian_rankscore,
    phastCons100way_vertebrate, phastCons100way_vertebrate_rankscore, phastCons20way_mammalian, phastCons20way_mammalian_rankscore,
    SiPhy_29way_pi, SiPhy_29way_logOdds, SiPhy_29way_logOdds_rankscore ,
  
    _1000Gp3_AC, _1000Gp3_AF, _1000Gp3_AFR_AC, _1000Gp3_AFR_AF, _1000Gp3_EUR_AC, _1000Gp3_EUR_AF, _1000Gp3_AMR_AC, _1000Gp3_AMR_AF, _1000Gp3_EAS_AC, _1000Gp3_EAS_AF, _1000Gp3_SAS_AC, _1000Gp3_SAS_AF,
  
    TWINSUK_AC, TWINSUK_AF,
    ALSPAC_AC, ALSPAC_AF,
    ESP6500_AA_AC, ESP6500_AA_AF, ESP6500_EA_AC, ESP6500_EA_AF,
  
    ExAC_AC, ExAC_AF, ExAC_Adj_AC, ExAC_Adj_AF, ExAC_AFR_AC, ExAC_AFR_AF, ExAC_AMR_AC, ExAC_AMR_AF, ExAC_EAS_AC, ExAC_EAS_AF, ExAC_FIN_AC, ExAC_FIN_AF, ExAC_NFE_AC,
    ExAC_NFE_AF, ExAC_SAS_AC, ExAC_SAS_AF, ExAC_nonTCGA_AC, ExAC_nonTCGA_AF, ExAC_nonTCGA_Adj_AC, ExAC_nonTCGA_Adj_AF, ExAC_nonTCGA_AFR_AC, ExAC_nonTCGA_AFR_AF, 
    ExAC_nonTCGA_AMR_AC, ExAC_nonTCGA_AMR_AF, ExAC_nonTCGA_EAS_AC, ExAC_nonTCGA_EAS_AF, ExAC_nonTCGA_FIN_AC, ExAC_nonTCGA_FIN_AF, ExAC_nonTCGA_NFE_AC, ExAC_nonTCGA_NFE_AF,
    ExAC_nonTCGA_SAS_AC, ExAC_nonTCGA_SAS_AF, ExAC_nonpsych_AC, ExAC_nonpsych_AF, ExAC_nonpsych_Adj_AC, ExAC_nonpsych_Adj_AF, ExAC_nonpsych_AFR_AC, ExAC_nonpsych_AFR_AF, 
    ExAC_nonpsych_AMR_AC, ExAC_nonpsych_AMR_AF, ExAC_nonpsych_EAS_AC, ExAC_nonpsych_EAS_AF, ExAC_nonpsych_FIN_AC, ExAC_nonpsych_FIN_AF, ExAC_nonpsych_NFE_AC, 
    ExAC_nonpsych_NFE_AF, ExAC_nonpsych_SAS_AC, ExAC_nonpsych_SAS_AF,
  
    clinvar_rs, clinvar_clnsig, clinvar_trait, clinvar_golden_stars, Interpro_domain,
    GTEx_V6_gene, GTEx_V6_tissue)
  
SELECT 
    CASE WHEN chr='X' THEN 23 WHEN chr='Y' THEN 24 WHEN chr='M' THEN 25 WHEN chr='.' THEN NULL WHEN chr IS NOT NULL THEN CAST(chr AS INTEGER) END, 
    CAST(pos AS INTEGER) -1, 
    CASE WHEN hg19_chr='X' THEN 23 WHEN hg19_chr='Y' THEN 24 WHEN hg19_chr='M' THEN 25 WHEN hg19_chr='.' THEN NULL WHEN hg19_chr IS NOT NULL THEN CAST(hg19_chr AS INTEGER) END,
    NULLIF(CAST(NULLIF(hg19_pos, '.') AS INTEGER)-1, -1),
    CASE WHEN hg18_chr='X' THEN 23 WHEN hg18_chr='Y' THEN 24 WHEN hg18_chr='M' THEN 25 WHEN hg18_chr='.' THEN NULL WHEN hg18_chr IS NOT NULL THEN CAST(hg18_chr AS INTEGER) END,
    NULLIF(CAST(NULLIF(hg18_pos, '.') AS INTEGER)-1, -1),
    ref, alt, aaref, aaalt, 
    rs_dbSNP147, genename, cds_strand,
    refcodon, 
    NULLIF(codonpos, '.'), 
    NULLIF(codon_degeneracy, '.'),
    
    NULLIF(Ancestral_allele, '.'),
    NULLIF(AltaiNeandertal, '.'),
    NULLIF(Denisova, '.'),

    Ensembl_geneid, Ensembl_transcriptid, Ensembl_proteinid, aapos,
    NULLIF(SIFT_score, '.'),
    CAST(NULLIF(SIFT_converted_rankscore, '.') AS REAL),
    NULLIF(SIFT_pred, '.'),

    NULLIF(FATHMM_score, '.'),
    CAST(NULLIF(FATHMM_converted_rankscore, '.') AS REAL),
    NULLIF(FATHMM_pred, '.'),
    NULLIF(PROVEAN_score, '.'),
    CAST(NULLIF(PROVEAN_converted_rankscore, '.') AS REAL),
    NULLIF(PROVEAN_pred, '.'),

    NULLIF(Uniprot_acc_Polyphen2, '.'),
    NULLIF(Uniprot_id_Polyphen2, '.'),
    NULLIF(Uniprot_aapos_Polyphen2, '.'),

    NULLIF(Polyphen2_HDIV_score, '.'),
    CAST(NULLIF(Polyphen2_HDIV_rankscore, '.') AS REAL),
    NULLIF(Polyphen2_HDIV_pred, '.'),
    NULLIF(Polyphen2_HVAR_score, '.'),
    CAST(NULLIF(Polyphen2_HVAR_rankscore, '.') AS REAL),
    NULLIF(Polyphen2_HVAR_pred, '.'),

    CAST(NULLIF(LRT_score, '.') AS REAL),
    CAST(NULLIF(LRT_converted_rankscore, '.') AS REAL),
    NULLIF(LRT_pred, '.'),
    CAST(NULLIF(LRT_Omega, '.') AS REAL),

    NULLIF(MutationTaster_score, '.'),
    CAST(NULLIF(MutationTaster_converted_rankscore, '.') AS REAL),
    NULLIF(MutationTaster_pred, '.'),
    NULLIF(MutationTaster_model, '.'),
    NULLIF(MutationTaster_AAE, '.'),
    NULLIF(MutationAssessor_UniprotID, '.'),
    NULLIF(MutationAssessor_variant, '.'),
    CAST(NULLIF(MutationAssessor_score, '.') AS REAL),
    CAST(NULLIF(MutationAssessor_rankscore, '.') AS REAL),
    NULLIF(MutationAssessor_pred, '.'),

    NULLIF(Transcript_id_VEST3, '.'),
    NULLIF(Transcript_var_VEST3, '.'),
    NULLIF(VEST3_score, '.'),
    CAST(NULLIF(VEST3_rankscore, '.') AS REAL),

    CAST(NULLIF(MetaSVM_score, '.') AS REAL),
    CAST(NULLIF(MetaSVM_rankscore, '.') AS REAL),
    NULLIF(MetaSVM_pred, '.'),
    CAST(NULLIF(MetaLR_score, '.') AS REAL),
    CAST(NULLIF(MetaLR_rankscore, '.') AS REAL),
    NULLIF(MetaLR_pred, '.'),

    CAST(NULLIF(Reliability_index, '.') AS REAL),

    CAST(NULLIF(M_CAP_score, '.') AS REAL),
    CAST(NULLIF(M_CAP_rankscore, '.') AS REAL),
    NULLIF(M_CAP_pred, '.'),

    CAST(NULLIF(CADD_raw, '.') AS REAL),
    CAST(NULLIF(CADD_raw_rankscore, '.') AS REAL),
    CAST(NULLIF(CADD_phred, '.') AS REAL),

    CAST(NULLIF(DANN_score, '.') AS REAL),
    CAST(NULLIF(DANN_rankscore, '.') AS REAL),

    CAST(NULLIF(fathmm_MKL_coding_score, '.') AS REAL),
    CAST(NULLIF(fathmm_MKL_coding_rankscore, '.') AS REAL),
    NULLIF(fathmm_MKL_coding_pred, '.'),
    NULLIF(fathmm_MKL_coding_group, '.'),

    CASE WHEN Eigen_coding_or_noncoding='.' THEN NULL WHEN Eigen_coding_or_noncoding='c' THEN TRUE ELSE FALSE END,
    CAST(NULLIF(Eigen_raw, '.') AS REAL),
    CAST(NULLIF(Eigen_phred, '.') AS REAL),
    CAST(NULLIF(Eigen_PC_raw, '.') AS REAL),
    CAST(NULLIF(Eigen_PC_phred, '.') AS REAL),
    CAST(NULLIF(Eigen_PC_raw_rankscore, '.') AS REAL),

    CAST(NULLIF(GenoCanyon_score, '.') AS REAL),
    CAST(NULLIF(GenoCanyon_rankscore, '.') AS REAL),

    CAST(NULLIF(integrated_fitCons_score, '.') AS REAL),
    CAST(NULLIF(integrated_fitCons_rankscore, '.') AS REAL),
    CAST(NULLIF(integrated_confidence_value, '.') AS INTEGER),

    CAST(NULLIF(GM12878_fitCons_score, '.') AS REAL),
    CAST(NULLIF(GM12878_fitCons_rankscore, '.') AS REAL),
    CAST(NULLIF(GM12878_confidence_value, '.') AS INTEGER),

    CAST(NULLIF(H1_hESC_fitCons_score, '.') AS REAL),
    CAST(NULLIF(H1_hESC_fitCons_rankscore, '.') AS REAL),
    CAST(NULLIF(H1_hESC_confidence_value, '.') AS INTEGER),
    CAST(NULLIF(HUVEC_fitCons_score, '.') AS REAL),
    CAST(NULLIF(HUVEC_fitCons_rankscore, '.') AS REAL),
    CAST(NULLIF(HUVEC_confidence_value, '.') AS INTEGER),

    CAST(NULLIF(GERPpp_NR, '.') AS REAL),
    CAST(NULLIF(GERPpp_RS, '.') AS REAL),
    CAST(NULLIF(GERPpp_RS_rankscore, '.') AS REAL),

    CAST(NULLIF(phyloP100way_vertebrate, '.') AS REAL),
    CAST(NULLIF(phyloP100way_vertebrate_rankscore, '.') AS REAL),
    CAST(NULLIF(phyloP20way_mammalian, '.') AS REAL),
    CAST(NULLIF(phyloP20way_mammalian_rankscore, '.') AS REAL),

    CAST(NULLIF(phastCons100way_vertebrate, '.') AS REAL),
    CAST(NULLIF(phastCons100way_vertebrate_rankscore, '.') AS REAL),
    CAST(NULLIF(phastCons20way_mammalian, '.') AS REAL),
    CAST(NULLIF(phastCons20way_mammalian_rankscore, '.') AS REAL),

    NULLIF(SiPhy_29way_pi, '.'),
    NULLIF(SiPhy_29way_logOdds, '.'),
    CAST(NULLIF(SiPhy_29way_logOdds_rankscore, '.') AS REAL),

    CAST(NULLIF(_1000Gp3_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_AF, '.') AS REAL),
    CAST(NULLIF(_1000Gp3_AFR_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_AFR_AF, '.') AS REAL),
    CAST(NULLIF(_1000Gp3_EUR_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_EUR_AF, '.') AS REAL),
    CAST(NULLIF(_1000Gp3_AMR_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_AMR_AF, '.') AS REAL),
    CAST(NULLIF(_1000Gp3_EAS_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_EAS_AF, '.') AS REAL),
    CAST(NULLIF(_1000Gp3_SAS_AC, '.') AS INTEGER),
    CAST(NULLIF(_1000Gp3_SAS_AF, '.') AS REAL),

    CAST(NULLIF(TWINSUK_AC, '.') AS INTEGER),
    CAST(NULLIF(TWINSUK_AF, '.') AS REAL),
    CAST(NULLIF(ALSPAC_AC, '.') AS INTEGER),
    CAST(NULLIF(ALSPAC_AF, '.') AS REAL),
    CAST(NULLIF(ESP6500_AA_AC, '.') AS INTEGER),
    CAST(NULLIF(ESP6500_AA_AF, '.') AS REAL),
    CAST(NULLIF(ESP6500_EA_AC, '.') AS INTEGER),
    CAST(NULLIF(ESP6500_EA_AF, '.') AS REAL),

    CAST(NULLIF(ExAC_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_Adj_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_Adj_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_AFR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_AFR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_AMR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_AMR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_EAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_EAS_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_FIN_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_FIN_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_NFE_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_NFE_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_SAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_SAS_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_Adj_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_Adj_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_AFR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_AFR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_AMR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_AMR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_EAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_EAS_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_FIN_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_FIN_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_NFE_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_NFE_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonTCGA_SAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonTCGA_SAS_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_Adj_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_Adj_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_AFR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_AFR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_AMR_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_AMR_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_EAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_EAS_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_FIN_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_FIN_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_NFE_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_NFE_AF, '.') AS REAL),
    CAST(NULLIF(ExAC_nonpsych_SAS_AC, '.') AS INTEGER),
    CAST(NULLIF(ExAC_nonpsych_SAS_AF, '.') AS REAL),

    NULLIF(clinvar_rs, '.'),
    NULLIF(clinvar_clnsig, '.'),
    NULLIF(clinvar_trait, '.'),
    NULLIF(clinvar_golden_stars, '.'),
    NULLIF(Interpro_domain, '.'),

    NULLIF(GTEx_V6_gene, '.'),
    NULLIF(GTEx_V6_tissue, '.')

FROM import_dbnfsp_variant;




-- Import CSV
-- Tue Jan 24 19:37:01 CET 2017
-- Tue Jan 24 22:17:12 CET 2017
-- Convert CSV to 
-- Wed Jan 25 09:53:11 CET 2017
-- Wed Jan 25 13:38:52 CET 2017














--
-- Register refGen into annso database
-- 

INSERT INTO public.annotation_database(id, version, name, name_ui, description, url, reference_id, update_date, jointure) VALUES
  (4,
  '3.3a',
  'dbnfsp_variant', 
  'dbNSFP', 
  'Integrated database of functional annotations from multiple sources for the comprehensive collection of human non-synonymous SNPs (nsSNVs).', 
  'https://sites.google.com/site/jpopgen/dbNSFP', 
  1, 
  CURRENT_TIMESTAMP, 
  'dbnfsp_variant ON {0}.bin=dbnfsp_variant.bin_hg19 AND {0}.chr=dbnfsp_variant.chr_hg19 AND {0}.pos=dbnfsp_variant.pos_hg19 AND {0}.ref=dbnfsp_variant.ref AND {0}.alt=dbnfsp_variant.alt');








INSERT INTO public.annotation_field(database_id, database_version, id, name, name_ui, type, description, meta) VALUES
  (4, '3.3a',  1, 'chr_hg38',          'chr (hg38)',       'enum',      'Chromosome as to hg38.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (4, '3.3a',  2, 'pos_hg38',          'pos (hg38)',       'int',       'Physical position on the chromosome as to hg38 (1-based coordinate). For mitochondrial SNV, this position refers to the rCRS (GenBank: NC_012920).', NULL),
  (4, '3.3a',  3, 'chr_hg19',          'chr (hg19)',       'enum',      'Chromosome as to hg19.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (4, '3.3a',  4, 'pos_hg19',          'pos (hg19)',       'int',       'Physical position on the chromosome as to hg19 (1-based coordinate).For mitochondrial SNV, this position refers to a YRI sequence (GenBank: AF347015).', NULL),
  (4, '3.3a',  5, 'chr_hg18',          'chr (hg18)',       'enum',      'Chromosome as to hg38.', '{"enum": {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "11": "11", "12": "12", "13": "13", "14": "14", "15": "15", "16": "16", "17": "17", "18": "18", "19": "19", "20": "20", "21": "21", "22": "22", "23": "X", "24": "Y", "25": "M"}}'),
  (4, '3.3a',  6, 'pos_hg18',          'pos (hg18)',       'int',       'Physical position on the chromosome as to hg18 (1-based coordinate). For mitochondrial SNV, this position refers to a YRI sequence (GenBank: AF347015).', NULL),
  -- (4, '3.3a', 7, 'ref',               'ref',              'string',    'Reference nucleotide allele (as on the + strand).', NULL),
  -- (4, '3.3a', 8, 'alt',               'alt',              'string',    'Alternative nucleotide allele (as on the + strand).', NULL),
  (4, '3.3a',  9, 'aaref',             'aaref',            'string',    'Reference amino acid. "." if the variant is a splicing site SNP (2bp on each end of an intron).', NULL),
  (4, '3.3a', 10, 'aaalt',             'aaalt',            'string',    'Alternative amino acid. "." if the variant is a splicing site SNP (2bp on each end of an intron).', NULL),
  (4, '3.3a', 11, 'rs_dbSNP147',       'rs_dbSNP147',      'string',    'Rs number from dbSNP 147.', NULL),
  (4, '3.3a', 12, 'genename',          'genename',         'string',    'Gene name; if the nsSNV can be assigned to multiple genes, gene names are separated by ";".', NULL),
  (4, '3.3a', 13, 'cds_strand',        'cds_strand',       'string',    'Coding sequence (CDS) strand (+ or -).', NULL),
  (4, '3.3a', 14, 'refcodon',          'refcodon',         'string',    'List of reference codon.', NULL),
  (4, '3.3a', 15, 'codonpos',          'codonpos',         'int',       'Position on the codon (1, 2 or 3).', NULL),
  (4, '3.3a', 16, 'codon_degeneracy',  'codon_degeneracy', 'int',       'Degenerate type (0, 2 or 3).', NULL),
  (4, '3.3a', 17, 'Ancestral_allele:', 'Ancestral_allele', 'string',    'Ancestral allele based on 8 primates EPO. Ancestral alleles by Ensembl 84. The following comes from its original README file: "ACTG" for high-confidence call, ancestral state supported by the other two sequences; "actg" for low-confidence call, ancestral state supported by one sequence only; "N" for failure, the ancestral state is not supported by any other sequence; "-" for the extant species contains an insertion at this position; "."for no coverage in the alignment.', NULL),
  (4, '3.3a', 18, 'AltaiNeandertal',   'AltaiNeandertal',  'int',       'Genotype of a deep sequenced Altai Neanderthal.', NULL),
  (4, '3.3a', 19, 'Denisova',          'Denisova',         'int',       'Genotype of a deep sequenced Denisova.', NULL),

  (4, '3.3a', 20, 'Ensembl_geneid',         'Ensembl_geneid',          'string',     'Ensembl gene id.', NULL),
  (4, '3.3a', 21, 'Ensembl_transcriptid',   'Ensembl_transcriptid',    'string',     'Ensembl transcript ids (Multiple entries separated by ";").', NULL),
  (4, '3.3a', 22, 'Ensembl_proteinid',      'Ensembl_proteinid',       'string',     'Ensembl protein ids. Multiple entries separated by ";",  corresponding to Ensembl_transcriptids.', NULL),  
  (4, '3.3a', 23, 'aapos',                  'aapos',                   'string',     'Amino acid position as to the protein. "-1" if the variant is a splicing site SNP (2bp on each end of an intron). Multiple entries separated by ";", corresponding to Ensembl_proteinid.', NULL),


  (4, '3.3a', 24, 'SIFT_score',                  'SIFT_score',                  'float',  'SIFT score (SIFTori). Scores range from 0 to 1. The smaller the score the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Ensembl_proteinid.', NULL),
  (4, '3.3a', 25, 'SIFT_converted_rankscore',    'SIFT_converted_rankscore',    'float',  'SIFTori scores were first converted to SIFTnew=1-SIFTori, then ranked among all SIFTnew scores in dbNSFP. The rankscore is the ratio of the rank the SIFTnew score over the total number of SIFTnew scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The rankscores range from 0.00963 to 0.91219.', NULL),
  (4, '3.3a', 26, 'SIFT_pred',                   'SIFT_pred',                   'string', 'If SIFTori is smaller than 0.05 (rankscore>0.395) the corresponding nsSNV is predicted as "D(amaging)"; otherwise it is predicted as "T(olerated)". Multiple predictions separated by ";".', NULL),
  (4, '3.3a', 27, 'FATHMM_score',                'FATHMM_score',                'string', 'FATHMM default score (weighted for human inherited-disease mutations with Disease Ontology) (FATHMMori). Scores range from -16.13 to 10.64. The smaller the score  the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Ensembl_proteinid.', NULL),
  (4, '3.3a', 28, 'FATHMM_converted_rankscore',  'FATHMM_converted_rankscore',  'float',  'FATHMMori scores were first converted to FATHMMnew=1-(FATHMMori+16.13)/26.77, then ranked among all FATHMMnew scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of FATHMMnew scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0 to 1.', NULL),
  (4, '3.3a', 29, 'FATHMM_pred',                 'FATHMM_pred',                 'string', 'If a FATHMMori score is <=-1.5 (or rankscore >=0.81332) the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "T(OLERATED)". Multiple predictions separated by ";", corresponding to Ensembl_proteinid.', NULL),
  (4, '3.3a', 30, 'PROVEAN_score',               'PROVEAN_score',               'string', 'PROVEAN score (PROVEANori). Scores range from -14 to 14. The smaller the score the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Ensembl_proteinid.', NULL),
  (4, '3.3a', 31, 'PROVEAN_converted_rankscore', 'PROVEAN_converted_rankscore', 'float',  'PROVEANori were first converted to PROVEANnew=1-(PROVEANori+14)/28, then ranked among all PROVEANnew scores in dbNSFP. The rankscore is the ratio of the rank the PROVEANnew score over the total number of PROVEANnew scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0 to 1.', NULL),
  (4, '3.3a', 32, 'PROVEAN_pred',                'PROVEAN_pred',                'string', 'If PROVEANori <= -2.5 (rankscore>=0.543) the corresponding nsSNV is predicted as "D(amaging)"; otherwise it is predicted as "N(eutral)". Multiple predictions separated by ";", corresponding to Ensembl_proteinid.', NULL),



  (4, '3.3a', 33, 'Uniprot_acc_Polyphen2',   'Uniprot_acc_Polyphen2',    'string', 'Uniprot accession number provided by Polyphen2. Multiple entries separated by ";".', NULL),
  (4, '3.3a', 34, 'Uniprot_id_Polyphen2',    'Uniprot_id_Polyphen2',     'string', 'Uniprot ID numbers corresponding to Uniprot_acc_Polyphen2. Multiple entries separated by ";".', NULL),
  (4, '3.3a', 35, 'Uniprot_aapos_Polyphen2', 'Uniprot_aapos_Polyphen2',  'int',    'Amino acid position as to Uniprot_acc_Polyphen2. Multiple entries separated by ";".', NULL),

  (4, '3.3a', 36, 'Polyphen2_HDIV_score',    'Polyphen2_HDIV_score',     'string',    'Polyphen2 score based on HumDiv, i.e. hdiv_prob. The score ranges from 0 to 1. Multiple entries separated by ";", corresponding to Uniprot_acc_Polyphen2.', NULL),
  (4, '3.3a', 37, 'Polyphen2_HDIV_rankscore','Polyphen2_HDIV_rankscore', 'float',     'Polyphen2_HDIV_rankscore: Polyphen2 HDIV scores were first ranked among all HDIV scores in dbNSFP. The rankscore is the ratio of the rank the score over the total number of the scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0.02634 to 0.89865.', NULL),
  (4, '3.3a', 38, 'Polyphen2_HDIV_pred',     'Polyphen2_HDIV_pred',      'string',    'Polyphen2 prediction based on HumDiv, "D" ("probably damaging", HDIV score in [0.957,1] or rankscore in [0.52844,0.89865]), "P" ("possibly damaging", HDIV score in [0.453,0.956] or rankscore in [0.34282,0.52689]) and "B" ("benign", HDIV score in [0,0.452] or rankscore in [0.02634,0.34268]). Score cutoff for binary classification is 0.5 for HDIV score or 0.3528 for rankscore, i.e. the prediction is "neutral" if the HDIV score is smaller than 0.5 (rankscore is smaller than 0.3528), and "deleterious" if the HDIV score is larger than 0.5 (rankscore is larger than 0.3528). Multiple entries are separated by ";".', NULL),
  (4, '3.3a', 39, 'Polyphen2_HVAR_score',    'Polyphen2_HVAR_score',     'string',    'Polyphen2 score based on HumVar, i.e. hvar_prob. The score ranges from 0 to 1. Multiple entries separated by ";", corresponding to Uniprot_acc_Polyphen2.', NULL),
  (4, '3.3a', 40, 'Polyphen2_HVAR_rankscore','Polyphen2_HVAR_rankscore', 'float',     'Polyphen2 HVAR scores were first ranked among all HVAR scores in dbNSFP. The rankscore is the ratio of the rank the score over the total number of the scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0.01257 to 0.97092.', NULL),
  (4, '3.3a', 41, 'Polyphen2_HVAR_pred',     'Polyphen2_HVAR_pred',      'string',    'Polyphen2 prediction based on HumVar, "D" ("probably damaging", HVAR score in [0.909,1] or rankscore in [0.62797,0.97092]), "P" ("possibly damaging", HVAR in [0.447,0.908] or rankscore in [0.44195,0.62727]) and "B" ("benign", HVAR score in [0,0.446] or rankscore in [0.01257,0.44151]). Score cutoff for binary classification is 0.5 for HVAR score or 0.45833 for rankscore, i.e. the prediction is "neutral" if the HVAR score is smaller than 0.5 (rankscore is smaller than 0.45833), and "deleterious" if the HVAR score is larger than 0.5 (rankscore is larger than 0.45833). Multiple entries are separated by ";".', NULL),

  (4, '3.3a', 42, 'LRT_score',               'LRT_score',               'float',  'The original LRT two-sided p-value (LRTori), ranges from 0 to 1.', NULL),
  (4, '3.3a', 43, 'LRT_converted_rankscore', 'LRT_converted_rankscore', 'float',  'LRTori scores were first converted as LRTnew=1-LRTori*0.5 if Omega<1, or LRTnew=LRTori*0.5 if Omega>=1. Then LRTnew scores were ranked among all LRTnew scores in dbNSFP. The rankscore is the ratio of the rank over the total number of the scores in dbNSFP. The scores range from 0.00162 to 0.84324.', NULL),
  (4, '3.3a', 44, 'LRT_pred',                'LRT_pred',                'string', 'LRT prediction, D(eleterious), N(eutral) or U(nknown), which is not solely determined by the score.', NULL),
  (4, '3.3a', 45, 'LRT_Omega',               'LRT_Omega',               'float',  'Estimated nonsynonymous-to-synonymous-rate ratio (Omega, reported by LRT).', NULL),




  (4, '3.3a', 46, 'MutationTaster_score',               'MutationTaster_score',               'float',  'MutationTaster p-value (MTori), ranges from 0 to 1. Multiple scores are separated by ";". Information on corresponding transcript(s) can be found by querying http://www.mutationtaster.org/ChrPos.html', NULL),
  (4, '3.3a', 47, 'MutationTaster_converted_rankscore', 'MutationTaster_converted_rankscore', 'float',  'The MTori scores were first converted: if the prediction is "A" or "D" MTnew=MTori; if the prediction is "N" or "P", MTnew=1-MTori. Then MTnew scores were ranked among all MTnew scores in dbNSFP. If there are multiple scores of a  SNV, only the largest MTnew was used in ranking. The rankscore is the ratio of the rank of the score over the total number of MTnew scores in dbNSFP. The scores range from 0.08979 to 0.81033.', NULL),
  (4, '3.3a', 48, 'MutationTaster_pred',                'MutationTaster_pred',                'string', 'MutationTaster prediction, "A" ("disease_causing_automatic"), "D" ("disease_causing"), "N" ("polymorphism") or "P" ("polymorphism_automatic"). The score cutoff between "D" and "N" is 0.5 for MTnew and 0.31713 for the rankscore.', NULL),
  (4, '3.3a', 49, 'MutationTaster_model',               'MutationTaster_model',               'string', 'MutationTaster prediction models.', NULL),
  (4, '3.3a', 50, 'MutationTaster_AAE',                 'MutationTaster_AAE',                 'string', 'MutationTaster predicted amino acid change.', NULL),
  (4, '3.3a', 51, 'MutationAssessor_UniprotID',         'MutationAssessor_UniprotID',         'string', 'Uniprot ID number provided by MutationAssessor.', NULL),
  (4, '3.3a', 52, 'MutationAssessor_variant',           'MutationAssessor_variant',           'string', 'AA variant as to MutationAssessor_UniprotID.', NULL),
  (4, '3.3a', 53, 'MutationAssessor_score',             'MutationAssessor_score',             'float',  'MutationAssessor''s functional impact combined score (MAori). The score ranges from -5.135 to 6.49 in dbNSFP. ', NULL),
  (4, '3.3a', 54, 'MutationAssessor_rankscore',         'MutationAssessor_rankscore',         'float',  'MAori scores were ranked among all MAori scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MAori scores in dbNSFP. The scores range from 0 to 1.', NULL),
  (4, '3.3a', 55, 'MutationAssessor_pred',              'MutationAssessor_pred',              'string', 'MutationAssessor functional impact of a variant : predicted functional, i.e. high ("H") or medium ("M"), or predicted non-functional, i.e. low ("L") or neutral ("N"). The MAori score cutoffs between "H" and "M", "M" and "L", and "L" and "N", are 3.5, 1.935 and 0.8, respectively. The rankscore cutoffs between "H" and "M", "M" and "L", and "L" and "N", are 0.92922, 0.51944 and 0.19719, respectively.', NULL),







  (4, '3.3a', 56, 'Transcript_id_VEST3',  'Transcript_id_VEST3',     'string', 'Transcript id provided by VEST3.', NULL),
  (4, '3.3a', 57, 'Transcript_var_VEST3', 'Transcript_var_VEST3',    'string', 'amino acid change as to Transcript_id_VEST3.', NULL),
  (4, '3.3a', 58, 'VEST3_score',          'VEST3_score',             'string', 'VEST 3.0 score. Score ranges from 0 to 1. The larger the score the more likely the mutation may cause functional change. Multiple scores separated by ";", corresponding to Transcript_id_VEST3. Please note this score is free for non-commercial use. For more details please refer to http://wiki.chasmsoftware.org/index.php/SoftwareLicense. Commercial users should contact the Johns Hopkins Technology Transfer office.', NULL),
  (4, '3.3a', 59, 'VEST3_rankscore',      'VEST3_rankscore',         'float', 'VEST3 scores were ranked among all VEST3 scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of VEST3 scores in dbNSFP. In case there are multiple scores for the same variant, the largest score (most damaging) is presented. The scores range from 0 to 1.  Please note VEST score is free for non-commercial use. For more details please refer to http://wiki.chasmsoftware.org/index.php/SoftwareLicense. Commercial users should contact the Johns Hopkins Technology Transfer office.', NULL),



  (4, '3.3a', 60, 'MetaSVM_score',     'MetaSVM_score',     'float',  'Our support vector machine (SVM) based ensemble prediction score, which incorporated 10 scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster, Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in the 1000 genomes populations. Larger value means the SNV is more likely to be damaging. Scores range from -2 to 3 in dbNSFP.', NULL),
  (4, '3.3a', 61, 'MetaSVM_rankscore', 'MetaSVM_rankscore', 'float',  'MetaSVM scores were ranked among all MetaSVM scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MetaSVM scores in dbNSFP. The scores range from 0 to 1.', NULL),
  (4, '3.3a', 62, 'MetaSVM_pred',      'MetaSVM_pred',      'string', 'Prediction of our SVM based ensemble prediction score,"T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0. The rankscore cutoff between "D" and "T" is 0.82268.', NULL),
  (4, '3.3a', 63, 'MetaLR_score',      'MetaLR_score',      'float',  'Our logistic regression (LR) based ensemble prediction score, which incorporated 10 scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster, Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in the 1000 genomes populations. Larger value means the SNV is more likely to be damaging. Scores range from 0 to 1.', NULL),
  (4, '3.3a', 64, 'MetaLR_rankscore',  'MetaLR_rankscore',  'float',  'MetaLR scores were ranked among all MetaLR scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MetaLR scores in dbNSFP. The scores range from 0 to 1.', NULL),
  (4, '3.3a', 65, 'MetaLR_pred',       'MetaLR_pred',       'string', 'Prediction of our MetaLR based ensemble prediction score,"T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0.5. The rankscore cutoff between "D" and "T" is 0.81113.', NULL),




  (4, '3.3a', 66, 'Reliability_index',   'Reliability_index',    'float', 'Number of observed component scores (except the maximum frequency in the 1000 genomes populations) for MetaSVM and MetaLR. Ranges from 1 to 10. As MetaSVM and MetaLR scores are calculated based on imputed data, the less missing component scores, the higher the reliability of the scores and predictions.', NULL),




  (4, '3.3a', 67, 'M_CAP_score',     'M-CAP_score',     'float',  'M-CAP score (details in DOI: 10.1038/ng.3703). Scores range from 0 to 1. The larger the score the more likely the SNP has damaging effect.', NULL),
  (4, '3.3a', 68, 'M_CAP_rankscore', 'M-CAP_rankscore', 'float',  'M-CAP scores were ranked among all M-CAP scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of M-CAP scores in dbNSFP.', NULL),
  (4, '3.3a', 69, 'M_CAP_pred',      'M-CAP_pred',      'string', 'Prediction of M-CAP score based on the authors''s recommendation, "T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0.025.', NULL),

  (4, '3.3a', 70, 'CADD_raw',           'CADD_raw',           'float',  'CADD raw score for functional prediction of a SNP. Please refer to Kircher et al. (2014) Nature Genetics 46(4):310-5 for details. The larger the score the more likely the SNP has damaging effect. Scores range from -7.535037 to 35.788538 in dbNSFP. Please note the following copyright statement for CADD: "CADD scores (http://cadd.gs.washington.edu/) are Copyright 2013 University of Washington and Hudson-Alpha Institute for Biotechnology (all rights reserved) but are freely available for all academic, non-commercial applications. For commercial licensing information contact Jennifer McCullar (mccullaj@uw.edu)."', NULL),
  (4, '3.3a', 71, 'CADD_raw_rankscore', 'CADD_raw_rankscore', 'float',  'CADD raw scores were ranked among all CADD raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of CADD raw scores in dbNSFP. Please note the following copyright statement for CADD: "CADD scores (http://cadd.gs.washington.edu/) are Copyright 2013 University of Washington and Hudson-Alpha Institute for Biotechnology (all rights reserved) but are freely available for all academic, non-commercial applications. For commercial licensing information contact Jennifer McCullar (mccullaj@uw.edu)."', NULL),
  (4, '3.3a', 72, 'CADD_phred',         'CADD_phred',         'float', 'CADD phred-like score. This is phred-like rank score based on whole genome CADD raw scores. Please refer to Kircher et al. (2014) Nature Genetics 46(4):310-5 for details. The larger the score the more likely the SNP has damaging effect. Please note the following copyright statement for CADD: "CADD scores (http://cadd.gs.washington.edu/) are Copyright 2013 University of Washington and Hudson-Alpha Institute for Biotechnology (all rights reserved) but are freely available for all academic, non-commercial applications. For commercial licensing information contact Jennifer McCullar (mccullaj@uw.edu)."', NULL),

  (4, '3.3a', 73, 'DANN_score',     'DANN_score',     'float', 'DANN is a functional prediction score retrained based on the training data of CADD using deep neural network. Scores range from 0 to 1. A larger number indicate a higher probability to be damaging. More information of this score can be found in doi: 10.1093/bioinformatics/btu703. For commercial application of DANN, please contact Daniel Quang (dxquang@uci.edu)', NULL),
  (4, '3.3a', 74, 'DANN_rankscore', 'DANN_rankscore', 'float', 'DANN scores were ranked among all DANN scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of DANN scores in dbNSFP.', NULL),

  (4, '3.3a', 75, 'fathmm_MKL_coding_score',     'fathmm-MKL_coding_score',     'float',  'fathmm-MKL p-values. Scores range from 0 to 1. SNVs with scores >0.5 are predicted to be deleterious, and those <0.5 are predicted to be neutral or benign. Scores close to 0 or 1 are with the highest-confidence. Coding scores are trained using 10 groups of features. More details of the score can be found in doi: 10.1093/bioinformatics/btv009.', NULL),
  (4, '3.3a', 76, 'fathmm_MKL_coding_rankscore', 'fathmm-MKL_coding_rankscore', 'float',  'fathmm-MKL coding scores were ranked among all fathmm-MKL coding scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of fathmm-MKL coding scores in dbNSFP.', NULL),
  (4, '3.3a', 77, 'fathmm_MKL_coding_pred',      'fathmm-MKL_coding_pred',      'string', 'If a fathmm-MKL_coding_score is >0.5 (or rankscore >0.28317) the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "N(EUTRAL)".', NULL),
  (4, '3.3a', 78, 'fathmm_MKL_coding_group',     'fathmm-MKL_coding_group',     'string', 'the groups of features (labeled A-J) used to obtained the score. More details can be found in doi: 10.1093/bioinformatics/btv009.', NULL),

  (4, '3.3a', 79, 'Eigen_coding_or_noncoding', 'Eigen_coding_or_noncoding', 'bool',  'Whether Eigen-raw and Eigen-phred scores are based on coding (True) model or noncoding (False) model.', NULL),
  (4, '3.3a', 80, 'Eigen_raw',                 'Eigen-raw',                 'float', 'Eigen score for coding SNVs. A functional prediction score based on conservation, allele frequencies, and deleteriousness prediction using an unsupervised learning method (doi: 10.1038/ng.3477).', NULL),
  (4, '3.3a', 81, 'Eigen_phred',               'Eigen-phred',               'float', 'Eigen score in phred scale.', NULL),
  (4, '3.3a', 82, 'Eigen_PC_raw',              'Eigen-PC-raw',              'float', 'Eigen PC score for genome-wide SNVs. A functional prediction score based on conservation, allele frequencies, deleteriousness prediction (for missense SNVs) and epigenomic signals (for synonymous and non-coding SNVs) using an unsupervised learning method (doi: 10.1038/ng.3477).', NULL),
  (4, '3.3a', 83, 'Eigen_PC_phred',            'Eigen-PC-phred',            'float', 'Eigen PC score in phred scale.', NULL),
  (4, '3.3a', 84, 'Eigen_PC_raw_rankscore',    'Eigen-PC-raw_rankscore',    'float', 'Eigen-PC-raw scores were ranked among all Eigen-PC-raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of Eigen-PC-raw scores in dbNSFP.', NULL),

  (4, '3.3a', 85, 'GenoCanyon_score',          'GenoCanyon_score',           'float', 'A functional prediction score based on conservation and biochemical annotations using an unsupervised statistical learning. (doi:10.1038/srep10576)', NULL),
  (4, '3.3a', 86, 'GenoCanyon_rankscore',      'GenoCanyon_rankscore',       'float', 'GenoCanyon_score scores were ranked among all integrated fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of GenoCanyon_score scores in dbNSFP.', NULL),

  (4, '3.3a', 87, 'integrated_fitCons_score',     'integrated_fitCons_score',     'float', 'fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of nucleic sites of the functional class the genomic position belong to are under selective pressure, therefore more likely to be functional important. Integrated (i6) scores are integrated across three cell types (GM12878, H1-hESC and HUVEC). More details can be found  in doi:10.1038/ng.3196.', NULL),
  (4, '3.3a', 88, 'integrated_fitCons_rankscore', 'integrated_fitCons_rankscore', 'float', 'integrated fitCons scores were ranked among all integrated fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of integrated fitCons scores in dbNSFP.', NULL),
  (4, '3.3a', 89, 'integrated_confidence_value',  'integrated_confidence_value',  'float', '0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).', NULL),

  (4, '3.3a', 90, 'GM12878_fitCons_score',     'GM12878_fitCons_score',     'float', 'fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of nucleic sites of the functional class the genomic position belong to are under selective pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type GM12878. More details can be found in doi:10.1038/ng.3196.', NULL),
  (4, '3.3a', 91, 'GM12878_fitCons_rankscore', 'GM12878_fitCons_rankscore', 'float', 'GM12878 fitCons scores were ranked among all GM12878 fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of GM12878 fitCons scores in dbNSFP.', NULL),
  (4, '3.3a', 92, 'GM12878_confidence_value',  'GM12878_confidence_value',  'float', '0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).', NULL),





  (4, '3.3a', 93, 'H1_hESC_fitCons_score',     'H1-hESC_fitCons_score',     'float', 'fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of nucleic sites of the functional class the genomic position belong to are under selective pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type H1-hESC. More details can be found in doi:10.1038/ng.3196.', NULL),
  (4, '3.3a', 94, 'H1_hESC_fitCons_rankscore', 'H1-hESC_fitCons_rankscore', 'float', 'H1-hESC fitCons scores were ranked among all H1-hESC fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of H1-hESC fitCons scores in dbNSFP.', NULL),
  (4, '3.3a', 95, 'H1_hESC_confidence_value',  'H1-hESC_confidence_value',  'float', '0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).', NULL),

  (4, '3.3a', 96, 'HUVEC_fitCons_score',     'HUVEC_fitCons_score',     'float', 'fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of nucleic sites of the functional class the genomic position belong to are under selective pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type HUVEC. More details can be found in doi:10.1038/ng.3196.', NULL),
  (4, '3.3a', 97, 'HUVEC_fitCons_rankscore', 'HUVEC_fitCons_rankscore', 'float', 'HUVEC fitCons scores were ranked among all HUVEC fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of HUVEC fitCons scores in dbNSFP.', NULL),
  (4, '3.3a', 98, 'HUVEC_confidence_value',  'HUVEC_confidence_value',  'float', '0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).', NULL),




  (4, '3.3a', 99, 'GERPpp_NR',           'GERP++_NR',           'float',  'GERP++ neutral rate.', NULL),
  (4, '3.3a', 100, 'GERPpp_RS',           'GERP++_RS',           'float',  'GERP++ RS score, the larger the score, the more conserved the site. Scores range from -12.3 to 6.17.', NULL),
  (4, '3.3a', 101, 'GERPpp_RS_rankscore', 'GERP++_RS_rankscore', 'string', 'GERP++ RS scores were ranked among all GERP++ RS scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of GERP++ RS scores in dbNSFP.', NULL),



  (4, '3.3a', 102, 'phyloP100way_vertebrate',           'phyloP100way_vertebrate',           'float', 'phyloP (phylogenetic p-values) conservation score based on the multiple alignments of 100 vertebrate genomes (including human). The larger the score, the more conserved the site. Scores range from -20.0 to 10.003 in dbNSFP.', NULL),
  (4, '3.3a', 103, 'phyloP100way_vertebrate_rankscore', 'phyloP100way_vertebrate_rankscore', 'float', 'phyloP100way_vertebrate scores were ranked among all phyloP100way_vertebrate scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of phyloP100way_vertebrate scores in dbNSFP.', NULL),
  (4, '3.3a', 104, 'phyloP20way_mammalian',             'phyloP20way_mammalian',             'float', 'phyloP (phylogenetic p-values) conservation score based on the multiple alignments of 20 mammalian genomes (including human). The larger the score, the more conserved the site. Scores range from -13.282 to 1.199 in dbNSFP.', NULL),
  (4, '3.3a', 105, 'phyloP20way_mammalian_rankscore',   'phyloP20way_mammalian_rankscore',   'float', 'phyloP20way_mammalian scores were ranked among all phyloP20way_mammalian scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of phyloP20way_mammalian scores in dbNSFP.', NULL),



  (4, '3.3a', 106, 'phastCons100way_vertebrate',           'phastCons100way_vertebrate',           'float', 'phastCons conservation score based on the multiple alignments of 100 vertebrate genomes (including human). The larger the score, the more conserved the site. Scores range from 0 to 1.', NULL),
  (4, '3.3a', 107, 'phastCons100way_vertebrate_rankscore', 'phastCons100way_vertebrate_rankscore', 'float', 'phastCons100way_vertebrate scores were ranked among all phastCons100way_vertebrate scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of phastCons100way_vertebrate scores in dbNSFP.', NULL),
  (4, '3.3a', 108, 'phastCons20way_mammalian',             'phastCons20way_mammalian',             'float', 'phastCons conservation score based on the multiple alignments of 20 mammalian genomes (including human). The larger the score, the more conserved the site. Scores range from 0 to 1.', NULL),
  (4, '3.3a', 109, 'phastCons20way_mammalian_rankscore',   'phastCons20way_mammalian_rankscore',   'float', 'phastCons20way_mammalian scores were ranked among all phastCons20way_mammalian scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of phastCons20way_mammalian scores in dbNSFP.', NULL),




  (4, '3.3a', 110, 'SiPhy_29way_pi',                'SiPhy_29way_pi',                'string', 'The estimated stationary distribution of A, C, G and T at the site, using SiPhy algorithm based on 29 mammals genomes.', NULL),
  (4, '3.3a', 111, 'SiPhy_29way_logOdds',           'SiPhy_29way_logOdds',           'string', 'SiPhy score based on 29 mammals genomes. The larger the score, the more conserved the site. Scores range from 0 to 37.9718 in dbNSFP.', NULL),
  (4, '3.3a', 112, 'SiPhy_29way_logOdds_rankscore', 'SiPhy_29way_logOdds_rankscore', 'string', 'SiPhy_29way_logOdds scores were ranked among all SiPhy_29way_logOdds scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of SiPhy_29way_logOdds scores in dbNSFP.', NULL),




  (4, '3.3a', 113, '_1000Gp3_AC',     '1000Gp3_AC',     'int',   'Alternative allele counts in the whole 1000 genomes phase 3 (1000Gp3) data.', NULL),
  (4, '3.3a', 114, '_1000Gp3_AF',     '1000Gp3_AF',     'percent', 'Alternative allele frequency in the whole 1000Gp3 data.', NULL),
  (4, '3.3a', 115, '_1000Gp3_AFR_AC', '1000Gp3_AFR_AC', 'int',   'Alternative allele counts in the 1000Gp3 African descendent samples.', NULL),
  (4, '3.3a', 116, '_1000Gp3_AFR_AF', '1000Gp3_AFR_AF', 'percent', 'Alternative allele frequency in the 1000Gp3 African descendent samples.', NULL),
  (4, '3.3a', 117, '_1000Gp3_EUR_AC', '1000Gp3_EUR_AC', 'int',   'Alternative allele counts in the 1000Gp3 European descendent samples.', NULL),
  (4, '3.3a', 118, '_1000Gp3_EUR_AF', '1000Gp3_EUR_AF', 'percent', 'Alternative allele frequency in the 1000Gp3 European descendent samples.', NULL),
  (4, '3.3a', 119, '_1000Gp3_AMR_AC', '1000Gp3_AMR_AC', 'int',   'Alternative allele counts in the 1000Gp3 American descendent samples.', NULL),
  (4, '3.3a', 120, '_1000Gp3_AMR_AF', '1000Gp3_AMR_AF', 'percent', 'Alternative allele frequency in the 1000Gp3 American descendent samples.', NULL),
  (4, '3.3a', 121, '_1000Gp3_EAS_AC', '1000Gp3_EAS_AC', 'int',   'Alternative allele counts in the 1000Gp3 East Asian descendent samples.', NULL),
  (4, '3.3a', 122, '_1000Gp3_EAS_AF', '1000Gp3_EAS_AF', 'percent', 'Alternative allele frequency in the 1000Gp3 East Asian descendent samples.', NULL),
  (4, '3.3a', 123, '_1000Gp3_SAS_AC', '1000Gp3_SAS_AC', 'int',   'Alternative allele counts in the 1000Gp3 South Asian descendent samples.', NULL),
  (4, '3.3a', 124, '_1000Gp3_SAS_AF', '1000Gp3_SAS_AF', 'percent', 'Alternative allele frequency in the 1000Gp3 South Asian descendent samples.', NULL),




  (4, '3.3a', 125, 'TWINSUK_AC', 'TWINSUK_AC', 'int',   'Alternative allele count in called genotypes in UK10K TWINSUK cohort.', NULL),
  (4, '3.3a', 126, 'TWINSUK_AF', 'TWINSUK_AF', 'percent', 'Alternative allele frequency in called genotypes in UK10K TWINSUK cohort.', NULL),



  (4, '3.3a', 127, 'ALSPAC_AC', 'ALSPAC_AC', 'int',   'Alternative allele count in called genotypes in UK10K ALSPAC cohort.', NULL),
  (4, '3.3a', 128, 'ALSPAC_AF', 'ALSPAC_AF', 'percent', 'Alternative allele frequency in called genotypes in UK10K ALSPAC cohort.', NULL),




  (4, '3.3a', 129, 'ESP6500_AA_AC', 'ESP6500_AA_AC', 'int',   'Alternative allele count in the African American samples of the NHLBI GO Exome Sequencing Project (ESP6500 data set).', NULL),
  (4, '3.3a', 130, 'ESP6500_AA_AF', 'ESP6500_AA_AF', 'percent', 'Alternative allele frequency in the African American samples of the NHLBI GO Exome Sequencing Project (ESP6500 data set).', NULL),
  (4, '3.3a', 131, 'ESP6500_EA_AC', 'ESP6500_EA_AC', 'int',   'Alternative allele count in the European American samples of the NHLBI GO Exome Sequencing Project (ESP6500 data set).', NULL),
  (4, '3.3a', 132, 'ESP6500_EA_AF', 'ESP6500_EA_AF', 'percent', 'Alternative allele frequency in the European American samples of the NHLBI GO Exome Sequencing Project (ESP6500 data set).', NULL),




  (4, '3.3a', 133, 'ExAC_AC',     'ExAC_AC',     'int',   'Allele count in total ExAC samples (60,706 samples).', NULL),
  (4, '3.3a', 134, 'ExAC_AF',     'ExAC_AF',     'percent', 'Allele frequency in total ExAC samples.', NULL),
  (4, '3.3a', 135, 'ExAC_Adj_AC', 'ExAC_Adj_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in total ExAC samples.', NULL),
  (4, '3.3a', 136, 'ExAC_Adj_AF', 'ExAC_Adj_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in total ExAC samples.', NULL),
  (4, '3.3a', 137, 'ExAC_AFR_AC', 'ExAC_AFR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in African & African American ExAC samples.', NULL),
  (4, '3.3a', 138, 'ExAC_AFR_AF', 'ExAC_AFR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in African & African American ExAC samples.', NULL),
  (4, '3.3a', 139, 'ExAC_AMR_AC', 'ExAC_AMR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in American ExAC samples.', NULL),
  (4, '3.3a', 140, 'ExAC_AMR_AF', 'ExAC_AMR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in American ExAC samples.', NULL),
  (4, '3.3a', 141, 'ExAC_EAS_AC', 'ExAC_EAS_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in East Asian ExAC samples.', NULL),
  (4, '3.3a', 142, 'ExAC_EAS_AF', 'ExAC_EAS_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in East Asian ExAC samples.', NULL),

  (4, '3.3a', 143, 'ExAC_FIN_AC',         'ExAC_FIN_AC',         'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Finnish ExAC samples.', NULL),
  (4, '3.3a', 144, 'ExAC_FIN_AF',         'ExAC_FIN_AF',         'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Finnish ExAC samples.', NULL),
  (4, '3.3a', 145, 'ExAC_NFE_AC',         'ExAC_NFE_AC',         'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC samples.', NULL),
  (4, '3.3a', 146, 'ExAC_NFE_AF',         'ExAC_NFE_AF',         'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC samples.', NULL),
  (4, '3.3a', 147, 'ExAC_SAS_AC',         'ExAC_SAS_AC',         'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in South Asian ExAC samples.', NULL),
  (4, '3.3a', 148, 'ExAC_SAS_AF',         'ExAC_SAS_AF',         'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in South Asian ExAC samples.', NULL),
  (4, '3.3a', 149, 'ExAC_nonTCGA_AC',     'ExAC_nonTCGA_AC',     'int',   'Allele count in total ExAC_nonTCGA samples (53,105 samples).', NULL),
  (4, '3.3a', 150, 'ExAC_nonTCGA_AF',     'ExAC_nonTCGA_AF',     'percent', 'Allele frequency in total ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 151, 'ExAC_nonTCGA_Adj_AC', 'ExAC_nonTCGA_Adj_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in total ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 152, 'ExAC_nonTCGA_Adj_AF', 'ExAC_nonTCGA_Adj_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in total ExAC_nonTCGA samples.', NULL),

  (4, '3.3a', 153, 'ExAC_nonTCGA_AFR_AC', 'ExAC_nonTCGA_AFR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in African & African American ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 154, 'ExAC_nonTCGA_AFR_AF', 'ExAC_nonTCGA_AFR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in African & African American ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 155, 'ExAC_nonTCGA_AMR_AC', 'ExAC_nonTCGA_AMR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in American ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 156, 'ExAC_nonTCGA_AMR_AF', 'ExAC_nonTCGA_AMR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in American ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 157, 'ExAC_nonTCGA_EAS_AC', 'ExAC_nonTCGA_EAS_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in East Asian ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 158, 'ExAC_nonTCGA_EAS_AF', 'ExAC_nonTCGA_EAS_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in East Asian ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 159, 'ExAC_nonTCGA_FIN_AC', 'ExAC_nonTCGA_FIN_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Finnish ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 160, 'ExAC_nonTCGA_FIN_AF', 'ExAC_nonTCGA_FIN_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Finnish ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 161, 'ExAC_nonTCGA_NFE_AC', 'ExAC_nonTCGA_NFE_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 162, 'ExAC_nonTCGA_NFE_AF', 'ExAC_nonTCGA_NFE_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC_nonTCGA samples.', NULL),

  (4, '3.3a', 163, 'ExAC_nonTCGA_SAS_AC',  'ExAC_nonTCGA_SAS_AC',  'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in South Asian ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 164, 'ExAC_nonTCGA_SAS_AF',  'ExAC_nonTCGA_SAS_AF',  'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in South Asian ExAC_nonTCGA samples.', NULL),
  (4, '3.3a', 165, 'ExAC_nonpsych_AC',     'ExAC_nonpsych_AC',     'int',   'Allele count in total ExAC_nonpsych samples (45,376 samples).', NULL),
  (4, '3.3a', 166, 'ExAC_nonpsych_AF',     'ExAC_nonpsych_AF',     'percent', 'Allele frequency in total ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 167, 'ExAC_nonpsych_Adj_AC', 'ExAC_nonpsych_Adj_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in total ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 168, 'ExAC_nonpsych_Adj_AF', 'ExAC_nonpsych_Adj_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in total ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 169, 'ExAC_nonpsych_AFR_AC', 'ExAC_nonpsych_AFR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in African & African American ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 170, 'ExAC_nonpsych_AFR_AF', 'ExAC_nonpsych_AFR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in African & African American ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 171, 'ExAC_nonpsych_AMR_AC', 'ExAC_nonpsych_AMR_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in American ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 172, 'ExAC_nonpsych_AMR_AF', 'ExAC_nonpsych_AMR_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in American ExAC_nonpsych samples.', NULL),

  (4, '3.3a', 173, 'ExAC_nonpsych_EAS_AC', 'ExAC_nonpsych_EAS_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in East Asian ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 174, 'ExAC_nonpsych_EAS_AF', 'ExAC_nonpsych_EAS_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in East Asian ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 175, 'ExAC_nonpsych_FIN_AC', 'ExAC_nonpsych_FIN_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Finnish ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 176, 'ExAC_nonpsych_FIN_AF', 'ExAC_nonpsych_FIN_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Finnish ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 177, 'ExAC_nonpsych_NFE_AC', 'ExAC_nonpsych_NFE_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 178, 'ExAC_nonpsych_NFE_AF', 'ExAC_nonpsych_NFE_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in Non-Finnish European ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 179, 'ExAC_nonpsych_SAS_AC', 'ExAC_nonpsych_SAS_AC', 'int',   'Adjusted Alt allele counts (DP >= 10 & GQ >= 20) in South Asian ExAC_nonpsych samples.', NULL),
  (4, '3.3a', 180, 'ExAC_nonpsych_SAS_AF', 'ExAC_nonpsych_SAS_AF', 'percent', 'Adjusted Alt allele frequency (DP >= 10 & GQ >= 20) in South Asian ExAC_nonpsych samples.', NULL),




  (4, '3.3a', 181, 'clinvar_rs',           'clinvar_rs',           'string', 'rs number from the clinvar data set.', NULL),
  (4, '3.3a', 182, 'clinvar_clnsig',       'clinvar_clnsig',       'string', 'clinical significance as to the clinvar data set. 0 - unknown, 1 - untested, 2 - Benign, 3 - Likely benign, 4 - Likely pathogenic, 5 - Pathogenic, 6 - drug response, 7 - histocompatibility. A negative score means the the score is for the ref allele.', NULL),
  (4, '3.3a', 183, 'clinvar_trait',        'clinvar_trait',        'string', 'the trait/disease the clinvar_clnsig referring to.', NULL),
  (4, '3.3a', 184, 'clinvar_golden_stars', 'clinvar_golden_stars', 'string', 'ClinVar Review Status summary. 0 - no assertion criteria provided, 1 - criteria provided, single submitter, 2 - criteria provided, multiple submitters, no conflicts, 3 - reviewed by expert panel, 4 - practice guideline.', NULL),




  (4, '3.3a', 185, 'Interpro_domain',   'Interpro_domain',    'string', 'domain or conserved site on which the variant locates. Domain annotations come from Interpro database. The number in the brackets following a specific domain is the count of times Interpro assigns the variant position to that domain, typically coming from different predicting databases. Multiple entries separated by ";".', NULL),




  (4, '3.3a', 186, 'GTEx_V6_gene',   'GTEx_V6_gene',    'string', 'Target gene of the (significant) eQTL SNP.', NULL),
  (4, '3.3a', 187, 'GTEx_V6_tissue', 'GTEx_V6_tissue',  'string', 'Tissue type of the expression data with which the eQTL/gene pair is detected.', NULL);




UPDATE public.annotation_database SET uid=MD5(concat(id, version)) WHERE uid IS NULL;
UPDATE public.annotation_field SET uid=MD5(concat(database_id, database_version, name)) WHERE uid IS NULL;







DROP TABLE IF EXISTS public.import_dbnfsp_variant;

