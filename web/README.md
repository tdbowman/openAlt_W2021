## How to run the web server 

### Before we start
This guide assumes you are using Python 3.8, and have established the `crossrefeventdatamain` and `dr_bowman_doi_data_tables` databases in MySQL. See the SQL folder for the relevant scripts.  
If you have Python 2 installed, you will need to substitute Python for Python3 below.  

### Step by step guide
These actions should be performed here, at this level in the folder.
1) Install virtualenv: `pip install virtualenv`
2) Create a virtual environment: `python -m virtualenv venv`
3) Activate the environment:
    - Windows: `./venv/scripts/activate`
    - Linux/Mac: `./venv/bin/activate`
4) Install Flask and our dependencies to this virtual environment:
    - `pip install flask mysql-connector-python flask-mysqldb python-dateutil flask-paginate`
5) Create a new file named `passwd.txt`. Open the file, and type only your MySQL user password. Save and close. This file is ignored by git, but used by app.py to access your local MySQL server.
6) Start the web server using `python app.py`
7) When the web server starts, navigate to [127.0.0.1:5000](127.0.0.1:5000)