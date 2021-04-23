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


def authorDashboardLogic(mysql, mysql2, years_list, yearInput):

    author_article_list = []
    author_doi_list = []

    # Initialize our cursor to doidata database
    cursor = mysql.connection.cursor()

    #global mysql2
    # Initialize our cursor to crossrefeventdatamain database
    cursor2 = mysql2.connection.cursor()

    pagination = None

    try:
        # Gets page parameter flask_paginate
        page = flask.request.args.get(
            get_page_parameter(), type=int, default=1)
        print('--Page number-- ', page)
    except ValueError:
        page = 1

    # Grab the form "perPage" value and store it in perPage
    perPage = str(flask.request.form.get("perPage"))
    if flask.request.form.get("perPage") is None:
        if flask.request.args.get("perPage") is None:
            perPage = "10"
        else:
            perPage = str(flask.request.args.get("perPage"))

    # fetch the query parameter author_id from the searchResults page
    author_id = str(flask.request.args.get("author_id"))

    author_sql = "SELECT name FROM doidata.author where id ="+author_id+";"
    cursor.execute(author_sql)
    author_name = cursor.fetchone()

    author_sql = "SELECT fk FROM doidata.author where name = '" + \
        author_name['name'] + "';"
    cursor.execute(author_sql)
    author_resultset = cursor.fetchall()

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

    # Queries will be inserted within the array
    #years_list = [2016, 2017, 2018, 2019, 2020]

    # Form a list of just the DOIs
    doi_list = '( '
    for doi in author_doi_list:
        if doi == author_doi_list[-1]:
            doi_list = doi_list + "'" + str(doi) + "'"
        else:
            doi_list = doi_list + "'" + str(doi) + "'" + ","
    doi_list = doi_list + ')'

    # ------------------------- Event count for each platform for the Bar Chart --------------------
    # Cambia Event
    cambiaEvent = []
    for year in years_list:
        cambia_sql = "select count(objectID) count from crossrefeventdatamain.cambiaevent " \
                     "where substr(objectID,17) in " + doi_list + " " \
                     "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(cambia_sql)
        event_count = cursor2.fetchone()
        cambiaEvent.append(event_count['count'])

    # Crossref Events
    crossrefevent = []
    for year in years_list:
        crossref_sql = "select count(objectID) count from crossrefeventdatamain.crossrefevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(crossref_sql)
        event_count = cursor2.fetchone()
        crossrefevent.append(event_count['count'])

    # Datacite Events
    dataciteevent = []
    for year in years_list:
        datacite_sql = "select count(objectID) count from crossrefeventdatamain.dataciteevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(datacite_sql)
        event_count = cursor2.fetchone()
        dataciteevent.append(event_count['count'])

    # F1000 Events
    f1000event = []
    for year in years_list:
        f1000_sql = "select count(objectID) count from crossrefeventdatamain.f1000event " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(f1000_sql)
        event_count = cursor2.fetchone()
        f1000event.append(event_count['count'])

    # Hypothesis Event
    hypothesisevent = []
    for year in years_list:
        hypothesis_sql = "select count(objectID) count from crossrefeventdatamain.hypothesisevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(hypothesis_sql)
        event_count = cursor2.fetchone()
        hypothesisevent.append(event_count['count'])

    # Newsfeed Event
    newsfeedevent = []
    for year in years_list:
        newsfeed_sql = "select count(objectID) count from crossrefeventdatamain.newsfeedevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(newsfeed_sql)
        event_count = cursor2.fetchone()
        newsfeedevent.append(event_count['count'])

    # Reddit Event
    redditevent = []
    for year in years_list:
        reddit_sql = "select count(objectID) count from crossrefeventdatamain.redditevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(reddit_sql)
        event_count = cursor2.fetchone()
        redditevent.append(event_count['count'])

    # Redditlinks Event
    redditlinksevent = []
    for year in years_list:
        redditlinks_sql = "select count(objectID) count from crossrefeventdatamain.redditlinksevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(redditlinks_sql)
        event_count = cursor2.fetchone()
        redditlinksevent.append(event_count['count'])

    # Stackexchange Event
    stackexchangeevent = []
    for year in years_list:
        stackexchange_sql = "select count(objectID) count from crossrefeventdatamain.stackexchangeevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(stackexchange_sql)
        event_count = cursor2.fetchone()
        stackexchangeevent.append(event_count['count'])

    # Twitter Event
    twitterevent = []
    for year in years_list:
        twitter_sql = "select count(objectID) count from crossrefeventdatamain.twitterevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(twitter_sql)
        event_count = cursor2.fetchone()
        twitterevent.append(event_count['count'])

    # Web Event
    webevent = []
    for year in years_list:
        web_sql = "select count(objectID) count from crossrefeventdatamain.webevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(web_sql)
        event_count = cursor2.fetchone()
        webevent.append(event_count['count'])

    # Wikipedia Event
    wikipediaevent = []
    for year in years_list:
        wikipedia_sql = "select count(objectID) count from crossrefeventdatamain.wikipediaevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wikipedia_sql)
        event_count = cursor2.fetchone()
        wikipediaevent.append(event_count['count'])

    # Wordpress Event
    wordpressevent = []
    for year in years_list:
        wordpress_sql = "select count(objectID) count from crossrefeventdatamain.wordpressevent " \
                        "where substr(objectID,17) in " + doi_list + " " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wordpress_sql)
        event_count = cursor2.fetchone()
        wordpressevent.append(event_count['count'])

    cursor2.close()

    per_page = int(perPage)  # article count per page
    # calculate starting article index (for any given page)
    article_start = (page * per_page) - per_page
    # calculate ending article index (for any given page)
    article_end = article_start + per_page

    author_url_param = "/authorDashboard?author_id=" + \
        str(author_id) + "&page={0}" + "&perPage=" + str(per_page)

    # form a pagination object
    pagination = Pagination(page=page, per_page=per_page, href=author_url_param,
                            total=len(author_article_list), css_framework='bootstrap3')

    return flask.render_template('authorDashboard.html',
                                 author_name=author_name['name'],
                                 years_list=years_list, 
                                 yearInput=yearInput,
                                 passed_author_id=author_id,  # this is for the year filter!
                                 author_article_list=author_article_list,
                                 cambiaEventData=cambiaEvent,
                                 crossrefEventData=crossrefevent,
                                 f1000eventData=f1000event,
                                 dataciteEventData=dataciteevent,
                                 hypothesisEventData=hypothesisevent,
                                 newsfeedEventData=newsfeedevent,
                                 redditEventData=redditevent,
                                 redditlinksEventData=redditlinksevent,
                                 stackexchangeEventData=stackexchangeevent,
                                 twitterEventData=twitterevent,
                                 webEventData=webevent,
                                 wikipediaEventData=wikipediaevent,
                                 wordpressEventData=wordpressevent,
                                 pagination=pagination,
                                 article_start=article_start,
                                 article_end=article_end,
                                 perPage=perPage
                                 )