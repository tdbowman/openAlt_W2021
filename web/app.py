# pip install flask-mysqldb
import flask
from flask_mysqldb import MySQL
app = flask.Flask(__name__)

# Database connection settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'crossRefEventData'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql = MySQL(app)

@app.route('/')
def index():
    
    return flask.render_template('index.html')

@app.route('/searchResultsPage', methods =["GET", "POST"])
def homepageSearch():
    
    # Initialize variables - need to use global mysql variable
    global mysql
    cursor = mysql.connection.cursor()
    returnedQueries = []
    x = "something not none"

    # Get the parameters from 
    if flask.request.method == "POST":
        search = str(flask.request.form.get("search"))
        selection = str(flask.request.form.get("dropdownSearchBy"))
    
    # Search by DOI - WORKING
    if (selection == "DOI"):
        sql = "Select * from main where objectID like '%" + search + "%\';"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()
        returnedQueries.pop() # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE AUTHOR TABLE NOT FILLED IN
    elif (selection == "Author"):  
        sql = "Select * from redditevent where objectID like '%10.1370/afm.1885';"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()
        returnedQueries.pop() # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE JOURNAL TABLE NOT FILLED IN
    elif (selection == "Journal"):
        sql = "Select * from redditevent where objectID like '%10.1370/afm.1885';"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()
        returnedQueries.pop() # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE ARTICLE TABLE NOT FILLED IN
    elif (selection == "Article"):
        sql = "Select * from redditevent where objectID like '%10.1370/afm.1885';"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()  
        returnedQueries.pop() # the last list item is always null so pop it

    return flask.render_template('searchResultsPage.html', listedSearchResults=returnedQueries)

# Article Dashboard
@app.route('/articleDashboard', methods =["GET", "POST"])
def articleDashboard():

    
    return flask.render_template('articleDashboard.html')

# Journal Dashboard
@app.route('/journalDashboard', methods =["GET", "POST"])
def journalDashboard():


    return flask.render_template('journalDashboard.html')

# Author Dashboard
@app.route('/authorDashboard', methods =["GET", "POST"])
def authorDashboard():


    return flask.render_template('authorDashboard.html')

if __name__ == "__main__":
    app.run(debug=True)