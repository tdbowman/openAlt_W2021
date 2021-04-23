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

def articleDashboardLogic(mysql, mysql2, mysql3, years_list, yearInput, citation_years_list, citationYearInput):

    # connect to Dr Bowman's database
    cursor = mysql.connection.cursor()

    # connect to crossrefeventdatamain
    cursor2 = mysql2.connection.cursor()

    # get DOI parameter
    search = str(flask.request.args.get("DOI"))

    # query main table by DOI
    sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where doi like '%" + search + "%\';"

    cursor.execute(sql)
    article_result = cursor.fetchone()
    if article_result is not None:
        # get article fk
        fk = article_result['fk']

        # get list of authors for that fk
        if fk is not None:
            author_sql = "select id,name from author where fk = " + \
                str(fk) + ";"
            cursor.execute(author_sql)
            author_list = cursor.fetchall()

        article = {'objectID': article_result['doi'], 'articleTitle': article_result['title'],
                   'journalName': article_result['container_title'],
                   'articleDate': article_result['published_print_date_parts'],
                   'author_list': author_list}

    cursor.close()

    # ---------------------------------- ARTICLE EVENTS --------------------------------------
    eventsForArticle = []

    if article_result is not None:
        TotalEventsQuery = "SELECT totalEvents FROM crossrefeventdatamain.main WHERE objectID like '%" + \
            article['objectID'] + "%';"
        cursor2.execute(TotalEventsQuery)
        totalEvents = cursor2.fetchone()

        if totalEvents is not None:
            rEventsQuery = "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.hypothesisevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.newsfeedevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.redditevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.redditlinksevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.stackexchangeevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.twitterevent WHERE objectID like '%" + \
                article['objectID'] + "%' and subjectPID like '%http://twitter.com%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.webevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.wikipediaevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "UNION " + \
                "SELECT subjectPID, sourceID, relationType, MAX(timeObserved) AS recent " + \
                "FROM crossrefeventdatamain.wordpressevent WHERE objectID like '%" + \
                article['objectID'] + "%' " + \
                "GROUP BY subjectPID " + \
                "ORDER BY recent DESC " + \
                "LIMIT 50;"

            cursor2.execute(rEventsQuery)
            eventRows = cursor2.fetchall()
            count = 1
            for event in eventRows:
                # grab each event's subjectPID
                subjPID = event['subjectPID']

                if subjPID is not None:

                    media = ""
                    mediaColor = ""

                    if event['sourceID'] == "cambia":
                        media = "Cambia"
                        mediaColor = "#002f99"
                    elif event['sourceID'] == "crossref":
                        media = "Crossref"
                        mediaColor = "#F4AE22"
                    elif event['sourceID'] == "datacite":
                        media = "Datacite"
                        mediaColor = "#15d4cf"
                    elif event['sourceID'] == "f1000":
                        media = "F1000"
                        mediaColor = "#D7ffD9"
                    elif event['sourceID'] == "hypothesis":
                        media = "Hypothesis"
                        mediaColor = "#D22C7F"
                    elif event['sourceID'] == "newsfeed":
                        media = "Newsfeed"
                        mediaColor = "#a89ae5"
                    elif event['sourceID'] == "reddit":
                        media = "Reddit"
                        mediaColor = "#FF4500"
                    elif event['sourceID'] == "redditlinks":
                        media = "RedditLinks"
                        mediaColor = "#983333"
                    elif event['sourceID'] == "stackexchange":
                        media = "StackExchange"
                        mediaColor = "#ee874e"
                    elif event['sourceID'] == "twitter":
                        media = "Twitter"
                        mediaColor = "#1DA1F2"
                    elif event['sourceID'] == "web":
                        media = "Web"
                        mediaColor = "#257E22"
                    elif event['sourceID'] == "wikipedia":
                        media = "Wikipedia"
                        mediaColor = "#D7D8D9"
                    elif event['sourceID'] == "wordpressdotcom":
                        media = "Wordpress"
                        mediaColor = "#e3b9c7"

                    # Store all column values of the event into a python dictionary and add the eachEvent dictionary to the eventsForArticle list.
                    eachEvent = {'subjectPID': event['subjectPID'],
                                 'sourceID': event['sourceID'],
                                 'relationType': event['relationType'],
                                 'media': media,
                                 'media_color': mediaColor,
                                 'count': count}
                    eventsForArticle.append(eachEvent)
                    count = count + 1

    # ---------------------------- End of Article Events ----------------------------------------

    # ------------------------------ Dynamic Year Range Selector Bounds and Range ------------------------

        boundsQuery = "SELECT totalEvents, totalCambiaEvents, totalCrossrefEvents, totalDataciteEvents, " + \
            "totalF1000Events, totalHypothesisEvents, totalNewsfeedEvents, totalRedditEvents, " + \
            "totalRedditLinksEvents, totalStackExchangeEvents, totalTwitterEvents, totalWebEvents, " + \
            "totalWikipediaEvents, totalWordpressEvents " + \
            "FROM crossrefeventdatamain.main " + \
            "WHERE objectID like '%" + article['objectID'] + "%';"

        cursor2.execute(boundsQuery)
        mainRow = cursor2.fetchone()
        # ----------------------------- Event Count for each platform across 5 years -------------------------------------

        # Size of each list depends on how many years(in chartScript.js) you'd like to display.
        # Queries will be inserted within the array
        # years_list = [2016, 2017, 2018, 2019, 2020]

        # initialize social media event lists
        cambiaevent = []
        crossrefevent = []
        dataciteevent = []
        f1000event = []
        hypothesisevent = []
        newsfeedevent = []
        redditevent = []
        redditlinksevent = []
        stackexchangeevent = []
        twitterevent = []
        webevent = []
        wikipediaevent = []
        webevent = []
        wordpressevent = []

        # ----------------------------- Event Count for each platform across 5 years ---------------------------------
        if mainRow is not None:

            # cambia event
            if mainRow['totalCambiaEvents'] is not None:

                for year in years_list:
                    cambia_sql = "select count(objectID) count from crossrefeventdatamain.cambiaevent " \
                        "where substr(objectID,17)='"+article_result['doi']+"' " \
                        "and substr(occurredAt,1,4)='"+str(year)+"';"

                cursor2.execute(cambia_sql)

                event_count = cursor2.fetchone()
                cambiaevent.append(event_count['count'])

            # crossrefevent
            if mainRow['totalCrossrefEvents'] is not None:

                for year in years_list:
                    crossref_sql = "select count(objectID) count from crossrefeventdatamain.crossrefevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(crossref_sql)

                    event_count = cursor2.fetchone()
                    crossrefevent.append(event_count['count'])

            # dataciteevent
            if mainRow['totalDataciteEvents'] is not None:

                for year in years_list:
                    datacite_sql = "select count(objectID) count from crossrefeventdatamain.dataciteevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(datacite_sql)

                    event_count = cursor2.fetchone()
                    dataciteevent.append(event_count['count'])

            # f1000event
            if mainRow['totalF1000Events'] is not None:

                for year in years_list:
                    f1000_sql = "select count(objectID) count from crossrefeventdatamain.f1000event " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(f1000_sql)

                    event_count = cursor2.fetchone()
                    f1000event.append(event_count['count'])

            # hypothesisevent
            if mainRow['totalHypothesisEvents'] is not None:

                for year in years_list:
                    hypothesis_sql = "select count(objectID) count from crossrefeventdatamain.hypothesisevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(hypothesis_sql)

                    event_count = cursor2.fetchone()
                    hypothesisevent.append(event_count['count'])

            # newsfeedevent
            if mainRow['totalNewsfeedEvents'] is not None:

                for year in years_list:
                    newsfeed_sql = "select count(objectID) count from crossrefeventdatamain.newsfeedevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(newsfeed_sql)

                    event_count = cursor2.fetchone()
                    newsfeedevent.append(event_count['count'])

            # redditevent
            if mainRow['totalRedditEvents'] is not None:

                for year in years_list:
                    reddit_sql = "select count(objectID) count from crossrefeventdatamain.redditevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(reddit_sql)

                    event_count = cursor2.fetchone()
                    redditevent.append(event_count['count'])

            # redditlinksevent
            if mainRow['totalRedditLinksEvents'] is not None:

                for year in years_list:
                    redditlinks_sql = "select count(objectID) count from crossrefeventdatamain.redditlinksevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(redditlinks_sql)

                    event_count = cursor2.fetchone()
                    redditlinksevent.append(event_count['count'])

            # stackexchangeevent
            if mainRow['totalStackExchangeEvents'] is not None:

                for year in years_list:
                    stackexchange_sql = "select count(objectID) count from crossrefeventdatamain.stackexchangeevent " \
                                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                                        "and substr(occurredAt,1,4)='" + \
                        str(year) + "';"

                    cursor2.execute(stackexchange_sql)

                    event_count = cursor2.fetchone()
                    stackexchangeevent.append(event_count['count'])

            # twitterevent
            if mainRow['totalTwitterEvents'] is not None:

                for year in years_list:
                    twitter_sql = "select count(objectID) count from crossrefeventdatamain.twitterevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(twitter_sql)

                    event_count = cursor2.fetchone()
                    twitterevent.append(event_count['count'])

            # webevent
            if mainRow['totalWebEvents'] is not None:

                for year in years_list:
                    web_sql = "select count(objectID) count from crossrefeventdatamain.webevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(web_sql)

                    event_count = cursor2.fetchone()
                    webevent.append(event_count['count'])

            # wikipediaevent
            if mainRow['totalWikipediaEvents'] is not None:

                for year in years_list:
                    wikipedia_sql = "select count(objectID) count from crossrefeventdatamain.wikipediaevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(wikipedia_sql)

                    event_count = cursor2.fetchone()
                    wikipediaevent.append(event_count['count'])

            # wordpressevent
            if mainRow['totalWordpressEvents'] is not None:

                for year in years_list:
                    wordpress_sql = "select count(objectID) count from crossrefeventdatamain.wordpressevent " \
                                    "where substr(objectID,17)='" + article_result['doi'] + "' " \
                                    "and substr(occurredAt,1,4)='" + \
                        str(year) + "';"

                    cursor2.execute(wordpress_sql)

                    event_count = cursor2.fetchone()
                    wordpressevent.append(event_count['count'])

        # ----------------------------- End of Event Count for each platform across 5 years ---------------------------------

        if mainRow is None:
            totalEventsSum = 0
        else:
            totalEventsSum = mainRow['totalEvents']
    else:
        years_list = []
        article = {}
        eventsForArticle = []
        totalEventsSum = 0
        cambiaevent = []
        crossrefevent = []
        dataciteevent = []
        f1000event = []
        hypothesisevent = []
        newsfeedevent = []
        redditevent = []
        redditlinksevent = []
        stackexchangeevent = []
        twitterevent = []
        webevent = []
        wikipediaevent = []
        wordpressevent = []

	
	#Author: 
    #Name: Mohammad Tahmid 
    #Lines 391-401, 446
    #---------------------
	#Date: 02/23/2021
	#Description: Fetches data from database per every article in the article landing page
	
    citationCountquery = """SELECT count FROM opencitations.citation_count WHERE doi = '%s'""" % (search)
    cursor3 = mysql3.connection.cursor()
    cursor3.execute(citationCountquery)
    citationCountResult = cursor3.fetchone()

    # Author: Rihat Rahman
    # Lines: 413 - 467
    #---------------------------------------------------------------------------------------------
    citationChartResults = []

    for year in citation_years_list:

        citationChartquery = "SELECT COUNT(*) count FROM opencitations.citations WHERE cited = '" + article_result['doi'] + "' and substr(creation,1,4)= '" +  str(year) + "';"
        cursor3 = mysql3.connection.cursor()
        cursor3.execute(citationChartquery)
        citationCount = cursor3.fetchone()
        citationChartResults.append(citationCount['count'])



    cambiaeventForTable = cambiaevent
    crossrefeventForTable = crossrefevent
    dataciteeventForTable = dataciteevent
    f1000eventForTable = f1000event
    hypothesiseventForTable = hypothesisevent
    newsfeedeventForTable = newsfeedevent
    redditeventForTable =  redditevent
    redditlinkseventForTable = redditlinksevent
    stackexchangeeventForTable = stackexchangeevent
    twittereventForTable = twitterevent
    webeventForTable = webevent
    wikipediaeventForTable = wikipediaevent
    wordpresseventForTable = wordpressevent
        

    cambiaevent = organizeEventData(cambiaevent)
    crossrefevent = organizeEventData(crossrefevent)
    dataciteevent = organizeEventData(dataciteevent)
    f1000event = organizeEventData(f1000event)
    hypothesisevent = organizeEventData(hypothesisevent)
    newsfeedevent = organizeEventData(newsfeedevent)
    redditevent = organizeEventData(redditevent)
    redditlinksevent = organizeEventData(redditlinksevent)
    stackexchangeevent = organizeEventData(stackexchangeevent)
    twitterevent = organizeEventData(twitterevent)
    webevent = organizeEventData(webevent)
    wikipediaevent = organizeEventData(wikipediaevent)
    wordpressevent = organizeEventData(wordpressevent)

    return flask.render_template('articleDashboard.html', years_list=years_list, citation_years_list= citation_years_list, citationYearInput = citationYearInput, yearInput=yearInput, article_detail=article, events=eventsForArticle, totalEventsSum=totalEventsSum,
                                 cambiaEventData=cambiaevent,
                                 crossrefEventData=crossrefevent,
                                 dataciteEventData=dataciteevent,
                                 f1000eventData=f1000event,
                                 hypothesisEventData=hypothesisevent,
                                 newsfeedEventData=newsfeedevent,
                                 redditEventData=redditevent,
                                 redditlinksEventData=redditlinksevent,
                                 stackexchangeEventData=stackexchangeevent,
                                 twitterEventData=twitterevent,
                                 webEventData=webevent,
                                 wikipediaEventData=wikipediaevent,
                                 wordpressEventData=wordpressevent,
								 citationCount=citationCountResult,
                                 citationChartData = citationChartResults,
                                 cambiaeventForTable = cambiaeventForTable,
                                 crossrefeventForTable = crossrefeventForTable,
                                 dataciteeventForTable = dataciteeventForTable,
                                 f1000eventForTable = f1000eventForTable,
                                 hypothesiseventForTable = hypothesiseventForTable,
                                 newsfeedeventForTable = newsfeedeventForTable,
                                 redditeventForTable =  redditeventForTable,
                                 redditlinkseventForTable = redditlinkseventForTable,
                                 stackexchangeeventForTable = stackexchangeeventForTable,
                                 twittereventForTable = twittereventForTable,
                                 webeventForTable = webeventForTable,
                                 wikipediaeventForTable = wikipediaeventForTable,
                                 wordpresseventForTable = wordpresseventForTable)

def organizeEventData (eventData):

    cleanEventData = [None] * 5

    for i in range(len(eventData)):

        if eventData[i] != 0:
            cleanEventData[i] = eventData[i]

    return cleanEventData
#---------------------------------------------------------------------------------------------