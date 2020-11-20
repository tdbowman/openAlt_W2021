import flask
from flask_mysqldb import MySQL
from flask import request, jsonify
import json
from datetime import datetime

# Import our functions for other pages
from searchLogic import searchLogic
from articleDashboardLogic import articleDashboardLogic
from journalDashboardLogic import journalDashboardLogic
from authorDashboardLogic import authorDashboardLogic
from getPassword import getPassword
from landingPageStats import landingPageStats
from landingPageArticles import landingPageArticles
from landingPageJournals import landingPageJournals

# get the users password from crossrefeventdata/web/passwd.txt
mysql_password = getPassword()

# Instantiate an object of class Flask
app = flask.Flask(__name__)
# Database connection settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = mysql_password
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'dr_bowman_doi_data_tables'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Database initialization and cursor
mysql = MySQL(app)

# Instantiate a second object of class Flask
app2 = flask.Flask(__name__)
# Database connection settings
app2.config['MYSQL_USER'] = 'root'
app2.config['MYSQL_PASSWORD'] = mysql_password
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app2.config['MYSQL_DB'] = 'crossrefeventdatamain'
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql2 = MySQL(app2)


@app.route('/')
def index():
    totalSum = landingPageStats(mysql)
    totalSumArticles = landingPageArticles(mysql)
    totalSumJournals = landingPageJournals(mysql)
    return flask.render_template('index.html', totalSum=totalSum, totalSumArticles=totalSumArticles, totalSumJournals=totalSumJournals)


@app.route('/searchResultsPage', methods=["GET", "POST"])
def search():

    if(request.method == "POST"):
        print("POST Method Received!")
        dropdownValue = request.form.get('dropdownSearchBy')
        print(dropdownValue)

    return searchLogic(mysql, mysql2, dropdownValue)


@app.route('/articleDashboard', methods=["GET", "POST"])
def articleDashboard():
    # TypeError: 'NoneType' object is not subscriptable

    # ***********Year Range Slider decomissioned until after P3 ***************
    # try:
    #     years_list = []
    #     print("This is the default year range.")
    #     currentYear = datetime.now().year
    #     for i in range(currentYear - 4, currentYear + 1):
    #         years_list.append(i)
    #     print(years_list)
    #     if request.method == "POST":
    #         print("Received POST method request ")
    #         if request.get_json() is not None:
    #             years_list = []
    #             print("JSON is not None")
    #             bounds = request.get_json()
    #             print("Bounds grabbed from ajax call: ", bounds)
    #             for i in range(bounds['min'], bounds['max'] + 1):
    #                 years_list.append(i)
    #             print(years_list)
    # except Exception as e:
    #     print("The error was " + str(e))

    # for i in range(bounds['min'], bounds['max'])
    # ------------------------------------------------

    years_list = []
    yearInput = ''

    print("This is the default year range.")
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)
    print(years_list)
    if request.method == "POST":
        if request.form.get('year') is not None:
            print("Received POST method request(year filter) ")
            print("After I submit a year...")
            print(request.form.get('year'))
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)
            print("New Years List: ", years_list)
    else:
        print("No POST method (year filter) received")
        yearInput = ''

    return articleDashboardLogic(mysql, mysql2, years_list, yearInput)


@ app.route('/journalDashboard', methods=["GET", "POST"])
def journalDashboard():
    return journalDashboardLogic(mysql)


@ app.route('/authorDashboard', methods=["GET", "POST"])
def authorDashboard():

    years_list = []
    yearInput = ''
    print("This is the default year range.")
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)
    print(years_list)
    if request.method == "POST":
        print("Received POST method request ")
        if request.form.get('year') is not None:
            print(request.form.get('year'))
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)
            print("New Years List: ", years_list)
    else:
        yearInput = ''

    return authorDashboardLogic(mysql, mysql2, years_list, yearInput)


@ app.route('/about', methods=["GET", "POST"])
def about():
    return flask.render_template('about.html')


@ app.route('/team', methods=["GET", "POST"])
def team():
    return flask.render_template('team.html')


@ app.route('/licenses', methods=["GET", "POST"])
def licenses():
    return flask.render_template('licenses.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
