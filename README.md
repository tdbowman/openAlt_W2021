# Building an Interface for Crossref Event Data

## Overview

Platforms such as Google Scholar and Web of Science allow users to search for authors, search by paper/article, and see how many citations a given paper has. The goal of this project is to create a dashboard-style interface that displays activity and engagement surrounding scientific publications. Rather than focusing on numbers of citations, we will be displaying the number of interactions. The data describing these interactions is taken from the [Crossref API](https://www.eventdata.crossref.org/guide/service/quickstart/).  

## Where the data comes from

Crossref is an official agency responsible for assigning DOIs (Document Object Identifier) to published research. They scrape the web across 13 different platforms (Twitter, Reddit, Wikipedia, and others) looking for interactions with scientific papers.
These interactions can be in the form of tweets, reddit posts, or wikipedia references. See the Crossref [documentation](https://www.eventdata.crossref.org/guide/data/about-the-data/) to learn about the platforms. 
   
We are working to create a web interface that organizes, simplifies, and visualizes this data. Our web interface will also rank authors in a consistent, and well documented way to facilitate bibliometric and altmetric research.

## How it works

### Collecting and organizing the Events
The Python script `pythonScripts/tapAPI.py` grabs new Event data from the Crossref API every day. This data is stored as a dated JSON file, where each file contains 10,000 Events.  
#### Example JSON format:
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
These files are then ingested into the database by another script: `pythonScripts/Ingest/main.py`. This script reads each JSON in the data directory, and inserts it into our MySQL database. Because the Event data does not contain the journal, publisher, authors, or titles for the DOI's, we are utilizing Dr. Bowman's database which is already populated with this data.

### The databases
The Event data is ingested into a MySQL database titled `crossRefEventDataMain`. The script to create it can be found [here](https://github.com/tdbowman-CompSci-F2020/crossrefEventData/blob/master/SQL/CrossrefeventdataWithMain/crossrefeventdataWithMain.sql).  
  
The journal, publisher, author, title, and date information is stored in a seperate MySQL database titled `dr_bowman_doi_data_tables`. The script to create it can be found [here](https://github.com/tdbowman-CompSci-F2020/crossrefEventData/blob/master/SQL/DOI_Author_Database/dr_bowman_doi_data_tables.sql).

Anyone can use our scripts and database schemas to create and fill in `crossRefEventDataMain`, but you will need to use other methods to fill in the needed fields for `dr_bowman_doi_data_tables`. This [GitHub repository](https://github.com/fabiobatalha/crossrefapi) is a good place to start.

### The website
We are developing a website which will allow users to search our databases for DOI's, authors, paper titles, or journals. Users will be able to see how many Events, and of which type, a given paper or author has generated. The number of papers published per year for a given journal will also be shown.

## Quirks of the Crossref API
* Some Events give a DOI(objectID) of simply https://doi.org. For example, the event with ID: `5c83ca20-d4a1-471b-a23f-f21486cefb5c`
* Some DOI's in the Crossref Event data are malformed.  
This appears to be an inability of the Crossref agent to process Arabic text. We have only observed this for Twitter events so far.  
For example, the event with ID `5dd6719b-8981-4712-988c-8c01f7ad760b` has a DOI(objectID) of:  
 ```
 "obj_id": "https://doi.org/www.kau.edu.sa/content.aspx?pg=%d9%88%d8%b8%d8%a7%d8%a6%d9%81-%d8%b4%d8%a7%d8%ba%d8%b1%d8%a9-%d8%b9%d9%84%d9%89-%d8%a8%d9%86%d8%af-%d8%a7%d9%84%d8%a7%d8%ac%d9%88%d8%b1-%d8%a8%d9%88%d9%83%d8%a7%d9%84%d8%a9-%d8%b4%d8%b7%d8%b1-%d8%a7%d9%84%d8%b7%d8%a7%d9%84%d8%a8%d8%a7%d8%aa"
 ```
* Many Twitter Events do not provide a link to the tweet as their subjectID. Instead, they have only `http://twitter.com` as their link.  Since these events do not contain useful links, we have designed the website to hide these events from the "100 recent events" section on the article dashboard. These events are still counted towards the author/article totals.

## Dependencies and their Licenses

| Software                        | License                            |
|:--------------------------------|:-----------------------------------|
| MySQL 8.0.21                    | GPL-2.0 License                    |
| MySQL Python Connector 8.0.21   | GPL-2.0 License                    |
| Python 3.8                      | Python Software Foundation License |
| Bootstrap 3.3.7                 | MIT License                        |
| C3 0.7.20                       | MIT License                        |
| D3 v5                           | BSD-3-Clause License               |
| jQuery 3.5.1                    | MIT License                        |
<br>

| Python Module             | License                    |
|:--------------------------|:---------------------------|
| schedule                  | MIT License                |
| crossrefapi               | BSD-2-Clause License       |
| mysql-connector-python    | GPL-2.0 License            |
| flask                     | BSD-3-Clause License       |
| flask-mysqldb             | MIT License                |
| virtualenv                | MIT License                |
| python-dateutil           | Apache-2.0 License         |


## Acknowledgements
We would like to thank:  
* Dr. Timothy Bowman for the project idea and guidance! 💡  
* Minh Nguyen for assisting us with technical questions 💬 
* Seyed Ziae Mousavi Mojab for teaching the class, of which this project was a part 🍎
