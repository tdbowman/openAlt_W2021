# pip install flask-mysqldb
import flask
from flask_mysqldb import MySQL
app = flask.Flask(__name__)

# Database connection settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '11911842'
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
        selcted_years = flask.request.form.getlist("years")

        for year in range(0, len(selcted_years)):
            selcted_years[year] = int(selcted_years[year])

        if not selcted_years:
            years = [{'year':2020, 'select': ''},
                     {'year':2019, 'select': ''},
                     {'year':2018, 'select': ''},
                     {'year':2017, 'select': ''},
                     {'year':2016, 'select': ''}]# TBD bring unique years from main table
        else:
            years = [{'year':2020, 'select': ''},
                     {'year':2019, 'select': ''},
                     {'year':2018, 'select': ''},
                     {'year':2017, 'select': ''},
                     {'year':2016, 'select': ''}]

            for year in years:
                if year.get('year') in selcted_years:
                    year['select'] = 'checked'
    # form query string for year filter constraint in where clause
    s_years = '( '
    for year in selcted_years:
        if year == selcted_years[-1]:
            s_years = s_years + "'" + str(year) + "'"
        else:
            s_years = s_years + "'" + str(year) + "'" + ","
    s_years = s_years + ')'

    # Search by DOI - WORKING
    if (selection == "DOI"):
        if not selcted_years:
            sql = "Select * from main where objectID like '%" + search + "%\';"
        else:
            sql = "Select * from main where objectID like '%" + search + "%\' and year(articleDate) in "+s_years+";"

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
        if not selcted_years:
            sql = "Select * from main where journalName like '%" + search + "%\';"
        else:
            sql = "Select * from main where journalName like '%" + search + "%\' and year(articleDate) in "+s_years+";"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()
        returnedQueries.pop() # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE ARTICLE TABLE NOT FILLED IN
    elif (selection == "Article"):
        if not selcted_years:
            sql = "Select * from main where articleTitle like '%" + search + "%\';"
        else:
            sql = "Select * from main where articleTitle like '%" + search + "%\' and year(articleDate) in " + s_years + ";"
        cursor.execute(sql)
        mysql.connection.commit()
        while x is not None:
            x = cursor.fetchone()
            returnedQueries.append(x)
        cursor.close()  
        returnedQueries.pop() # the last list item is always null so pop it

    return flask.render_template('searchResultsPage.html',
                                 listedSearchResults=returnedQueries,
                                 years=years,
                                 dropdownSearchBy=selection,
                                 search=search )

# Article Dashboard
@app.route('/articleDashboard', methods =["GET", "POST"])
def articleDashboard():
    article_detail = []
    x = "something not none"
    global mysql
    cursor = mysql.connection.cursor()

    search = str(flask.request.args.get("DOI"))
    sql = "Select * from main where objectID like '%" + search + "%\';"

    cursor.execute(sql)
    mysql.connection.commit()
    article_detail=cursor.fetchone()
    cursor.close()

    return flask.render_template('articleDashboard.html',
                                 article_detail=article_detail)

# Journal Dashboard
@app.route('/journalDashboard', methods =["GET", "POST"])
def journalDashboard():
    journal_list = [] #list initializing
    x = "something not none"
    global mysql
    cursor = mysql.connection.cursor()

    journal_name = str(flask.request.args.get("journalName")) #fetch the query parameter journal name from searchREsults page
    sql = "Select * from main where journalName like '%" + journal_name + "%\';"

    cursor.execute(sql)
    mysql.connection.commit()

    #iterate SQL result set from cursor and move it into journal_list (python list)
    while x is not None:
        x = cursor.fetchone()
        journal_list.append(x)
    cursor.close()
    journal_list.pop()

    return flask.render_template('journalDashboard.html',
                                 journal_list=journal_list)

# Author Dashboard
@app.route('/authorDashboard', methods =["GET", "POST"])
def authorDashboard():


    return flask.render_template('authorDashboard.html')

@app.route('/about', methods =["GET", "POST"])
def about():
    
    return flask.render_template('about.html')

@app.route('/team', methods =["GET", "POST"])
def team():
    
    return flask.render_template('team.html')

@app.route('/licenses', methods =["GET", "POST"])
def licenses():
    
    return flask.render_template('licenses.html')

if __name__ == "__main__":
    app.run(debug=True)