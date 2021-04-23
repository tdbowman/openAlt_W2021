"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import flask
from flask import Flask, session
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter


def searchLogic(mysql, mysql2, dropdownValue):

    # Declare variables here for readability
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    cursor3 = mysql2.connection.cursor()
    cursor4 = mysql2.connection.cursor()
    cursor5 = mysql2.connection.cursor()
    cursor6 = mysql2.connection.cursor()

    row = "something not none"
    totalEventsSum = 0
    pagination = None
    s_years = None
    startYear = None
    endYear = None
    sortSelector = None
    returnedQueries = []
    selected_years = []
    domain = None
    country = None
    university = None

    # sort by descending by default, change to asc if user wants
    descending_or_ascending = " desc;"

    # Get page number if it exists. If not, set to 1
    try:
        page = flask.request.args.get(
            get_page_parameter(), type=int, default=1)
    except ValueError:
        page = 1

    # get search and dropdownSearchBy parameters from GET request if form data is None
    # This occurs when you click on a page number, since the hidden form is not repopulated
    search = str(flask.request.form.get("search"))
    selection = str(flask.request.form.get("dropdownSearchBy"))
    startYear = flask.request.form.get("startYear")
    endYear = flask.request.form.get("endYear")
    sortSelector = flask.request.form.get('sortSelector')
    perPage = str(flask.request.form.get("perPage"))
    country = flask.request.form.get('country')
    domain = flask.request.form.get("domain")
    university = flask.request.form.get("university")


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
    if flask.request.form.get("perPage") is None:
        if flask.request.args.get("perPage") is None:
            perPage = "10"
        else:
            perPage = str(flask.request.args.get("perPage"))

    if flask.request.form.get("domain") is None:
        domain = flask.request.args.get("domain")

    if flask.request.form.get("country") is None:
        country = flask.request.args.get("country")

    if flask.request.form.get("university") is None:
        university = flask.request.args.get("university")
        

    # Now that we have checked the form and URL for how the user would like to search, we can set it
    if (sortSelector == "PublicationYearAscending"):
        descending_or_ascending = " asc;"
    else:
        descending_or_ascending = " desc;"  # redundant but having this here is clearer

    # Grab the years from the year form if they exist
    # Store these in selected_years list. This is related to the s_years string, but used in different ways
    try:
        # used in the year range form
        startYear = int(startYear)
        endYear = int(endYear)
        temp_year = startYear  # We want to keep startYear unchanged from users input
        if temp_year > datetime.now().year:
            pass  # If user enters a year greater than this year, just proceed to the except block AKA execute search with no year filter

        # Build up a list of selected years, ranging from startYear to endYear
        while (temp_year < endYear + 1):
            selected_years.append(temp_year)
            temp_year += 1
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

    #   Select which SQL to execute, based on the drop-down selection,
    #   the search term, and the years selected, if any


    # Author: Rihat Rahman
    # Lines: 120 - 168
    # create part of the query for advanced search and add it to the regular search query
    # ---------------------------------------------------------------------------------------------------
    if (country == None) | (country == 'Select'):
        country = ''
        country_query = ''

    else:
        country_query = country_query =  " country like '%" + country + "%'"


    if domain == None:
        domain = ''
        domain_query = ''

    else:
        domain_query = "(select fk from doidata.content_domain where domain like '" + domain + "')"


    if (university == None) | (university == '') :
        university = ''
        university_query = ''

    else:
        university_query = " university like '%" + university + "%'"

    advanced_query = ''

    if (country != '') | (university != '') | (domain != ''):

        prefix = ' and fk in '

        if (country == '') & (university == '') & (domain != ''):
            advanced_query = prefix + domain_query

        else:

            if (country != '') & (university != ''):
                
                if domain != '':
                    advanced_query = prefix + ' (select fk from doidata.author where ' + country_query + 'and' + university_query + ' and fk in ' + domain_query + ') '

                else:
                    advanced_query = prefix + ' (select fk from doidata.author where ' + country_query + 'and' + university_query + ') '

            else:

                if domain != '':
                    advanced_query = prefix + ' (select fk from doidata.author where ' + country_query + university_query + ' and fk in ' + domain_query + ') '

                else:
                    advanced_query = prefix + ' (select fk from doidata.author where ' + country_query + university_query + ') '
    # ---------------------------------------------------------------------------------------------------


    # Search by DOI
    if (selection == "DOI"):


        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from doidata._main_ where doi like '%" + \
                search + "%'" + advanced_query + " order by published_print_date_parts" + descending_or_ascending 
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from doidata._main_ where doi like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in " + \
                s_years + advanced_query + " order by published_print_date_parts" + descending_or_ascending

        
        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the _main_ table result set
        for row in result_set:

            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name, university, country from doidata.author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # Author: Rihat Rahman
            # Lines: 210 - 224
            # arrays to store country and university information and display in on search results page
            # ---------------------------------------------------------------------------------------------------
            list_of_countries = []
            list_of_universities = []

            for author in author_list:

                if author['country'] not in list_of_countries:
                    if author['country'] != None:
                        if author['country'] != '':
                            list_of_countries.append(author['country'])


                if author['university'] not in list_of_universities:
                    if author['university'] != None:
                        if author['university'] != '':
                            list_of_universities.append(author['university'])
            # ---------------------------------------------------------------------------------------------------


            TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + \
                row['doi'] + "';"
            cursor6.execute(TotalEventsQuerySum)

            totalEventsSum = cursor6.fetchone()

            if totalEventsSum is None:
                totalEventsSum = 0
            else:
                totalEventsSum = totalEventsSum['sumCount']

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list,
                       'totalEventsSum': totalEventsSum,
                       'list_of_countries': list_of_countries,
                       'list_of_universities': list_of_universities}
            # append article dict to returnedQueries list
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        cursor6.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    elif (selection == "Author"):
        # get fk and name for searched author name
        given_author = []
        given_author = '( '
        auth_sql = "SELECT fk, name, university, country FROM doidata.author where name like'%" + search + "%';"
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
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
                    given_author + advanced_query + " order by published_print_date_parts" + descending_or_ascending + ";"
            else:
                # with year filter
                sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
                    given_author + \
                    " and substr(published_print_date_parts, 1,4) in" + \
                    s_years + advanced_query + " order by published_print_date_parts" + descending_or_ascending + ";"

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
                        author_sql = "select id, name, university, country from doidata.author where fk = " + \
                            str(fk) + ";"
                        cursor.execute(author_sql)
                        # get list of authors for given fk
                        author_list = cursor.fetchall()

                    # Author: Rihat Rahman
                    # Lines: 302 - 315
                    # arrays to store country and university information and display in on search results page
                    # ---------------------------------------------------------------------------------------------------
                    list_of_countries = []
                    list_of_universities = []

                    for author in author_list:
                        if author['country'] not in list_of_countries:
                            if author['country'] != None:
                                if author['country'] != '':
                                    list_of_countries.append(author['country'])


                        if author['university'] not in list_of_universities:
                            if author['university'] != None:
                                if author['university'] != '':
                                    list_of_universities.append(author['university'])
                    # ---------------------------------------------------------------------------------------------------

                    TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + \
                        row['doi'] + "';"
                    cursor5.execute(TotalEventsQuerySum)

                    totalEventsSum = cursor5.fetchone()

                    if totalEventsSum is None:
                        totalEventsSum = 0
                    else:
                        totalEventsSum = totalEventsSum['sumCount']

                    # create dict with _main_ table row and author list
                    article = {'objectID': row['doi'], 'articleTitle': row['title'],
                               'journalName': row['container_title'],
                               'articleDate': row['published_print_date_parts'],
                               'author_list': author_list,
                               'totalEventsSum': totalEventsSum,
                               'list_of_countries': list_of_countries,
                                'list_of_universities': list_of_universities}
                    # append article dict to returnedQueries list
                    returnedQueries.append(article)

                returnedQueries.append(None)
                cursor.close()
                cursor5.close()
                returnedQueries.pop()  # the last list item is always null so pop it
            except:
                pass

    elif (selection == "Journal"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + \
                search + "%\'" +  advanced_query + " order by published_print_date_parts" + descending_or_ascending + ";"
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where container_title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years + advanced_query +" order by published_print_date_parts" + descending_or_ascending + ";"

        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name, country, university from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()


            # Author: Rihat Rahman
            # Lines: 380 - 393
            # arrays to store country and university information and display in on search results page
            # ---------------------------------------------------------------------------------------------------
            list_of_countries = []
            list_of_universities = []

            for author in author_list:
                if author['country'] not in list_of_countries:
                    if author['country'] != None:
                        if author['country'] != '':
                            list_of_countries.append(author['country'])


                if author['university'] not in list_of_universities:
                    if author['university'] != None:
                        if author['university'] != '':
                            list_of_universities.append(author['university'])
             # ---------------------------------------------------------------------------------------------------

            TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + \
                row['doi'] + "';"
            cursor4.execute(TotalEventsQuerySum)

            totalEventsSum = cursor4.fetchone()

            if totalEventsSum is None:
                totalEventsSum = 0
            else:
                totalEventsSum = totalEventsSum['sumCount']

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list,
                       'totalEventsSum': totalEventsSum,
                       'list_of_countries': list_of_countries,
                        'list_of_universities': list_of_universities}
            returnedQueries.append(article)

        returnedQueries.append(None)
        cursor.close()
        cursor4.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    elif (selection == "Article"):
        if not selected_years:
            # no year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + \
                search +  "%\'" + advanced_query + " order by published_print_date_parts" + descending_or_ascending + ";"
        else:
            # with year filter
            sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where title like '%" + \
                search + \
                "%\' and substr(published_print_date_parts, 1,4) in" + \
                s_years + advanced_query + " order by published_print_date_parts" + descending_or_ascending + ";"


        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name, university, country from doidata.author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()


            # Author: Rihat Rahman
            # Lines: 456 - 469
            # arrays to store country and university information and display in on search results page
            # ---------------------------------------------------------------------------------------------------
            list_of_countries = []
            list_of_universities = []

            for author in author_list:
                if author['country'] not in list_of_countries:
                    if author['country'] != None:
                        if author['country'] != '':
                            list_of_countries.append(author['country'])


                if author['university'] not in list_of_universities:
                    if author['university'] != None:
                        if author['university'] != '':
                            list_of_universities.append(author['university'])
            # ---------------------------------------------------------------------------------------------------

            TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID ='https://doi.org/" + \
                row['doi'] + "';"
            cursor3.execute(TotalEventsQuerySum)

            totalEventsSum = cursor3.fetchone()

            if totalEventsSum is None:
                totalEventsSum = 0
            else:
                totalEventsSum = totalEventsSum['sumCount']


            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list, 'totalEventsSum': totalEventsSum,
                       'list_of_countries': list_of_countries,
                       'list_of_universities': list_of_universities}
            returnedQueries.append(article)


        returnedQueries.append(None)
        cursor.close()
        cursor3.close()
        returnedQueries.pop()  # the last list item is always null so pop it

    # Get oldest publication date in database
    oldestPubYearQuery = "SELECT published_print_date_parts FROM _main_ " + \
        "WHERE published_print_date_parts IS NOT NULL " + \
        "ORDER BY published_print_date_parts ASC;"

    cursor2.execute(oldestPubYearQuery)
    oldestPubYear = cursor2.fetchone()
    oldestPubYear = oldestPubYear['published_print_date_parts']

    # sort returnedQueries list by totalEventsSum - commented out because when implemented it cancels out publicaton year filter
    sorted_returnedQueries = sorted(
        returnedQueries, key=lambda x: x['totalEventsSum'], reverse=True)

    # If the user has selected the "Sort by events descending" option, then use the above to sort
    if sortSelector == "eventsDescending":
        returnedQueries = sorted_returnedQueries

    #   Pagination and Return statements
    per_page = int(perPage)
    # calculate starting article index (for any given page)
    article_start = (page * per_page) - per_page
    # calculate ending article index (for any given page)
    article_end = article_start + per_page

    # form a URL for href with parameters
    search_url_param = "/searchResultsPage?search=" + search + "&dropdownSearchBy=" + selection + \
        "&page={0}" + "&startYear=" + str(startYear) + "&endYear=" + str(
            endYear) + "&sortSelector=" + sortSelector + "&perPage=" + str(per_page)

    # Instantiate a pagination object
    pagination = Pagination(page=page, per_page=per_page, href=search_url_param,
                            total=len(returnedQueries), css_framework='bootstrap3')


    return flask.render_template('searchResultsPage.html', totalEventsSum=totalEventsSum, listedSearchResults=returnedQueries, dropdownSearchBy=selection, article_start=article_start, article_end=article_end, search=search, pagination=pagination, oldestPubYear=oldestPubYear, dropdownValue=dropdownValue)
