refGen
======
 * create you temps local folder and go inside
 * Download refgen : wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz (find db url here : http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/)
 * Unzip file : gzip -d refGene.txt.gz
 * update the Annso/annso/database/scripts/import_refgen.sql script with the path where you unzip the refGene.txt file
 * run the sql script on the annso database : psql -U annso -d annso -f Annso/annso/database/scripts/import_refgen.sql
 
 
dbNSFP
======
 * create you temps local folder and go inside
 * Download dbNSFP : wget 'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv3.3a.zip' (find db url here : https://sites.google.com/site/jpopgen/dbNSFP)
 * Unzip file : unzip dbNSFPv3.3a.zip -d .
 * update the Annso/annso/database/scripts/import_dbNFSP.sql script with the path where you unzip the file
 * run the sql script on the annso database : psql -U annso -d annso -f Annso/annso/database/scripts/import_dbNFSP.sql
 * run the Annso/annso/database/scripts/import_dbNFSP.py python script to compute bin indexes (can take several days)
 * python3 Annso/annso/database/scripts/import_dbNFSP.py &!
 
