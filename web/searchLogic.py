import flask
from flask import Flask, session
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter

def searchLogic(mysql, mysql2):

    # Declare variables here for readability
    cursor = mysql.connection.cursor()
    #cursor3 = mysql2.connection.cursor()
    #cursor4 = mysql2.connection.cursor()
    #cursor5 = mysql2.connection.cursor()
    #cursor6 = mysql2.connection.cursor()

    row = "something not none"
    pagination = None
    s_years = None
    startYear = None
    endYear = None
    sortSelector = None
    returnedQueries = []
    selected_years = []
    descending_or_ascending = " desc;" # sort by descending by default, change to asc if user wants

    # Get page number if it exists. If not, set to 1
    try:
        page = flask.request.args.get(get_page_parameter(), type=int, default=1)
    except ValueError:
        page = 1

    # get search and dropdownSearchBy parameters from GET request if form data is None
    # This occurs when you click on a page number, since the hidden form is not repopulated
    search = str(flask.request.form.get("search"))
    selection = str(flask.request.form.get("dropdownSearchBy"))
    startYear = flask.request.form.get("startYear")
    endYear = flask.request.form.get("endYear")
    sortSelector = flask.request.form.get('sortSelector')
    
    #print("Selection from hidden form is:", selection)
    #print("Search from hidden form is:", search)
    #print("startYear from hidden form is:", startYear)
    #print("endYear from hidden form is:", endYear)
    
    if flask.request.form.get("search") is None:
        search = str(flask.request.args.get("search"))
    if flask.request.form.get("dropdownSearchBy") is None:
        selection = str(flask.request.args.get("dropdownSearchBy"))
    if flask.request.form.get("startYear") is None:
        startYear = str(flask.request.args.get("startYear"))
    if flask.request.form.get("endYear") is None:
        endYear = str(flask.request.args.get("endYear"))
    if flask.request.form.get("sortSelector") is None:
        sortSelector = str(flask.request.args.get("sortSelector"))

    # Now that we have checked the form and URL for how the user would like to search, we can set it
    if (sortSelector == "PublicationYearAscending"):
        descending_or_ascending = " asc;"
    else:
        descending_or_ascending = " desc;" # redundant but having this here is clearer

    # Grab the years from the year form if they exist
    # Store these in selected_years list. This is related to the s_years string, but used in different ways
    try:
        # used in the year range form
        startYear = int(startYear)
        endYear = int(endYear)
        temp_year = startYear # We want to keep startYear unchanged from users input
        if temp_year > datetime.now().year:
            pass  # If user enters a year greater than this year, just proceed to the except block AKA execute search with no year filter
        
        # Build up a list of selected years, ranging from startYear to endYear
        while (temp_year < endYear + 1):
            selected_years.append(temp_year)
            temp_year += 1
        print(selected_years[0])
        print(selected_years[1])
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

########################################################################
#
#   Select which SQL to execute, based on the drop-down selection,
#   the search term, and the years selected, if any
#
########################################################################

    # Search by DOI - WORKING
    if (selection == "DOI"):

        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\' order by published_print_date_parts" + descending_or_ascending
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in " + \
                s_years + " order by published_print_date_parts" + descending_or_ascending

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

            #TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID like '%" + \
            #row['doi'] + "%';"
            #cursor6.execute(TotalEventsQuerySum)

            #totalEventsSum = cursor6.fetchone()

            #if totalEventsSum is None:
            #    totalEventsSum = 0
            #else:
              #  totalEventsSum = totalEventsSum['sumCount']
            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
                       #'totalEventsSum':totalEventsSum}
            # append article dict to returnedQueries list
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

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

        # query _main_ table with list of fk gotten previously
        if result_set is not None:
            if not selected_years:
                # no year filter
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + given_author + " order by published_print_date_parts" + descending_or_ascending
            else:
                # with year filter
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
                    given_author + \
                    " and substr(published_print_date_parts, 1,4) in" + \
                    s_years + " order by published_print_date_parts" + descending_or_ascending

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
                    
                    #TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID like '%" + \
                    #row['doi'] + "%';"
                    #cursor5.execute(TotalEventsQuerySum)

                    #totalEventsSum = cursor5.fetchone()

                    #if totalEventsSum is None:
                    #    totalEventsSum = 0
                    #else:
                    #      totalEventsSum = totalEventsSum['sumCount']

                    # create dict with _main_ table row and author list
                    article = {'objectID': row['doi'], 'articleTitle': row['title'],
                               'journalName': row['container_title'],
                               'articleDate': row['published_print_date_parts'],
                               'author_list': author_list}
                               #'totalEventsSum':totalEventsSum}
                    # append article dict to returnedQueries list
                    returnedQueries.append(article)

                returnedQueries.append(None)
                cursor.close()
                returnedQueries.pop()  # the last list item is always null so pop it
            except:
                pass

    elif (selection == "Journal"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + search + "%\' order by published_print_date_parts" + descending_or_ascending
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years+" order by published_print_date_parts" + descending_or_ascending

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
            
            #TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID like '%" + \
            #row['doi'] + "%';"
            #cursor4.execute(TotalEventsQuerySum)

            #totalEventsSum = cursor4.fetchone()

            #if totalEventsSum is None:
                #totalEventsSum = 0
            #else:
                #totalEventsSum = totalEventsSum['sumCount']

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
                       #'totalEventsSum':totalEventsSum}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    elif (selection == "Article"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + search + "%\' order by published_print_date_parts" + descending_or_ascending
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years + " order by published_print_date_parts" + descending_or_ascending

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

            #TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID like '%" + \
            #row['doi'] + "%';"
            #cursor3.execute(TotalEventsQuerySum)

            #totalEventsSum = cursor3.fetchone()

            #if totalEventsSum is None:
                #totalEventsSum = 0
            #else:
               # totalEventsSum = totalEventsSum['sumCount']


            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list} #'totalEventsSum':totalEventsSum}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        #cursor3.close()
        #cursor4.close()
        #cursor5.close()
        #cursor6.close()

        returnedQueries.pop()  # the last list item is always null so pop it


########################################################################
#
#   Pagination and Return statements
#
########################################################################
    
    per_page = 10 #article count per page
    article_start = (page*per_page)-10 #calculate starting article index (for any given page)
    article_end = article_start+10 #calculate ending article index (for any given page)

    #form a URL for href with parameters
    search_url_param = "/searchResultsPage?search=" + search + "&dropdownSearchBy=" + selection + "&page={0}" + "&startYear=" + str(startYear) + "&endYear=" + str(endYear) + "&sortSelector=" + sortSelector

    #Instantiate a pagination object
    pagination = Pagination(page=page, per_page=per_page, href=search_url_param,
                            total=len(returnedQueries), css_framework='bootstrap3')

    return flask.render_template('searchResultsPage.html', listedSearchResults=returnedQueries, dropdownSearchBy=selection, article_start=article_start, article_end=article_end, search=search, pagination=pagination)
