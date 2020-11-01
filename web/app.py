import flask
from flask_mysqldb import MySQL

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
app2.config['MYSQL_DB'] = 'crossrefeventdata'
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql2 = MySQL(app2)


@app.route('/')
def index():
    totalSum = landingPageStats(mysql)
    totalSumArticles = landingPageArticles(mysql)
    totalSumJournals = landingPageJournals(mysql)
    return flask.render_template('index.html', totalSum=totalSum , totalSumArticles=totalSumArticles , totalSumJournals=totalSumJournals)


@app.route('/searchResultsPage', methods=["GET", "POST"])
def search():
    cursor = mysql.connection.cursor()
    return searchLogic(mysql, cursor)

@app.route('/articleDashboard', methods=["GET", "POST"])
def articleDashboard():
    return articleDashboardLogic(mysql, mysql2)


@app.route('/journalDashboard', methods=["GET", "POST"])
def journalDashboard():
    return journalDashboardLogic(mysql)


@app.route('/authorDashboard', methods=["GET", "POST"])
def authorDashboard():
    return authorDashboardLogic(mysql, mysql2)


@app.route('/about', methods=["GET", "POST"])
def about():
    return flask.render_template('about.html')


@app.route('/team', methods=["GET", "POST"])
def team():
    return flask.render_template('team.html')


@app.route('/licenses', methods=["GET", "POST"])
def licenses():
    return flask.render_template('licenses.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
