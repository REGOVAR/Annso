init:
	pip install -r requirements.txt

test:
	# ignore E302,E303 (to allow multiple blank line in the code)
	# ignore E501 too long line as (we have large screen now... and long sql queries...  <_< )
	flake8 . --statistics --exclude=__*  --ignore=E302,E303,E501 --exit-zero
	# python tests.py

app:
	python annso_server.py

drop:
	psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"
	psql -U postgres -c "DROP DATABASE annso"
	psql -U postgres -c "CREATE DATABASE annso OWNER annso"
	psql -U annso -d annso -f ./database/create_all.sql
	psql -U annso -d annso -f /tmp/hg19_db/refGene.sql
	
clear:
	psql -U annso -d annso -c "DELETE FROM sample_file"
	psql -U annso -d annso -c "DELETE FROM file"
	psql -U annso -d annso -c "DELETE FROM sample_variant_hg19"
	psql -U annso -d annso -c "DELETE FROM variant_hg19"
	psql -U annso -d annso -c "DELETE FROM analysis_sample"
	psql -U annso -d annso -c "DELETE FROM filter"
	psql -U annso -d annso -c "DELETE FROM attribute"
	psql -U annso -d annso -c "DELETE FROM analysis"
	psql -U annso -d annso -c "DELETE FROM sample"

	psql -U annso -d annso -c "DROP TABLE IF EXISTS csq_v76_hg19"
	psql -U annso -d annso -c "DROP TABLE IF EXISTS eff_4_2_hg19"
	psql -U annso -d annso -c "DELETE FROM annotation_database WHERE uid='be9dc0ad28f104b08178aad3aa1b3e0d'"
	psql -U annso -d annso -c "DELETE FROM annotation_field WHERE database_uid='be9dc0ad28f104b08178aad3aa1b3e0d'"
	psql -U annso -d annso -c "DELETE FROM annotation_database WHERE uid='6c4755844bbc192dd4bd92e54868896d'"
	psql -U annso -d annso -c "DELETE FROM annotation_field WHERE database_uid='6c4755844bbc192dd4bd92e54868896d'"



list_db:
	psql -U annso -d annso -c "SELECT relname as Table, pg_size_pretty(pg_total_relation_size(relid)) As Size, pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as ExternalSize, rowcount as RowCount \
    FROM pg_catalog.pg_statio_user_tables  \
    LEFT JOIN ( \
        SELECT table_name, n_tup_ins - n_tup_del as rowcount  \
        FROM (SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name) AS _t  \
        LEFT JOIN pg_stat_all_tables ON table_name=relname ORDER BY table_name) AS _sub ON table_name=relname \
    ORDER BY pg_total_relation_size(relid) DESC"

list_field:
	psql -U annso -d annso -c "select d.name, f.uid, f.name, f.name_ui from annotation_field f INNER JOIN annotation_database d ON f.database_uid=d.uid ORDER BY d.name, f.name"

free_db:
	psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"


.PHONY: init test app clear list_db list_field free_db
