import os
import flask
from flask import Flask
from flask import send_file
from flask_mysqldb import MySQL
from flask import request, jsonify, redirect
from datetime import datetime

# Import our functions for other pages
from searchLogic import searchLogic
from articleDashboardLogic import articleDashboardLogic
from journalDashboardLogic import journalDashboardLogic
from authorDashboardLogic import authorDashboardLogic
from landingPageStats import landingPageStats
from landingPageArticles import landingPageArticles
from landingPageJournals import landingPageJournals
from uploadDOI import searchByDOI, getZipEvents
from uploadAuthor import searchByAuthor, getZipAuthor

from getPassword import getPassword

# get the users password from crossrefeventdata/web/passwd.txt
mysql_username = 'root'
mysql_password = getPassword()

# Instantiate an object of class Flask
app = flask.Flask(__name__)
# Database connection settings
app.config['MYSQL_USER'] = mysql_username
app.config['MYSQL_PASSWORD'] = mysql_password
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'doidata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Database initialization and cursor
mysql = MySQL(app)

# Instantiate a second object of class Flask
app2 = flask.Flask(__name__)
# Database connection settings
app2.config['MYSQL_USER'] = mysql_username
app2.config['MYSQL_PASSWORD'] = mysql_password

# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app2.config['MYSQL_DB'] = 'crossrefeventdatamain'
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql2 = MySQL(app2)


@app.route('/')
def index():
    # Go to landingPageStats.py
    totalSum = landingPageStats(mysql)

    # Go to landingPageArticles.py
    totalSumArticles = landingPageArticles(mysql)

    # Go to landingPageJournals.py
    totalSumJournals = landingPageJournals(mysql)

    return flask.render_template('index.html', totalSum=totalSum, totalSumArticles=totalSumArticles, totalSumJournals=totalSumJournals)


@app.route('/searchResultsPage', methods=["GET", "POST"])
def search():

    # If a HTTPS POST Request is received...
    if(request.method == "POST"):
        dropdownValue = request.form.get('dropdownSearchBy')
    else:
        dropdownValue = str(flask.request.args.get("dropdownSearchBy"))

    # Go to searchLogic.py
    return searchLogic(mysql, mysql2, dropdownValue)


@app.route('/articleDashboard', methods=["GET", "POST"])
def articleDashboard():

    # Initialize years_list and yearInput.
    years_list = []
    yearInput = ''

    # Based on the current year, initialize the years_list list year range(5 years).
    # This is the default year range.
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)

    # If a HTTPS POST Request is received...
    if request.method == "POST":
        # Grab the year value from the year filter of the bar chart.
        if request.form.get('year') is not None:
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)

    # Go to articleDashboardLogic.py
    return articleDashboardLogic(mysql, mysql2, years_list, yearInput)


@ app.route('/journalDashboard', methods=["GET", "POST"])
def journalDashboard():

    # Get the current year so we can pass it to the graph X axis
    # The earliest year we consider is 1997
    years_list = []
    currentYear = datetime.now().year
    for i in range(1997, currentYear + 1):
        years_list.append(i)

    # Go to journalDashboardLogic.py
    return journalDashboardLogic(mysql, years_list)


@ app.route('/authorDashboard', methods=["GET", "POST"])
def authorDashboard():

    # Initialize years_list and yearInput.
    years_list = []
    yearInput = ''

    # Based on the current year, initialize the years_list list year range(5 years).
    # This is the default year range.
    currentYear = datetime.now().year
    for i in range(currentYear - 4, currentYear + 1):
        years_list.append(i)

    # If a HTTPS POST Request is received...
    if request.method == "POST":
        # Grab the year value from the year filter of the bar chart.
        if request.form.get('year') is not None:
            yearInput = request.form.get('year')
            yearInput = int(yearInput)
            years_list = []
            for i in range(yearInput - 2, yearInput + 3):
                years_list.append(i)

    # Go to authorDashboardLogic.py
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

@ app.route('/upload', methods=["GET", "POST"])
def upload():

    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    target = app.config["UPLOAD_FILES"]

    if not os.path.isdir(target):
        os.mkdir(target)

    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # target = os.path.join(APP_ROOT, 'uploadFiles')
    # print(target)

    # if not os.path.isdir(target):
    #     os.mkdir(target)
    destination = app.config["UPLOAD_FILES"]

    if request.method=="POST":
        if request.files:
            uploadFiles = request.files["csv/json"]
            print(uploadFiles)

            fileName = uploadFiles.filename
            uploadFiles.save(os.path.join(destination, fileName))
            print("File saved.")

            #downloadfile(fileName)
            # return flask.render_template('download.html')
        
        return searchByDOI(mysql, fileName)

    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # target = os.path.join(APP_ROOT, 'uploadFiles')
    # print(target)

    # if not os.path.isdir(target):
    #     os.mkdir(target)

    # for file in request.files.getlist("file"):
    #     filename = file.filename
    #     destination = "/".join([target, filename])
    #     print(destination)
    #     file.save(destination)

    return flask.render_template('upload.html')

@ app.route('/uploadAuthors', methods=["GET", "POST"])
def uploadAuthors():

    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method=="POST":
        if request.files:
            uploadFiles = request.files["csv/json"]
            print(uploadFiles)

            fileName = uploadFiles.filename
            uploadFiles.save(os.path.join(destination, fileName))
            print("File saved.")
        
        return searchByAuthor(mysql, fileName)

    return flask.render_template('uploadAuthors.html')

@ app.route('/uploadUni', methods=["GET", "POST"])
def uploadUni():

    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

    if not os.path.isdir(destination):
        os.mkdir(destination)

    if request.method=="POST":
        if request.files:
            uploadFiles = request.files["csv/json"]
            print(uploadFiles)

            fileName = uploadFiles.filename
            uploadFiles.save(os.path.join(destination, fileName))
            print("File saved.")
        
        return searchByAuthor(mysql, fileName) ## return searchByUni()

    return flask.render_template('uploadUni.html')



@ app.route('/download', methods=["GET", "POST"])
def download():
    if request.method=="POST":
                
        test = getZipEvents()
        print("ZIP EVENTS:", test)
        return send_file(test, as_attachment=True)
    return flask.render_template('download.html')


@ app.route('/downloadAuthors', methods=["GET", "POST"])
def downloadAuthors():
    if request.method=="POST":
        
        print("ZIP AUTHOR:",getZipAuthor())
        return send_file(getZipAuthor(), as_attachment=True)
    return flask.render_template('downloadAuthors.html')

@ app.route('/downloadUni', methods=["GET", "POST"])
def downloadUni():
    if request.method=="POST":
        
        print("ZIP University:","getZipUni()")
        #return send_file(getZipAuthor(), as_attachment=True)
    return flask.render_template('downloadUni.html')

# @ app.route('/downloadAuthorZip', methods=["GET", "POST"])
# def downloadAuthorZip():
#     dir_file = str(os.path.dirname(os.path.realpath(__file__)))
#     dir_results = dir_file + '\\Results\\uploadAuthor_results.csv'
#     return send_file(dir_results, as_attachment=True)


@ app.route('/searchByOptions', methods=["GET", "POST"])
def searchByOptions():
    
    if request.method=="POST":
        select = request.form.get("uploadList")

        if select == "DOI":
            return redirect('/upload')
        elif select == "Author":
            return redirect('/uploadAuthors')
        elif select == "University":
            return redirect('/uploadUni')
    
    return flask.render_template('searchByOptions.html')
        
# If this is the main module or main program being run (app.py)......
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
