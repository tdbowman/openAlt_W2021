# User Manual
This document details how to get set-up if you would like to clone the repository and run the web server yourself.  

For video documentation, click [here](https://youtu.be/FStFargq8Uo).

## 1. Install the Dependencies
### 1.1 Windows
  * Install [Python 3.8.6](https://www.python.org/downloads/) and add it to your PATH.
  * Install MySQL using the [Windows Installer](https://dev.mysql.com/downloads/installer/). Be sure to install the Python connector and workbench.
  * Use pip to install the needed Python modules. This command will install them all at once:    
    `pip install schedule crossrefapi flask virtualenv python-dateutil flask-paginate pytz email-validator pandas smtplib ssl EmailMessage MIMEMultipart MIMEApplication MIMEText`
  * Install version 4.4 or higher of MongoDB community edition by by following the instructions in this [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/). 
### 1.2 Ubuntu
  * Install Python 3:  
  `sudo apt install Python3`
  * Python for Windows includes pip3 but on Ubuntu we need to install it with:  
  `sudo apt install python3-pip`
  * Install the first set of needed Python modules:  
  `pip3 install schedule crossrefapi flask virtualenv python-dateutil flask-paginate pytz email-validator pandas smtplib ssl EmailMessage MIMEMultipart MIMEApplication MIMEText `
  * Add the [mysql apt repository](https://dev.mysql.com/downloads/repo/apt/) to your sources. You can use `dkpg -i` or just use Gnome Software Center to install it by double clicking it.
  * Update and install mysql-community-server:  
  `sudo apt update && sudo apt install mysql-community-server`
  * Check systemd to ensure the MySQL daemon is enabled and active:  
  `sudo systemctl status mysql ---- check that daemon is active and enabled`
  * Install the config will get the config you need for the last two pip modules:  
  `sudo apt-get install libmysqlclient-dev` 
  * Install the last of the Python modules:  
  `pip3 install flask-mysqldb mysql-connector-python`
  * Install the mysql-connector:  
  `sudo apt install mysql-connector-python-py3`
  * Install MySQL shell:  
  `sudo apt install mysql-shell`
  * Go into mysql shell by executing this command: `mysql --user root -p` and then execute  
  `SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));`
  * Install version 4.4 or higher of MongoDB community edition by by following the instructions in this [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/).

## 2. Setting up the Databases 📊
The Event data will be ingested into a MySQL database titled `crossRefEventDataMain`. The script to create it can be found [here](https://github.com/tdbowman/openAlt_W2021/blob/master/SQL/CrossrefeventdataWithMain/crossrefeventdataWithMain.sql).  
  
The journal, publisher, author, title, and date information is stored in a seperate MySQL database titled `doidata`. The script to create it can be found [here](https://github.com/tdbowman/openAlt_W2021/blob/master/SQL/DOI_Author_Database/doidataSchema.sql).

Anyone can use our scripts and database schemas to create and fill in `crossRefEventDataMain`, but you will need to use other methods to fill in the needed fields for `doidata`. This [GitHub repository](https://github.com/fabiobatalha/crossrefapi) is a good place to start.

The `OpenCitations` database can be created using the opencitationsSchema.sql that can be found [here](https://github.com/tdbowman/openAlt_W2021/blob/master/SQL/OpenCitations/opencitationsSchema.sql).

The 'BulkSearchStats' database is necessary for the bulk search limitation to avoid user abuse of the system. The schema to create this database can be found [here](https://github.com/tdbowman/openAlt_W2021/tree/master/SQL/BulkSearchStats).

## 3. Update Configs 📝
1) After creation of the SQL tables, edit the config file to match your database credentials. The config file can be found [here](https://github.com/tdbowman/openAlt_W2021/blob/master/config/openAltConfig.json). 

2) In the project, update the `config_path` variable to match the directory of your config file. The variable can be found in the following files:
      * [content_domain_ingest.py](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/content_domain_ingest.py)
      * [fetchCitations.py](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/fetchCitations.py)
      * [fetchOpenCitations.py](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/fetchOpenCitations.py)
      * [fetchEventBuffer.py](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/Ingest/fetchEventBuffer.py)
      * [ingestMongoEvents.py](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/Ingest/ingestMongoEvents.py)
      * [app.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/app.py)
      * [dbQuery.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/dbQuery.py)
      * [emailAdmin.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/emailAdmin.py)
      * [uploadAuthor.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/uploadAuthor.py)
      * [uploadDOI.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/uploadDOI.py)
      * [uploadUni.py](https://github.com/tdbowman/openAlt_W2021/blob/master/web/uploadUni.py)

      This can be easily done in VS Code by hitting `Ctrl + Shift + F` and searching and replacing the variable.

## 4. Collecting and Ingesting the Events, Metadata, and Citations 🏷️
Before we can run the web server, we also need to collect the data from the Crossref API. This will take some time, as there are millions of events to collect. We highly recommend reading Crossref's [guide](https://www.eventdata.crossref.org/guide/) before continuing.  

Our Python script `openAlt/pythonScripts/Ingest/fetchEventBuffer.py` grabs new event data from the Crossref API. This data is retrieved in a JSON format into MongoDB, filtered and sorted through by the type of event it is, and then ingested into `crossrefeventdatamain` database. The retrieval of the data and ingestion may take time because there can be thousands of events related to one single publication. 

Author metadata for publications are also retrieved from the Crossref API. Metada can be fetched and ingested by running the `metadataThroughMongoDB.py` script which can be found [here](https://github.com/tdbowman/openAlt_W2021/blob/master/pythonScripts/metadataThroughMongoDB.py).

Citation data is retrieved from the OpenCitations API. This takes a long duration since a publication can have upwards of thousands of citations. We also recommend the reading the manual for OpenCitations API [here](https://opencitations.net/index/coci/api/v1).

`openAlt/pythonScripts/fetchOpenCitations.py` script can be run to fetch citation data for all of the publications of doidata database and store them in OpenCitations database.

### 4.1 Example of JSON Format:
Data retrieved from the third-party APIs will be retrieved as JSON format. Each API will have a unique format of the data. An example of data retrieved from the Crossref Event Data API will look like:
```JSON
{
        "license": "https:\/\/creativecommons.org\/publicdomain\/zero\/1.0\/",
        "obj_id": "https:\/\/doi.org\/10.1370\/afm.1970",
        "source_token": "a6c9d511-9239-4de8-a266-b013f5bd8764",
        "occurred_at": "2016-09-13T14:16:37Z",
        "subj_id": "https:\/\/reddit.com\/r\/UPFORFUN\/comments\/52koe6\/science_recommending_oral_probiotics_to_reduce\/",
        "id": "c831d209-a955-4e61-903d-40ef35b0e454",
        "evidence_record": "https:\/\/evidence.eventdata.crossref.org\/evidence\/201702226e03dbb4-bc2e-46e3-8c1e-d27f2d7fc1e4",
        "terms": "https:\/\/doi.org\/10.13003\/CED-terms-of-use",
        "action": "add",
        "subj": {
          "pid": "https:\/\/reddit.com\/r\/UPFORFUN\/comments\/52koe6\/science_recommending_oral_probiotics_to_reduce\/",
          "type": "post",
          "title": "[Science] Recommending Oral Probiotics to Reduce Winter Antibiotic Prescriptions in People With Asthma: A Pragmatic Randomized Controlled Trial",
          "issued": "2016-09-13T14:16:37.000Z"
        },
        "source_id": "reddit",
        "obj": {
          "pid": "https:\/\/doi.org\/10.1370\/afm.1970",
          "url": "http:\/\/www.annfammed.org\/content\/14\/5\/422.full"
        },
        "timestamp": "2017-02-22T16:15:50Z",
        "relation_type_id": "discusses"
}
```
## 5. Ingesting the Data 🗃️

### 5.1 Ingesting DOIs into main table
1. Open up MySQL Workbench.
    - Connect to your Local MySQL Connection.
2. Execute this SQL query `SELECT * FROM doidata._main_;`.
3. Import `openAlt_W2021/SQL/DOI_Author_Database/doi_mainTable_10k_V2.0.csv` to the `doidata._main_` table.


### 5.2 Ingesting from SciELO
We recevied a dump of data for articles from [SciELO](https://scielo.org/) that are from Brazil. This dump is located at `openAlt/pythonScripts/SciELOPID` and includes PIDs for over 400,000+ records. These records are not for the public at this time and wil take time to gather all the information for each of the articles. It is recommended to run the following steps for about 10,000 records instead of the full 400,000 to see how the data is ingested.

#### Step By Step Guide:
1. Open up MySQL Workbench.
    - Connect to your Local MySQL Connection.
2. Execute this SQL command `SELECT * FROM doidata._main_`.
3. Go to this directory: `openAlt/pythonScripts` in the project files and locate the `getSciELO.py` file .
4. Navigate to the `openAlt/config` folder and locate `OpenAltConfig.json`. Change MySQL username and password to suit your device.
5. Run `python getSciELO.py` in your preferred terminal from `openAlt/pythonScripts` to ingest in data from Crossref for the SciELO articles.
6. Run `python fetchEventBuffer.py` in your preferred terminal from `openAlt/pythonScripts/Ingest` to ingest in event data for the articles.
7. Run `python metadataThroughMongoDB.py` in your preferred terminal from `openAlt/pythonScripts` to ingest in metadata for the articles.
8. Run `python fetchOpenCitations.py` in your preferred terminal from `openAlt/pythonScripts` to ingest in citation and reference data for the articles.

### 6. Quirks of the Crossref Event API ❓
* Some Events give a DOI(objectID) as https://doi.org. For example, the event with ID: `5c83ca20-d4a1-471b-a23f-f21486cefb5c` will follow that format. 
* Event IDs are unique to each DOI.
* The Crossref Event API defaults to only showing the first thousand events associated with each DOI. You must use the cursor provided to fetch the next set of data from the API until there are no more events to fetch.
* Some DOI's in the Crossref Event data are malformed.  
This appears to be an inability of the Crossref agent to process Arabic text. We have only observed this for Twitter events so far.  
For example, the event with ID `5dd6719b-8981-4712-988c-8c01f7ad760b` has a DOI(objectID) of:  
 ```
 "obj_id": "https://doi.org/www.kau.edu.sa/content.aspx?pg=%d9%88%d8%b8%d8%a7%d8%a6%d9%81-%d8%b4%d8%a7%d8%ba%d8%b1%d8%a9-%d8%b9%d9%84%d9%89-%d8%a8%d9%86%d8%af-%d8%a7%d9%84%d8%a7%d8%ac%d9%88%d8%b1-%d8%a8%d9%88%d9%83%d8%a7%d9%84%d8%a9-%d8%b4%d8%b7%d8%b1-%d8%a7%d9%84%d8%b7%d8%a7%d9%84%d8%a8%d8%a7%d8%aa"
 ```
* Many Twitter Events do not provide a link to the tweet as their subjectID. Instead, they have only `http://twitter.com` as their link.  Since these events do not contain useful links, we have designed the website to hide these events from the "Latest Events" section on the article dashboard. These events are still counted towards the total number of events for the author/article.

### 7. Initiating Cron Jobs
The purpose of the Cron Jobs is to gather new data and allow it to be fetched, sorted, and ingested from third-party APIs so that the databases are updated frequently. To set up the Cron Jobs, it must be run on Linux Terminal. To begin, you must first locate the path files of the following files: 
 * fetchEventBuffer.py
 * fetchOpenCitations.py
 * metadataThroughMongoDB.py

In addition to locating the path files of these files, you must also find the path file of the python library module. Without locating the python library, the Cron Jobs will not be able to execute the python scripts. Once these are found, you can begin to initiate the Cron Jobs. 

The command to access the Cron Job scheduler through the Linux Terminal is: `crontab -e`. This will allow you to set up the Cron Jobs. To do this, you must first indicate how frequently you would like to run the script, then you specify the path file of the python library module, and finally you specify the path file of the python script. After indicating the tasks to be run, you will initiate the Cron Jobs by entering this command: `sudo cron`. To check if the Cron Jobs are running, you can check the status of it by entering this command on the terminal: `sudo service cron status`.

## 8. How to run the web server 🖥️

### 8.1 Before we Start ✋
This guide assumes you are using Python 3.8, and have established the `crossrefeventdatamain`, `doidata`, `opencitations`, and `bulksearchstats` databases in MySQL. Check `openAlt/SQL/` for the relevant scripts.  
If you have Python 2 installed, you will need to substitute Python3 for Python below.  

### 8.2 Step by Step Guide 📝
These actions should be performed inside the `openAlt/web/` folder.
1) Install virtualenv: `pip install virtualenv`.
2) Create a virtual environment: `python -m virtualenv venv`.
3) Activate the environment:
    - Windows: `./venv/scripts/activate`.
    - Linux/Mac: `./venv/bin/activate`.
4) Install Flask and our dependencies to this virtual environment:
    - `pip install flask mysql-connector-python flask-mysqldb python-dateutil flask-paginate pytz email-validator pandas smtplib ssl EmailMessage MIMEMultipart MIMEApplication MIMEText`.
5) Create a new file named 'passwd.txt'.
    - Open the file and type only your MySQL user password.
    - Save and close.
    - This file is ignored by git but used by app.py to access your local MySQL server.
6) Navigate to config folder and locate `OpenAltConfig.json`. Change MySQL username and password to suit your device.
7) If you are not using the root MySQL user account, you will need to change the user on line 19 in `app.py`.
8) Start the web server using `python app.py`.
9) When the web server starts, navigate to [127.0.0.1:5000](127.0.0.1:5000).




