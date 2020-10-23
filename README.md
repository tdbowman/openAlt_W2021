# Building an Interface for Crossref Event Data

Hassan Bachir, Mitchell Fenner, Mohammad Riyadh, Ponnila Sampath Kumar, Dr. Timothy Bowman 

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

Search page image is from [99images.com](https://www.99images.com/wallpapers/travel-world/detroit-city-android-iphone-desktop-hd-backgrounds-wallpapers-1080p-4k-r1zh/193037)

## Acknowledgements
We would like to thank:  
* Dr. Timothy Bowman for the project idea and guidance! 💡  
* Minh Nguyen for assisting us with technical questions 💬 
* Seyed Ziae Mousavi Mojab for teaching the class, of which this project was a part 🍎
