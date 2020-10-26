import flask
import json
from datetime import datetime
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


# connect to cross ref database
app2 = flask.Flask(__name__)

# Database connection settings
app2.config['MYSQL_USER'] = 'root'
app2.config['MYSQL_PASSWORD'] = ''
# Or use the database.table which will allow us to join the databases - the one with author, and the one with events
app2.config['MYSQL_DB'] = 'crossrefeventdata'
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Database initialization and cursor
mysql2 = MySQL(app2)


@app.route('/')
def index():

    return flask.render_template('index.html')


@app.route('/searchResultsPage', methods=["GET", "POST"])
def homepageSearch():

    # Initialize variables - need to use global mysql variable
    global mysql
    cursor = mysql.connection.cursor()

    returnedQueries = []

    row = "something not none"
    # Get the parameters
    if flask.request.method == "POST":
        search = str(flask.request.form.get("search"))
        selection = str(flask.request.form.get("dropdownSearchBy"))
        selected_years = []
        try:
            # Mitch - used to for range form
            startYear = int(flask.request.form.get("startYear"))
            if startYear > datetime.now().year:
                pass  # If they enter a year greater than this year, just proceed to the except block AKA execute search with no year filter
            # Mitch - used for range form
            endYear = int(flask.request.form.get("endYear"))
            # Build up a list of selected years, ranging from startYear to endYear
            while (startYear < endYear + 1):
                selected_years.append(startYear)
                startYear += 1
        except:
            selected_years = []

    # This builds up the years to select from
    # If the user does not put anything, then this code set s_years to "( )" and all years are searched
    s_years = '( '
    for year in selected_years:
        if year == selected_years[-1]:
            s_years = s_years + "'" + str(year) + "'"
        else:
            s_years = s_years + "'" + str(year) + "'" + ","
    s_years = s_years + ')'

    # Search by DOI - WORKING
    if (selection == "DOI"):

        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\';"
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in " + \
                s_years+";"

        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the _main_ table result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            # append article dict to returnedQueries list
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE AUTHOR TABLE NOT FILLED IN
    elif (selection == "Author"):
        # get fk and name for searched author name
        given_author = []
        given_author = '( '
        auth_sql = "SELECT fk, name FROM dr_bowman_doi_data_tables.author where name like'%" + search+"%';"
        cursor.execute(auth_sql)
        result_set = cursor.fetchall()
        # form a list of fk for the where statement (ex.) ('2005','2006')
        for row in result_set:
            if row == result_set[-1]:
                given_author = given_author + str(row['fk'])
            else:
                given_author = given_author + str(row['fk']) + ","
        given_author = given_author + ')'

        print(given_author)

        # query _main_ table with list of fk gotten previously
        if result_set is not None:
            if not selected_years:
                # no year filter
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + given_author + ";"
            else:
                # with year filter
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
                    given_author + \
                    " and substr(published_print_date_parts, 1,4) in" + \
                    s_years + ";"

            print(sql)
            try:
                cursor.execute(sql)
                result_set = cursor.fetchall()
                # iterate the result set
                for row in result_set:
                    # get fk from _main_ table
                    fk = row['fk']
                    author_list = []
                    if fk is not None:
                        # look up author table by fk
                        author_sql = "select id, name from author where fk = " + \
                            str(fk) + ";"
                        cursor.execute(author_sql)
                        # get list of authors for given fk
                        author_list = cursor.fetchall()

                    # create dict with _main_ table row and author list
                    article = {'objectID': row['doi'], 'articleTitle': row['title'],
                               'journalName': row['container_title'],
                               'articleDate': row['published_print_date_parts'],
                               'author_list': author_list}
                    # append article dict to returnedQueries list
                    returnedQueries.append(article)

                returnedQueries.append(None)
                cursor.close()
                returnedQueries.pop()  # the last list item is always null so pop it
            except:
                pass

    # THIS DOES NOT WORK YET SINCE JOURNAL TABLE NOT FILLED IN
    elif (selection == "Journal"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + search + "%\';"
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years+";"

        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    # THIS DOES NOT WORK YET SINCE ARTICLE TABLE NOT FILLED IN
    elif (selection == "Article"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + search + "%\';"
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years + ";"

        print(sql)
        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    return flask.render_template('searchResultsPage.html',
                                 listedSearchResults=returnedQueries,
                                 dropdownSearchBy=selection,
                                 search=search)

# Article Dashboard


@app.route('/articleDashboard', methods=["GET", "POST"])
def articleDashboard():

    global mysql
    cursor = mysql.connection.cursor()

    global mysql2
    # connect to crossrefeventdata
    cursor2 = mysql2.connection.cursor()

    # get DOI parameter
    search = str(flask.request.args.get("DOI"))

    # query main table by DOI
    sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\';"

    cursor.execute(sql)
    mysql.connection.commit()
    article_result = cursor.fetchone()

    if article_result is not None:
        # get article fk
        fk = article_result['fk']

        # get list of authors for that fk
        if fk is not None:
            author_sql = "select name from author where fk = " + str(fk) + ";"
            cursor.execute(author_sql)
            author_list = cursor.fetchall()

        article = {'objectID': article_result['doi'], 'articleTitle': article_result['title'],
                   'journalName': article_result['container_title'],
                   'articleDate': article_result['published_print_date_parts'],
                   'author_list': author_list}

    cursor.close()
    # ---------- Article Events ----------

    # "UNION "
    # "UNION "
    # "UNION "
    # "UNION "
    # "UNION "
    # "UNION "
    # "UNION "
    # "UNION "
    # "WHERE substr(objectID,17) like '%" + \
    #     article['objectID'] + "%';"

    # May have to seperate the queries into different lists because only events from one platform are showing up in the event data. Next would be to append them together in one list.
    eventsForArticle = []
    twitterEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.twitterevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%' "

    # "UNION ALL " not working meaning it only displays columns for the first query but nothing else.
    wikipediaEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.wikipediaevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%';"

    hypothesisEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.hypothesisevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%';"

    newsfeedEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.newsfeedevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    redditEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.redditevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    redditLinksEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.redditlinksevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    stackexchangeEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.stackexchangeevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    webEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.webevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    wordpressEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdata.wordpressevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    cursor2.execute(twitterEventQuery)
    eventRows = cursor2.fetchall()

    # ---------- Twitter Events -------------
    for tweet in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each twitter event's subjectID and objectID
        subjID = tweet['subjectID']
        objID = tweet['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': tweet['subjectID'],
                             'sourceID': tweet['sourceID'],
                             'relationType': tweet['relationType'], 'objectID': tweet['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(wikipediaEventQuery)
    eventRows = cursor2.fetchall()

    # ----------- Wikipedia Events -----------
    for wiki in eventRows:
        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each wikipedia event's subjectID and objectID
        subjID = wiki['subjectID']
        objID = wiki['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:
                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': wiki['subjectID'],
                             'sourceID': wiki['sourceID'],
                             'relationType': wiki['relationType'],
                             'objectID': wiki['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(hypothesisEventQuery)
    eventRows = cursor2.fetchall()

    # ------------ Hypothesis Events -------------
    for hypo in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each hypothesis event's subjectID and objectID
        subjID = hypo['subjectID']
        objID = hypo['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': hypo['subjectID'],
                             'sourceID': hypo['sourceID'],
                             'relationType': hypo['relationType'], 'objectID': hypo['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(newsfeedEventQuery)
    eventRows = cursor2.fetchall()

    # ------------ Newsfeed Events ---------------
    for news in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each newsfeed event's subjectID and objectID
        subjID = news['subjectID']
        objID = news['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': news['subjectID'],
                             'sourceID': news['sourceID'],
                             'relationType': news['relationType'], 'objectID': news['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(redditEventQuery)
    eventRows = cursor2.fetchall()
    # ------------ Reddit Events -----------------

    for red in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each reddit event's subjectID and objectID
        subjID = red['subjectID']
        objID = red['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': red['subjectID'],
                             'sourceID': red['sourceID'],
                             'relationType': red['relationType'], 'objectID': red['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(redditLinksEventQuery)
    eventRows = cursor2.fetchall()

    # ------------ Redditlinks Events -----------
    for redl in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each redditlink event's subjectID and objectID
        subjID = redl['subjectID']
        objID = redl['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': redl['subjectID'],
                             'sourceID': redl['sourceID'],
                             'relationType': redl['relationType'], 'objectID': redl['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(stackexchangeEventQuery)
    eventRows = cursor2.fetchall()
    # ------------ Stackexchange Events ----------
    for stack in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each stackexchange event's subjectID and objectID
        subjID = stack['subjectID']
        objID = stack['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': stack['subjectID'],
                             'sourceID': stack['sourceID'],
                             'relationType': stack['relationType'], 'objectID': stack['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(webEventQuery)
    eventRows = cursor2.fetchall()

    # ------------ Web Events -------------------
    for web in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each web event's subjectID and objectID
        subjID = web['subjectID']
        objID = web['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': web['subjectID'],
                             'sourceID': web['sourceID'],
                             'relationType': web['relationType'], 'objectID': web['objectID']}
                eventsForArticle.append(eachEvent)

    cursor2.execute(wordpressEventQuery)
    eventRows = cursor2.fetchall()

    # ------------ Wordpress Events -------------
    for word in eventRows:

        # Shouldn't have to check if the objectID in each row is the same as the articleURL but the query kept retrieving all events.
        # The 9 queries that were brought together using unions worked in workbench but not here for some unkown reason for now.
        # UPDATE: the substring() isn't working as it retrieves the whole objectID rather than part of it. objID[16:length] is the workaround for substr().

        # grab each wordpress event's subjectID and objectID
        subjID = word['subjectID']
        objID = word['objectID']
        length = len(objID)

        # Had to slice the objectID and start at the 16th index and compare the rest of the slice with the selected article's URL
        if objID[16:length] == article['objectID']:
            if subjID is not None:

                # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                eachEvent = {'subjectID': word['subjectID'],
                             'sourceID': word['sourceID'],
                             'relationType': word['relationType'], 'objectID': word['objectID']}
                eventsForArticle.append(eachEvent)

    # ---------- End of Article Events ---------
    # Size of each list depends on how many years(in chartScript.js) you'd like to display.
    # Queries will be inserted within the array
    years_list = [2016, 2017, 2018, 2019, 2020]

    # cambia event
    cambiaEvent = []
    for year in years_list:
        cambia_sql = "select count(*) count from crossrefeventdata.cambiaevent " \
                     "where substr(objectID,17)='"+article_result['doi']+"' " \
                     "and substr(occurredAt,1,4)='"+str(year)+"';"

        cursor2.execute(cambia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        cambiaEvent.append(event_count['count'])
    print('cambiaEvent ~~~~~~~~~', cambiaEvent)
    # cambiaEvent = [30, 20, 50, 10, 90]  # TBD - delete this line after we upload data in cambia event table for all these years

    # crossrefevent
    crossrefevent = []
    for year in years_list:
        crossref_sql = "select count(*) count from crossrefeventdata.crossrefevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(crossref_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        crossrefevent.append(event_count['count'])
    print(' crossrefevent ~~~~~~~~~~~', crossrefevent)
    # crossrefevent = [5, 7, 14, 18, 25]; # TBD - delete this line after we upload data in cambia event table for all these years

    # dataciteevent
    dataciteevent = []
    for year in years_list:
        datacite_sql = "select count(*) count from crossrefeventdata.dataciteevent " \
                       "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(datacite_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        dataciteevent.append(event_count['count'])
    print(' dataciteevent ~~~~~~~~~~~', dataciteevent)
    # dataciteevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # hypothesisevent
    hypothesisevent = []
    for year in years_list:
        hypothesis_sql = "select count(*) count from crossrefeventdata.hypothesisevent " \
                         "where substr(objectID,17)='" + article_result['doi'] + "' " \
                         "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(hypothesis_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        hypothesisevent.append(event_count['count'])
    print(' hypothesisevent ~~~~~~~~~~~', hypothesisevent)
    # hypothesisevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # newsfeedevent
    newsfeedevent = []
    for year in years_list:
        newsfeed_sql = "select count(*) count from crossrefeventdata.newsfeedevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(newsfeed_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        newsfeedevent.append(event_count['count'])
    print(' newsfeedevent ~~~~~~~~~~~', newsfeedevent)
    # newsfeedevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditevent
    redditevent = []
    for year in years_list:
        reddit_sql = "select count(*) count from crossrefeventdata.redditevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(reddit_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditevent.append(event_count['count'])
    print(' redditevent ~~~~~~~~~~~', redditevent)
    # redditevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditlinksevent
    redditlinksevent = []
    for year in years_list:
        redditlinks_sql = "select count(*) count from crossrefeventdata.redditlinksevent " \
                          "where substr(objectID,17)='" + article_result['doi'] + "' " \
                          "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(redditlinks_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditlinksevent.append(event_count['count'])
    print(' redditlinksevent ~~~~~~~~~~~', redditlinksevent)
    # redditlinksevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # stackexchangeevent
    stackexchangeevent = []
    for year in years_list:
        stackexchange_sql = "select count(*) count from crossrefeventdata.stackexchangeevent " \
                            "where substr(objectID,17)='" + article_result['doi'] + "' " \
                            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(stackexchange_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        stackexchangeevent.append(event_count['count'])
    print(' stackexchangeevent ~~~~~~~~~~~', stackexchangeevent)
    # stackexchangeevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # twitterevent
    twitterevent = []
    for year in years_list:
        twitter_sql = "select count(*) count from crossrefeventdata.twitterevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(twitter_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        twitterevent.append(event_count['count'])
    print(' twitterevent ~~~~~~~~~~~', twitterevent)
    # twitterevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # webevent
    webevent = []
    for year in years_list:
        web_sql = "select count(*) count from crossrefeventdata.webevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(web_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        webevent.append(event_count['count'])
    print(' webevent ~~~~~~~~~~~', webevent)
    # webevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wikipediaevent
    wikipediaevent = []
    for year in years_list:
        wikipedia_sql = "select count(*) count from crossrefeventdata.wikipediaevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wikipedia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wikipediaevent.append(event_count['count'])
    print(' wikipediaevent ~~~~~~~~~~~', wikipediaevent)
    # wikipediaevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wordpressevent
    wordpressevent = []
    for year in years_list:
        wordpress_sql = "select count(*) count from crossrefeventdata.wordpressevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wordpress_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wordpressevent.append(event_count['count'])
    print(' wordpressevent ~~~~~~~~~~~', wordpressevent)
    # wordpressevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    return flask.render_template('articleDashboard.html', article_detail=article, events=eventsForArticle,
                                 cambiaEventData=cambiaEvent,
                                 crossrefEventData=crossrefevent,
                                 dataciteEventData=dataciteevent,
                                 hypothesisEventData=hypothesisevent,
                                 newsfeedEventData=newsfeedevent,
                                 redditEventData=redditevent,
                                 redditlinksEventData=redditlinksevent,
                                 stackexchangeEventData=stackexchangeevent,
                                 twitterEventData=twitterevent,
                                 webEventData=webevent,
                                 wikipediaEventData=wikipediaevent,
                                 wordpressEventData=wordpressevent)

# Journal Dashboard


@app.route('/journalDashboard', methods=["GET", "POST"])
def journalDashboard():
    journal_list = []  # list initializing

    global mysql
    cursor = mysql.connection.cursor()

    # fetch the journal name parameter from searchResults page
    journal_name = str(flask.request.args.get("journalName"))
    sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + journal_name + "%\';"

    cursor.execute(sql)
    result_set = cursor.fetchall()

    # iterate the result set
    for row in result_set:
        # get fk from _main_ table
        fk = row['fk']
        author_list = []
        if fk is not None:
            # look up author table by fk
            author_sql = "select name from author where fk = " + str(fk) + ";"
            cursor.execute(author_sql)
            # get list of authors for given fk
            author_list = cursor.fetchall()

        # create dict with _main_ table row and author list
        article = {'objectID': row['doi'], 'articleTitle': row['title'],
                   'journalName': row['container_title'],
                   'articleDate': row['published_print_date_parts'],
                   'author_list': author_list}
        journal_list.append(article)

    start_year = 1995
    end_year = 2020
    publishedPerYear = []
    while (start_year <= end_year):
        articles_per_year_sql = "select count(*) count " \
                                "from dr_bowman_doi_data_tables._main_ " \
                                "where container_title like '%" + journal_name + "%' " \
                                "and substr(published_print_date_parts,1,4)='" + str(
                                    start_year) + "' ;"
        cursor.execute(articles_per_year_sql)
        yr_count = cursor.fetchone()
        publishedPerYear.append(yr_count["count"])
        start_year = start_year + 1
    print("publishedPerYear ---- ", publishedPerYear)
    return flask.render_template('journalDashboard.html',
                                 journal_name=journal_name,
                                 journal_list=journal_list,
                                 publishedPerYear=publishedPerYear
                                 )

# Author Dashboard


@app.route('/authorDashboard', methods=["GET", "POST"])
def authorDashboard():
    author_article_list = []
    author_doi_list = []
    global mysql
    cursor = mysql.connection.cursor()

    global mysql2
    # connect to crossrefeventdata
    cursor2 = mysql2.connection.cursor()

    # fetch the query parameter author_id from searchResults page
    author_id = str(flask.request.args.get("author_id"))
    print('author_id', author_id)

    author_sql = "SELECT name FROM dr_bowman_doi_data_tables.author where id ="+author_id+";"
    cursor.execute(author_sql)
    author_name = cursor.fetchone()
    print('author_name -----<<<: ', author_name['name'])

    author_sql = "SELECT fk FROM dr_bowman_doi_data_tables.author where name = '" + \
        author_name['name'] + "';"
    cursor.execute(author_sql)
    author_resultset = cursor.fetchall()
    print('###################', author_resultset)
    # form a list of fk for the where statement (ex.) ('2005','2006')
    author_fk_list = '('
    for row in author_resultset:
        # author_name=row['name']
        if row == author_resultset[-1]:
            author_fk_list = author_fk_list + str(row['fk'])
        else:
            author_fk_list = author_fk_list + str(row['fk']) + ","
    author_fk_list = author_fk_list + ')'

    #author_name = author_resultset['name']
    #author_fk = author_resultset['fk']
    if author_fk_list is not None:
        # look up author table by fk
        sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
            author_fk_list + ";"
        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            author_article_list.append(article)
            author_doi_list.append(row['doi'])
        cursor.close()

        print('author_article_list --------------->>>> :', author_article_list)

    # Size of each list depends on how many years(in chartScript.js) you'd like to display.
    # Queries will be inserted within the array
    years_list = [2016, 2017, 2018, 2019, 2020]

    # form a list of just the DOIs
    doi_list = '( '
    for doi in author_doi_list:
        if doi == author_doi_list[-1]:
            doi_list = doi_list + "'" + str(doi) + "'"
        else:
            doi_list = doi_list + "'" + str(doi) + "'" + ","
    doi_list = doi_list + ')'

    print(' Author DOI list : ', doi_list)
    # cambia event
    cambiaEvent = []
    for year in years_list:
        cambia_sql = "select count(*) count from crossrefeventdata.cambiaevent " \
                     "where substr(objectID,17) in " + doi_list + " " \
                     "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(cambia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        cambiaEvent.append(event_count['count'])
    print('cambiaEvent ~~~~~~~~~', cambiaEvent)
    # cambiaEvent = [30, 20, 50, 10, 90]  # TBD - delete this line after we upload data in cambia event table for all these years

    # crossrefevent
    crossrefevent = []
    for year in years_list:
        crossref_sql = "select count(*) count from crossrefeventdata.crossrefevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(crossref_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        crossrefevent.append(event_count['count'])
    print(' crossrefevent ~~~~~~~~~~~', crossrefevent)
    # crossrefevent = [5, 7, 14, 18, 25]; # TBD - delete this line after we upload data in cambia event table for all these years

    # dataciteevent
    dataciteevent = []
    for year in years_list:
        datacite_sql = "select count(*) count from crossrefeventdata.dataciteevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(datacite_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        dataciteevent.append(event_count['count'])
    print(' dataciteevent ~~~~~~~~~~~', dataciteevent)
    # dataciteevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # hypothesisevent
    hypothesisevent = []
    for year in years_list:
        hypothesis_sql = "select count(*) count from crossrefeventdata.hypothesisevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(hypothesis_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        hypothesisevent.append(event_count['count'])
    print(' hypothesisevent ~~~~~~~~~~~', hypothesisevent)
    # hypothesisevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # newsfeedevent
    newsfeedevent = []
    for year in years_list:
        newsfeed_sql = "select count(*) count from crossrefeventdata.newsfeedevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(newsfeed_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        newsfeedevent.append(event_count['count'])
    print(' newsfeedevent ~~~~~~~~~~~', newsfeedevent)
    # newsfeedevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditevent
    redditevent = []
    for year in years_list:
        reddit_sql = "select count(*) count from crossrefeventdata.redditevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(reddit_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditevent.append(event_count['count'])
    print(' redditevent ~~~~~~~~~~~', redditevent)
    # redditevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditlinksevent
    redditlinksevent = []
    for year in years_list:
        redditlinks_sql = "select count(*) count from crossrefeventdata.redditlinksevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(redditlinks_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditlinksevent.append(event_count['count'])
    print(' redditlinksevent ~~~~~~~~~~~', redditlinksevent)
    # redditlinksevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # stackexchangeevent
    stackexchangeevent = []
    for year in years_list:
        stackexchange_sql = "select count(*) count from crossrefeventdata.stackexchangeevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(stackexchange_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        stackexchangeevent.append(event_count['count'])
    print(' stackexchangeevent ~~~~~~~~~~~', stackexchangeevent)
    # stackexchangeevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # twitterevent
    twitterevent = []
    for year in years_list:
        twitter_sql = "select count(*) count from crossrefeventdata.twitterevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(twitter_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        twitterevent.append(event_count['count'])
    print(' twitterevent ~~~~~~~~~~~', twitterevent)
    # twitterevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # webevent
    webevent = []
    for year in years_list:
        web_sql = "select count(*) count from crossrefeventdata.webevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(web_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        webevent.append(event_count['count'])
    print(' webevent ~~~~~~~~~~~', webevent)
    # webevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wikipediaevent
    wikipediaevent = []
    for year in years_list:
        wikipedia_sql = "select count(*) count from crossrefeventdata.wikipediaevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wikipedia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wikipediaevent.append(event_count['count'])
    print(' wikipediaevent ~~~~~~~~~~~', wikipediaevent)
    # wikipediaevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wordpressevent
    wordpressevent = []
    for year in years_list:
        wordpress_sql = "select count(*) count from crossrefeventdata.wordpressevent " \
                        "where substr(objectID,17) in " + doi_list + " " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wordpress_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wordpressevent.append(event_count['count'])
    print(' wordpressevent ~~~~~~~~~~~', wordpressevent)
    # wordpressevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    return flask.render_template('authorDashboard.html',
                                 author_name=author_name['name'],
                                 author_article_list=author_article_list,
                                 cambiaEventData=cambiaEvent,
                                 crossrefEventData=crossrefevent,
                                 dataciteEventData=dataciteevent,
                                 hypothesisEventData=hypothesisevent,
                                 newsfeedEventData=newsfeedevent,
                                 redditEventData=redditevent,
                                 redditlinksEventData=redditlinksevent,
                                 stackexchangeEventData=stackexchangeevent,
                                 twitterEventData=twitterevent,
                                 webEventData=webevent,
                                 wikipediaEventData=wikipediaevent,
                                 wordpressEventData=wordpressevent)


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
