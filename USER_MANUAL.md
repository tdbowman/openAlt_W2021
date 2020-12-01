# User Manual
This document details how to get set-up if you would like to clone the repository and run the web server yourself.  
Please make sure you have installed the dependencies listed in the [README](https://github.com/tdbowman-CompSci-F2020/openAlt/blob/master/README.md) before continuing.

## 1. Setting up the Databases 📊
The Event data will be ingested into a MySQL database titled `crossRefEventDataMain`. The script to create it can be found [here](https://github.com/tdbowman-CompSci-F2020/openAlt/blob/master/SQL/CrossrefeventdataWithMain/crossrefeventdataWithMain.sql).  
  
The journal, publisher, author, title, and date information is stored in a seperate MySQL database titled `dr_bowman_doi_data_tables`. The script to create it can be found [here](https://github.com/tdbowman-CompSci-F2020/openAlt/blob/master/SQL/DOI_Author_Database/dr_bowman_doi_data_tables.sql).

Anyone can use our scripts and database schemas to create and fill in `crossRefEventDataMain`, but you will need to use other methods to fill in the needed fields for `dr_bowman_doi_data_tables`. This [GitHub repository](https://github.com/fabiobatalha/crossrefapi) is a good place to start.

## 2. Collecting and Organizing the Events 🏷️
Before we can run the web server, we need to collect the data from the Crossref API. This will take some time, as there are millions of events to collect. We highly recommend reading Crossref's [guide](https://www.eventdata.crossref.org/guide/) before continuing.  

Our Python script `openAlt/pythonScripts/tapAPI.py` grabs new Event data from the Crossref API on a schedule. This data is stored as a dated JSON file, where each file contains 10,000 Events. You will need to enter your email on line 19, and can modify the schedule on line 35.

### 2.1 Example JSON Format:
Downloaded JSON files will look similar to this. Each of the 13 Event types has a unique format.  
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

## 3. Ingesting the Data 🗃️
These files will need to be ingested into the database by the following script: `openAlt/pythonScripts/Ingest/main.py`. This script reads each JSON in the data directory, and inserts the events into the MySQL database. Again, the Event data does not contain the journal, publisher, authors, or titles for the DOI's. We utilized Dr. Bowman's database which was already populated with this data when we started this project. If you are cloning the repository, *you will need to source this data yourself*. This GitHub [repository](https://github.com/fabiobatalha/crossrefapi) is a good place to start.

### 3.1 Ingesting from JSON files
#### Step by step guide:
1. Create a file inside this folder: `openAlt/pythonScripts/Ingest` named `passwd.txt`. The only line in this file should be your MySQL password.
2. Change the datadirectory for your JSON folder to suit your system (line 30). *Note, if not using the root MySQL account, you will need to change the MySQL user on line 31*.  
3. Run `python main.py` in your preferred terminal.

### 3.2 Ingesting from PaperBuzz Data
We were fortunate enough to be given a dump of Crossref JSON data from the nice folks at [Paperbuzz](http://paperbuzz.org/). This one time dump we recieved is simply Crossref Event data stored in a slighly different way. Here we document how we ingested this data, but can not provide a means for others to aquire this data. While the first 10,000 of such records are located in `openAlt/SQL/DOI_Author_Database/doi_json_dump_10k.csv`, we are not making the remaining data public at this time. Anyone cloning the repository will need to use see section 2.1 and ingest JSON data which they gather themselves.

#### Step By Step Guide:
1. Create a file inside `openAlt/pythonScripts/Ingest` named `passwd.txt`. The only line in this file should be your MySQL password.
2. Open up MySQL Workbench.
    - Connect to your Local MySQL Connection.
3. Create a new database within Workbench.
    - File -> Open SQL Script.
	    - Go to this directory: `openAlt/SQL/paperbuzz_dump/`.
      - Open `paperbuzz.sql`.
    - Execute the script(⚡).
    - Organization Tip **(Recommendation but not required)**
      - File -> New Query Tab(CTRL + T).
      - This step is not required however it can be helpful. Any SQL commands that you want to execute for a database or table can be placed here in the new tab. It allows you to use the script purely for creating the database/table(s) while using another tab to execute commands for that database.
    - Execute this SQL query `SELECT * FROM event_data_json;`.
      - Import `json_dump_10k.csv` to the event_data_json table.
3. Ignore steps 1 - 3 if you already have a database containing the Paperbuzz data dump.
4. Execute this SQL command `DROP DATABASE crossrefeventdatawithmain`.
5. Go to this directory: `openAlt\SQL\CrossrefeventdataWithMain`.
    - Execute the SQL script `crossrefeventdataWithMain.sql` to create all 13 tables.
6. If you are not using the root MySQL user account, you will need to change the user on line 28.
7. Run `python paperBuzzMain.py` in your preferred terminal.

### 4. Quirks of the Crossref API ❓
* Some Events give a DOI(objectID) of simply https://doi.org. For example, the event with ID: `5c83ca20-d4a1-471b-a23f-f21486cefb5c`
* Some DOI's in the Crossref Event data are malformed.  
This appears to be an inability of the Crossref agent to process Arabic text. We have only observed this for Twitter events so far.  
For example, the event with ID `5dd6719b-8981-4712-988c-8c01f7ad760b` has a DOI(objectID) of:  
 ```
 "obj_id": "https://doi.org/www.kau.edu.sa/content.aspx?pg=%d9%88%d8%b8%d8%a7%d8%a6%d9%81-%d8%b4%d8%a7%d8%ba%d8%b1%d8%a9-%d8%b9%d9%84%d9%89-%d8%a8%d9%86%d8%af-%d8%a7%d9%84%d8%a7%d8%ac%d9%88%d8%b1-%d8%a8%d9%88%d9%83%d8%a7%d9%84%d8%a9-%d8%b4%d8%b7%d8%b1-%d8%a7%d9%84%d8%b7%d8%a7%d9%84%d8%a8%d8%a7%d8%aa"
 ```
* Many Twitter Events do not provide a link to the tweet as their subjectID. Instead, they have only `http://twitter.com` as their link.  Since these events do not contain useful links, we have designed the website to hide these events from the "Latest Events" section on the article dashboard. These events are still counted towards the total number of events for the author/article.

## 5. How to run the web server 🖥️

### 5.1 Before we Start ✋
This guide assumes you are using Python 3.8, and have established the `crossrefeventdatamain` and `dr_bowman_doi_data_tables` databases in MySQL. Check `openAlt/SQL/` for the relevant scripts.  
If you have Python 2 installed, you will need to substitute Python3 for Python below.  

### 5.2 Step by Step Guide 📝
These actions should be performed inside the `openAlt/web/` folder.
1) Install virtualenv: `pip install virtualenv`.
2) Create a virtual environment: `python -m virtualenv venv`.
3) Activate the environment:
    - Windows: `./venv/scripts/activate`
    - Linux/Mac: `./venv/bin/activate`
4) Install Flask and our dependencies to this virtual environment:
    - `pip install flask mysql-connector-python flask-mysqldb python-dateutil flask-paginate`
5) Create a new file named `passwd.txt`. 
    - Open the file, and type only your MySQL user password.
    - Save and close. 
    - This file is ignored by git, but used by app.py to access your local MySQL server.
6) Start the web server using `python app.py`
7) When the web server starts, navigate to [127.0.0.1:5000](127.0.0.1:5000)
