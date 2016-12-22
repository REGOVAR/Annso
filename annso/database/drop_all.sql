
-- 
-- DROP ALL
--

--
-- psql -U postgres -d annso -f database/drop_all.sql
--



DROP TABLE IF EXISTS public."sample_file" CASCADE;
DROP TABLE IF EXISTS public."project_sample" CASCADE;

DROP TABLE IF EXISTS public."sample_variant_hg19" CASCADE;
DROP TABLE IF EXISTS public."regmut_hg19" CASCADE;
DROP TABLE IF EXISTS public."variant_hg19" CASCADE;
DROP TABLE IF EXISTS public."sample" CASCADE;
DROP TABLE IF EXISTS public."file" CASCADE;
DROP TABLE IF EXISTS public."reference" CASCADE;
DROP TABLE IF EXISTS public."subject_patient" CASCADE;
DROP TABLE IF EXISTS public."subject_relation" CASCADE;
DROP TABLE IF EXISTS public."subject" CASCADE;
DROP TABLE IF EXISTS public."selection" CASCADE;
DROP TABLE IF EXISTS public."analysis" CASCADE;
DROP TABLE IF EXISTS public."template" CASCADE;
DROP TABLE IF EXISTS public."project" CASCADE;
DROP TABLE IF EXISTS public."user" CASCADE;
DROP TABLE IF EXISTS public."annotation_fields" CASCADE;
DROP TABLE IF EXISTS public."annotation_database" CASCADE;
DROP TABLE IF EXISTS public."parameter" CASCADE;


DROP SEQUENCE IF EXISTS public."variant_hg19_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."sample_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."file_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."reference_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."subject_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."selection_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."analysis_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."project_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."template_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."user_id_seq" CASCADE;
DROP SEQUENCE IF EXISTS public."annotation_database_id_seq" CASCADE;


DROP TYPE IF EXISTS tpl_status CASCADE;
DROP TYPE IF EXISTS analysis_status CASCADE;
DROP TYPE IF EXISTS subject_relation_type CASCADE;
DROP TYPE IF EXISTS regmut_pathos CASCADE;
DROP TYPE IF EXISTS regmut_contrib CASCADE;
DROP TYPE IF EXISTS field_type CASCADE;



-- If doesn't work. you can try to force drop the de db and recreate it
-- psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"
-- psql -U postgres -c "DROP DATABASE annso"
-- psql -U postgres -c "CREATE DATABASE annso OWNER annso"

