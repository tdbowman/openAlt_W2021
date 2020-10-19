# pip install flask-mysqldb
import flask
from flask_mysqldb import MySQL
app = flask.Flask(__name__)

# Database connection settings
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app.config['MYSQL_DB'] = 'dr_bowman_doi_data_tables'
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
    row = "something not none"
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
                     {'year':2016, 'select': ''},
                     {'year':1997, 'select': ''}]# TBD bring unique years from main table
        else:
            years = [{'year':2020, 'select': ''},
                     {'year':2019, 'select': ''},
                     {'year':2018, 'select': ''},
                     {'year':2017, 'select': ''},
                     {'year':2016, 'select': ''},
                     {'year':1997, 'select': ''}]

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
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\';"
        else:
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\' and substr(published_print_date_parts, 1,4) in "+s_years+";"

        cursor.execute(sql)
        result_set = cursor.fetchall()

        for row in result_set:
            fk = row['fk']
            author_list = []
            if fk is not None:
                author_sql = "select name from author where fk = " + str(fk) + ";"
                cursor.execute(author_sql)
                author_list = cursor.fetchall()

            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['publisher'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop() # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE AUTHOR TABLE NOT FILLED IN
    elif (selection == "Author"):
        given_author= []
        given_author = '( '
        auth_sql = "SELECT fk, name FROM dr_bowman_doi_data_tables.author where name like'%" +search+"%';"
        cursor.execute(auth_sql)
        result_set = cursor.fetchall()
        for row in result_set:
            if row == result_set[-1]:
                given_author = given_author + str(row['fk'])
            else:
                given_author = given_author + str(row['fk']) + ","
        given_author = given_author + ')'

        print(given_author)

        if result_set is not None:
            if not selcted_years:
                sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where fk in " + given_author + ";"
            else:
                sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where fk in " + given_author + " and substr(published_print_date_parts, 1,4) in" + s_years + ";"

            print(sql)
            cursor.execute(sql)
            result_set = cursor.fetchall()

            for row in result_set:
                fk = row['fk']
                author_list = []
                if fk is not None:
                    author_sql = "select name from author where fk = " + str(fk) + ";"
                    cursor.execute(author_sql)
                    author_list = cursor.fetchall()

                article = {'objectID': row['doi'], 'articleTitle': row['title'],
                           'journalName': row['publisher'],
                           'articleDate': row['published_print_date_parts'],
                           'author_list': author_list}
                returnedQueries.append(article)

            returnedQueries.append(None)
            cursor.close()
            returnedQueries.pop()  # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE JOURNAL TABLE NOT FILLED IN
    elif (selection == "Journal"):
        if not selcted_years:
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where publisher like '%" + search + "%\';"
        else:
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where publisher like '%" + search + "%\' and substr(published_print_date_parts, 1,4) in" + s_years+";"

        cursor.execute(sql)
        result_set = cursor.fetchall()

        for row in result_set:
            fk = row['fk']
            author_list = []
            if fk is not None:
                author_sql = "select name from author where fk = " + str(fk) + ";"
                cursor.execute(author_sql)
                author_list = cursor.fetchall()

            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['publisher'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE ARTICLE TABLE NOT FILLED IN
    elif (selection == "Article"):
        if not selcted_years:
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where title like '%" + search + "%\';"
        else:
            sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where title like '%" + search + "%\' and substr(published_print_date_parts, 1,4) in" + s_years + ";"

        print(sql)
        cursor.execute(sql)
        result_set = cursor.fetchall()

        for row in result_set:
            fk = row['fk']
            author_list = []
            if fk is not None:
                author_sql = "select name from author where fk = " + str(fk) + ";"
                cursor.execute(author_sql)
                author_list = cursor.fetchall()

            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['publisher'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    return flask.render_template('searchResultsPage.html',
                                 listedSearchResults=returnedQueries,
                                 years=years,
                                 dropdownSearchBy=selection,
                                 search=search )

# Article Dashboard
@app.route('/articleDashboard', methods =["GET", "POST"])
def articleDashboard():

    global mysql
    cursor = mysql.connection.cursor()

    search = str(flask.request.args.get("DOI"))

    sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\';"

    cursor.execute(sql)
    mysql.connection.commit()
    article_result = cursor.fetchone()

    if article_result is not None:
        fk = article_result['fk']

        if fk is not None:
            author_sql = "select name from author where fk = " + str(fk) + ";"
            cursor.execute(author_sql)
            author_list = cursor.fetchall()

        article = {'objectID': article_result['doi'], 'articleTitle': article_result['title'],
                   'journalName': article_result['publisher'],
                   'articleDate': article_result['published_print_date_parts'],
                   'author_list': author_list}

    cursor.close()
    print(" ############", article)
    return flask.render_template('articleDashboard.html',
                                 article_detail=article)

# Journal Dashboard
@app.route('/journalDashboard', methods =["GET", "POST"])
def journalDashboard():
    journal_list = [] #list initializing
    x = "something not none"
    global mysql
    cursor = mysql.connection.cursor()

    journal_name = str(flask.request.args.get("journalName")) #fetch the query parameter journal name from searchREsults page
    sql = "Select doi, title, publisher, published_print_date_parts, fk from _main_ where publisher like '%" + journal_name + "%\';"

    cursor.execute(sql)
    result_set = cursor.fetchall()

    for row in result_set:
        fk = row['fk']
        author_list = []
        if fk is not None:
            author_sql = "select name from author where fk = " + str(fk) + ";"
            cursor.execute(author_sql)
            author_list = cursor.fetchall()

        article = {'objectID': row['doi'], 'articleTitle': row['title'],
                   'journalName': row['publisher'],
                   'articleDate': row['published_print_date_parts'],
                   'author_list': author_list}
        journal_list.append(article)

    return flask.render_template('journalDashboard.html',
                                 journal_name=journal_name,
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
    app.run(host='localhost', port=8057)