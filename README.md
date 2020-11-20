# Building an Interface for Crossref Event Data 
This is only an overview. Check the [manual](./USER_MANUAL.md) for more details.

## Overview 
Platforms such as Google Scholar and Web of Science allow users to search for authors, search by paper/article, and see how many citations a given paper has. The goal of this project is to create a dashboard-style interface that displays activity and engagement surrounding scientific publications. Rather than focusing on numbers of citations, we will be displaying the number of interactions. The data describing these interactions is taken from the [Crossref API](https://www.eventdata.crossref.org/guide/service/quickstart/).  

## Where the data comes from 
Crossref is an official agency responsible for assigning DOIs (Document Object Identifier) to published research. They scrape the web across 13 different platforms (Twitter, Reddit, Wikipedia, and others) looking for interactions with scientific papers.
These interactions can be in the form of tweets, reddit posts, or wikipedia references. See the Crossref [documentation](https://www.eventdata.crossref.org/guide/data/about-the-data/) to learn about the platforms. 

## The Website 
We are developing a website which will allow users to search our databases for DOI's, authors, paper titles, or journals. Users will be able to see how many Events, and of which type, a given paper or author has generated. The number of papers published per year for a given journal will also be shown.

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
| jQRangeSlider 5.7.2             | MIT & GPL License                  |

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
| flask-paginate            | BSD-3-Clause License       |

<br>

## 	Acknowledgements 
We would like to thank:  
* Dr. Timothy Bowman for the project idea and guidance! 💡  
* Minh Nguyen for assisting us with technical questions 💬 
* Seyed Ziae Mousavi Mojab for teaching the class, of which this project was a part 🍎
