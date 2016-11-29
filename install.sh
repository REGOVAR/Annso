
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser --interactive # username:annso superuser y
sudo -u postgres createdb annso


sudo apt-get install libmagickwand-dev --fix-missing # for python wand (report generation)





apt install nginx uwsgi
mkdir /regovar
chown 
cd /regovar/regovar







touch /etc/nginx/sites-available/regovar
echo "server 
{
	listen      80;
	server_name regovar.org;
	charset     utf-8;
	client_max_body_size 75M;

	location / { try_files $uri @regovar; }
	location @regovar {
	include uwsgi_params;
	uwsgi_pass unix:/tmp/uwsgi.sock;
}  



}

location = /regovar/regovar 
{ 
	rewrite ^ /regovar/regovar/; 
} 
location /regovar/regovar 
{ 
	try_files $uri @regovar/regovar; 
}
location @regovar/regovar 
{
  include uwsgi_params;
  uwsgi_pass unix:/tmp/regovar.sock;
}" > /etc/nginx/sites-available/regovar


cd /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/regovar regovar
cd /regovar/regovar




uwsgi -s /tmp/uwsgi.sock --manage-script-name --mount /regovar/regovar=app:app &
