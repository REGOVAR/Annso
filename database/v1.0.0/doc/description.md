[![Regovar datamodel](https://raw.githubusercontent.com/REGOVAR/regovar-server/master/database/v1.0.0/doc/db_schema.png)](https://raw.githubusercontent.com/REGOVAR/regovar-server/master/database/v1.0.0/doc/db_schema.png)

***

Current version : **V1.0.0**
* Download [create_all sql](https://raw.githubusercontent.com/REGOVAR/regovar-server/master/database/v1.0.0/create_all.sql)
* Download [drop_all sql](https://raw.githubusercontent.com/REGOVAR/regovar-server/master/database/v1.0.0/drop_all.sql)
* Download [import_all sql](https://raw.githubusercontent.com/REGOVAR/regovar-server/master/database/v1.0.0/import_all.sql)

***

## Tables descriptions



### user
_Store information related to Regovar's users._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the user                                       |
| email              | varchar(255) | email of the user                                                |
| password           | varchar(255) | SHA-2 token of the user's password                               |
| firstname          | varchar(255) | the firstname of the user                                        |
| astname            | varchar(255) | the lastname of the user                                         |
| location           | varchar(255) | the location where is working the user (CHU + City by example)   |
| function           | varchar(50)  | the job of the user or the service where he is working           |
| last_activity_date | datetime     | the last date when the user used one of the regovar applications |
| settings           | text         | the settings of the applications are saved online to alow user to retrieve it even if he have to use the application on another computer, or need to reinstall the application   |


### project
_A Regovar project; is like a folder on the OS. it's just here to organise and group analises and samples._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the project                                    |
| parent_id          | int          | [FK] can refer to another project id, the parent folder          |
| name               | varchar(50)  | the name of the project; (owner_id, name) shall be unique        |
| comments           | text         | some comments can be stored by project                           |
| data               | text         | JSON data that wrap several statistics/status about the content of this project |

Data in data dictionary :
* number of analyses
* number of samples
* space occupied in database / hard drive disk




### analysis
_many differents analyses can be conducted on the dataset of the project_

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the analysis                                   |
| name               | varchar(50)  | the name of the analysis                                         |
| project_id         | int          | [FK] the id of the project that own te analysis                  |
| owner_id           | integer      | [FK] the id of the user who created this project                 |
| comments           | text         | some comments can be stored about the analysis                   |
| template_id        | int          | the id of the template (pipe) on which this analysis is based    |
| template_settings  | text         | some custom parameters can be set for the analysis               |
| creation_date      | datetime     | the date when the analysis have been created                     |
| update_date        | datetime     | the last date when the analysis have been edited                 |
| is_archived        | bool         | if the analysis is archived or not; see [archiving analysis]() feature |
| status             | enum         | current status of the analysis : init, in progress, done         |



### selection
_A selection is a subset of variant obtained by applying filters_

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the user                                       |
| analysis_id        | int          | [FK] the id of the analysis                                      |
| name               | varchar(50)  | the displayed name of the selection                              |
| comments           | text         | some comments can be stored about the selection                  |
| order              | int          | selection are displayed in an ordered list that the user can arrange as he want|
| query              | text         | the JSON description of the query use to retrieve data of this selection|


### template
_A template describe a pipe or succession of operation that will be applied on the variants list to filter and do the annotation._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the template                                   |
| name               | varchar(50)  | the displayed name of the template                               |
| author_id          | int          | [FK] the id of the author of the template                        |
| description        | varchar(255) | a description of the pipe and what it does                       |
| version            | varchar(20)  | the version of the template                                      |
| creation_date      | datetime     | when the template have been created                              |
| update_date        | datetime     | the last time that the template have been edited                 |
| parent_id          | int          | if the template is a fork or a new version of another one, store the parent template |
| status             | enum         | the status of the pipe : draft, release candidate, validated     |
| configuration      | text         | the JSON dictionary that describe the pipe                       |




***

### file
_Data are imported from file, the file are then stored on a dedicated repository, and only the minimal information are stored in database to be able to retrieve them (for export or re-import by example)._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the file                                       |
| filename           | varchar(50)  | the displayed name of the file                                   |
| description        | varchar(255) | the description of the file if the user set it                   |
| type               | enum         | the type of the file (see [suported input file types]())         |
| reference_id       | int          | the description of the file if the user set it                   |


### subject
_Data imported in Regovar shall always be linked to a subject. A subject can be a human patient, or a bacteria, cells, virus, ..., the table subject is "abstract", and its hold all kinds of subjects. Several dedicated table will be created to wrap specific properties like the table "subject_patient". (Note that the "contact" field in the subject_patient table is to contact the patient himself or his familly, it's not the same that the contact field in the subject table) ._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the subject                                    |
| name               | varchar(255) | the displayed name of the subject                                |
| contact            | varchar(255) | used only when the contact is not the user that imported the data|
| comments           | text         | some comments about the subject                                  |




### subject_relation
_Describe relation between two subject. Actually the only relation is "id1 parent of id2". It seem to be enough to describe phylogenetic tree or familly tree for human's patient._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **subject1_id**    | int          | [PK/FK] id of the "left operand" subject in the relation         |
| **subject2_id**    | int          | [PK/FK] id of the "right operand" subject in the relation        |
| **relation**       | enum         | [PK] relation type : parent (only one for the moment)            |



### sample
_Several sample can be associated to a same subject. Do the link between, the file, the subject and the variants._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **id**             | serial       | [PK] unique id of the sample                                     |
| name               | varchar(50)  | the name of the sample                                           |
| comments           | text         | some comments about the sample                                   |
| file_id            | int          | [FK] id to the file where sample data are comming                |
| subject_id         | int          | [FK] id to the subject link to this sample                       |



### sample_variant[_hg19]
_Several sample can be associated to a same subject. Do the link between, the file, the subject and the variants. Note that data are variant are linked to a referencial. it's not possible to merge all referetial in the same table, that why the table is suffixed by hg19._

| Field          | Type              | Description                                                      |
| :------------- | :---------------- | :--------------------------------------------------------------- |
| **sample_id**  | serial            | [PK] unique id of the association sample-variant                 |
| bin            | int               | bin score of the variant                                         |
| **chr**        | varchar(50)       | the normalized name of the variant's chromosom                   |
| **pos**        | int               | the position of the variant in the chromosom                     |
| **ref**        | text              | the reference sequence                                           |
| **alt**        | text              | the alternative sequence of the variant                          |
| variant_id     | int               | [FK] a ref to the "unique" variant referenced in the Regovar db  |
| genotype       | varchar(1)        | is the variant, heterozygotic or homozygotic ...                 |
| deepth         | int               | the deepth of the variant in the sample                          |
| infos          | varchar(255)[ ][ ]| other information that can be found in the vcf related to the sample and the variant are stored here |



### variant[_hg19]
_As in sample_variant[_hg19], variant are duplicated (a same variant can be used in several sample), in this table we stored only one version of the version, with all general information and precalculated fields to improve the query speed._

| Field          | Type              | Description                                                      |
| :------------- | :---------------- | :--------------------------------------------------------------- |
| **id**         | serial            | [PK] unique id of the variant                                    |
| bin            | int               | bin score of the variant                                         |
| chr            | varchar(50)       | the normalized name of the variant's chromosom                   |
| pos            | int               | the position of the variant in the chromosom                     |
| ref            | text              | the reference sequence                                           |
| alt            | text              | the alternative sequence of the variant                          |
| sample_list    | int[ ]            | the list of sample that reference this variant                   |
| ...            | ...               | let see if we need others precalculated stats/fields ...         |





***

### omnisearch
_Store keyword to allow efficient search to retrieve a user, a sample, an analysis, ..._

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **keyord**         | varchar(50)  | [PK] a keyword                                                   |
| **object_type**    | enum         | [PK] the type of the associated object to the keyword            |
| id                 | int          | the id of the object                                             |
| snippet            | varchar(255) | an html snippet that will be used in the HMI to describe the object |

By object type, the fields list that will be checked to list keyword :
* **user** : 
   - table : user
   - fields : email, firstname, lastname, function, location
* **project** : 
   - table : project
   - fields : name
* **analysis** :
   - table : analysis
   - fields : name, status
* **subject** :
   - table : subject
   - fields : name, contact
* **patient** :
   - table : subject_patient
   - fields : firstname, lastname, birthdate, deathdate, contact
* **sample** :
   - table : sample
   - fields : name
* **file** :
   - table : file
   - fields : filename, type
* **phenotype** :
   - table : sample_phenotype
   - fields : name (via phenotype_id), is_present
* **characteristic** :
   - table : sample_characteristic
   - fields : name (via characteristic_id), value


### parameter
_Store common config / parameters_

| Field              | Type         | Description                                                      |
| :----------------- | :----------- | :--------------------------------------------------------------- |
| **key**            | varchar(50)  | [PK] unique key that identify the parameter                      |
| value              | varchar(255) | the stored value of the parameter                                |
| description        | varchar(255) | the description of the parameter                                 |

Parameter :
* **DatabaseVersion** : the current version of the database;
* **HeavyClientLastVersion** : the version available (and complient with this version of the database) for the last Regovar heavy client;
* **HeavyClient** : JSON dictionary with all information usefull for the Regovar Launcher to be able to download/update the heavy clients;
* **LastBackupDate** : the date of the last database dump;
* **RegovarDatabaseUUID* : UUID of the Regovar database; will be used for during export/import or synchronization with other databases in order to be able to know from where are comming new data imported into the database
