import os
import flask
from flask import Flask
from flask import send_file
from flask_mysqldb import MySQL
from flask import request, jsonify, redirect, flash
from datetime import datetime

# Import our functions for other pages
from searchLogic import searchLogic
from articleDashboardLogic import articleDashboardLogic
from journalDashboardLogic import journalDashboardLogic
from authorDashboardLogic import authorDashboardLogic
from landingPageStats import landingPageStats
from landingPageArticles import landingPageArticles
from landingPageJournals import landingPageJournals
from uploadDOI import searchByDOI
from uploadAuthor import searchByAuthor

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
app.config['MYSQL_DB'] = 'dr_bowman_doi_data_tables'
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

# Salsabil's code from line 162-288
# Beginning of Salsabil's Code

@ app.route('/upload', methods=["GET", "POST"])
def upload():

    # Directory of where to put the uploaded file
    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    target = app.config["UPLOAD_FILES"]

    # Allowed extensions of file
    ALLOWED_EXTENSIONS = {'csv'}

    # Limit of the file size to 1 GB
    # app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

    # If directory does not exist, create it
    if not os.path.isdir(target):
        os.mkdir(target)

    # If a HTTPS POST Request is received...
    if request.method=="POST":

        # If file is received...
        if request.files:

            # Retrieve the uploaded file 
            uploadFiles = request.files["csv/json"]
            fileName = uploadFiles.filename

            # Check extension of file
            fileExtension = fileName.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


            # Check file submission
            if uploadFiles and fileExtension:

                # Save the file to the directory
                uploadFiles.save(os.path.join(target, fileName))

                # Send the file to uploadDOI.py
                return searchByDOI(mysql, fileName)

            else:
                app.logger.error('Wrong file type uploaded.')
                # flash('No file part')
                return flask.render_template('validateDOI.html')


    return flask.render_template('upload.html')

@ app.route('/uploadAuthors', methods=["GET", "POST"])
def uploadAuthors():

     # Directory of where to put the uploaded file
    app.config["UPLOAD_FILES"] = "../web/uploadFiles"
    destination = app.config["UPLOAD_FILES"]

     # Allowed extensions of file
    ALLOWED_EXTENSIONS = {'csv'}

    # If directory does not exist, create it
    if not os.path.isdir(destination):
        os.mkdir(destination)

    # If a HTTPS POST Request is received...
    if request.method=="POST":

        # # If file is received...
        # if request.files:

        #     # Retrieve the uploaded file 
        #     uploadFiles = request.files["csv/json"]
        #     fileName = uploadFiles.filename

        #     # Check extension of file
        #     fileExtension = fileName.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
            
        #     if uploadFiles and fileExtension:
        #         uploadFiles.save(os.path.join(destination, fileName) 
        #         return searchByAuthor(mysql, fileName)

        #     else:
        #         app.logger.error('Wrong file type uploaded.')
        #         # flash('No file part')
        #         return flask.render_template('validateAuthor.html')

        # If file is received...
        if request.files:

            # Retrieve the uploaded file 
            uploadFiles = request.files["csv/json"]
            fileName = uploadFiles.filename

            # Check extension of file
            fileExtension = fileName.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


            # Check file submission
            if uploadFiles and fileExtension:

                # Save the file to the directory
                uploadFiles.save(os.path.join(destination, fileName))

                # Send the file to uploadDOI.py
                return searchByAuthor(mysql, fileName)

            else:
                app.logger.error('Wrong file type uploaded.')
                # flash('No file part')
                return flask.render_template('validateAuthor.html')

    return flask.render_template('uploadAuthors.html')

@ app.route('/download', methods=["GET", "POST"])
def download():

    # If a HTTPS POST Request is received...
    if request.method=="POST":

        # Directory of results zipped folder
        dir_file = str(os.path.dirname(os.path.realpath(__file__)))
        dir_results = dir_file + '\\Results\\uploadDOI_Results.zip'

        # Download folder onto local machine
        return send_file(dir_results, as_attachment=True)
    
    return flask.render_template('download.html')

@ app.route('/downloadAuthors', methods=["GET", "POST"])
def downloadAuthors():

    # If a HTTPS POST Request is received...
    if request.method=="POST":

        # Directory of results zipped folder
        dir_file = str(os.path.dirname(os.path.realpath(__file__)))
        dir_results = dir_file + '\\Results\\uploadAuthor_Results.zip'

        # Download folder onto local machine
        return send_file(dir_results, as_attachment=True)

    return flask.render_template('downloadAuthors.html')

@ app.route('/searchByOptions', methods=["GET", "POST"])
def searchByOptions():
    
    # If a HTTPS POST Request is received...
    if request.method=="POST":

        # Retrieve selection from form
        select = request.form.get("uploadList")

        # If selection is DOI, send to upload.html
        if select == "DOI":
            return redirect('/upload')

        # If selection is Author (only other option), send to uploadAuthors.html
        else:
            return redirect('/uploadAuthors')
    
    return flask.render_template('searchByOptions.html')

@ app.errorhandler(413)
def too_large(e):
    return "File is too large!", 413

# End of Salsabil's Code


# @ app.route('/upload_file_validation', methods=['POST'])
# def upload_file_validation():
#     options = {
#         'validation': {
#             'allowedExts': ['csv']
#         }
#     }

#     try:
#         response = File.upload(FlaskAdapter(request), '/public/', options)
    
#     except Exception: 
#         response = {'error': str(sys.exc_info()[1])}
        
#     return json.dumps(response)
        
# If this is the main module or main program being run (app.py)......
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
