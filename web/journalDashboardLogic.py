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
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter


def journalDashboardLogic(mysql, years_list):
    
    totalEventsSum = 0
    journal_list = []  # list initializing
    cursor = mysql.connection.cursor()
    pagination = None

    try:
        # Gets page parameter flask_paginate
        page = flask.request.args.get(
            get_page_parameter(), type=int, default=1)
    except ValueError:
        page = 1

    # Grab the form "perPage" value and store it in perPage
    perPage = str(flask.request.form.get("perPage"))
    if flask.request.form.get("perPage") is None:
        if flask.request.args.get("perPage") is None:
            perPage = "10"
        else:
            perPage = str(flask.request.args.get("perPage"))

    # fetch the journal name parameter from searchResults page
    journal_name = str(flask.request.args.get("journalName"))
    sql = "Select doi, title, container_title, issue, page, published_print_date_parts, fk from _main_ where container_title like '%" + journal_name + "%\';"

    # Execute query and fetch all rows and store in result_set
    cursor.execute(sql)
    result_set = cursor.fetchall()

    # iterate the result set
    for row in result_set:
        # get fk from _main_ table
        fk = row['fk']
        author_list = []
        if fk is not None:
            # look up author table by fk
            author_sql = "select id,name from author where fk = " + \
                str(fk) + ";"
            cursor.execute(author_sql)
            # get list of authors for given fk
            author_list = cursor.fetchall()


        TotalEventsQuerySum = "SELECT totalEvents AS sumCount FROM crossrefeventdatamain.main WHERE objectID = 'https://doi.org/" + \
                row['doi'] + "';"
        cursor.execute(TotalEventsQuerySum)

        totalEventsSum = cursor.fetchone()

        if totalEventsSum is None:
                totalEventsSum = 0
        else:
                totalEventsSum = totalEventsSum['sumCount']

        # create dict with _main_ table row and author list
        article = {'objectID': row['doi'], 'articleTitle': row['title'],
                   'journalName': row['container_title'],
                   'issue': row['issue'],
                   'journalPage': row['page'],
                   'articleDate': row['published_print_date_parts'],
                   'author_list': author_list,
                   'totalEventsSum':totalEventsSum}
        journal_list.append(article)

    copyStartYear = 1997
    start_year = 1997
    end_year = 2020
    publishedPerYear = []
    # Grab all journal names from 1997 to 2020.
    while (start_year <= end_year):
        articles_per_year_sql = "select count(*) AS count " \
                                "from doidata._main_ " \
                                "where container_title like '%" + journal_name + "%' " \
                                "and substr(published_print_date_parts,1,4)='" + str(
                                    start_year) + "' ;"
        cursor.execute(articles_per_year_sql)
        yr_count = cursor.fetchone()
        publishedPerYear.append(yr_count["count"])
        start_year = start_year + 1

    cursor.close()

    per_page = int(perPage)  # article count per page
    # calculate starting article index (for any given page)
    article_start = (page * per_page) - per_page
    # calculate ending article index (for any given page)
    article_end = article_start + per_page

    journal_url_param = "/journalDashboard?journalName=" + \
        journal_name + "&page={0}" + "&perPage=" + str(per_page)

    # form a pagination object
    pagination = Pagination(page=page, per_page=per_page, href=journal_url_param,
                            total=len(journal_list), css_framework='bootstrap3')

    return flask.render_template('journalDashboard.html',
                                 totalEventsSum=totalEventsSum,
                                 journal_name=journal_name,
                                 journal_list=journal_list,
                                 publishedPerYear=publishedPerYear,
                                 pagination=pagination,
                                 article_start=article_start,
                                 article_end=article_end,
                                 perPage=perPage, 
                                 start_year=copyStartYear, 
                                 end_year=end_year,
                                 years_list=years_list,
                                 )
