Run these commands:

    pip install virtualenv
    python3 -m venv env
    pip install flask
    pip install pandas
    pip install mysql-connector-python

now go into testingFlask, and
    python form.py

It will open a command promt. Leave it.

Go to http://127.0.0.1:5000/

MAKE SURE TO ENTER YOUR OWN SQL DB PASSWORD in connect_mysql.py


DATA FLOW:

HTML:
crossRefhome.html

UI Python:
cr_home_search.py

Process:
cr_search_process.py

Backend:
cr_search_db.py