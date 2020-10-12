# Building an Interface for Crossref Event Data

Hassan Bachir, Mitchell Fenner, Mohammad Riyadh, Ponnila Sampath Kumar, Dr. Timothy Bowman 
See the full documentation on the [Jupyter README](https://github.com/tdbowman-CompSci-F2020/crossrefEventData/blob/master/readme.ipynb).
## Overview
The goal of this project is to create a dashboard-style interface that displays activity and engagement surrounding scientific publications.  

[Crossref](https://www.crossref.org/) is an official agency responsible for assigning DOIs (Document Object Identifier) to published papers. Their API provides a substantial amount of data, which is used to create dashboards such as Google Scholar, Web of Science, and Scopus. Due to differences between platforms, h-index, i10-index, and citation counts vary depending on which site you use.  

We will work to create a web interface that organizes, simplifies, and visualizes this data. Our web interface will also rank authors in a consistent, and well documented way to facilitate bibliometric and altmetric research.

## How it works
### Collecting and organizing the Events
The Python script `pythonScripts/tapAPI.py` pulls down data on a regular schedule from the crossref API. This data is stored as a dated JSON file, each file containing 10,000 Events.
These files are then ingested into the database by `pythonScripts/Ingest/main.py`. Which reads each JSON in the data directory, and inserts it into our MySQL database.  
Because the Events do not contain the authors, journal, or article title for every DOI, we are developing more scripts to fetch that data from crossref based on the gaps in our database.
### The website
We are developing a website which will allow users to search our database for DOI's, authors, article titles, or journals. Users will be able to see how many Events, and of which type, a given article or author has generated.

## Dependencies
* MySQL 8.0.21
* MySQL Python Connector 8.0.21
* Python 3.8
* Bootstrap 3.3.7
* Python Modules (These may be installed with `pip3 install <name of module>`)
    * schedule
    * crossrefapi
    * mysql-connector-python
    * flask
    * flask-mysqldb
    * virtualenv

## Acknowledgements
We would like to thank:  
* Dr. Timothy Bowman for the project idea and guidance! 💡  
* Minh Nguyen for assisting us with technical questions 💬 
* Seyed Ziae Mousavi Mojab for teaching the class, of which this project was a part 🍎
