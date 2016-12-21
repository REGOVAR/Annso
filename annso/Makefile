init:
	pip install -r requirements.txt

test:
	python tests.py

app:
	python annso_server.py

reset:
	psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'annso'"
	psql -U postgres -c "DROP DATABASE annso"
	psql -U postgres -c "CREATE DATABASE annso OWNER annso"
	psql -U annso -d annso -f ./database/create_all.sql
	psql -U annso -d annso -f /tmp/hg19_db/refGene.sql
	

.PHONY: init test app reset
