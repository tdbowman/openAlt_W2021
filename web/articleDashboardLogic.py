import flask


def articleDashboardLogic(mysql, mysql2, years_list, yearInput):

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
                                 'media_color': mediaColor}
                    eventsForArticle.append(eachEvent)

    # ---------------------------- End of Article Events ----------------------------------------

    # ------------------------------ Dynamic Year Range Selector Bounds and Range ------------------------

        boundsQuery = "SELECT totalEvents, totalCambiaEvents, firstCambiaEvent, lastCambiaEvent, totalCrossrefEvents, " + \
            "firstCrossrefEvent, lastCrossrefEvent, totalDataciteEvents, firstDataciteEvent, lastDataciteEvent, " + \
            "totalF1000Events, firstF1000Event, lastF1000Event,  totalHypothesisEvents, firstHypothesisEvent, " + \
            "lastHypothesisEvent totalNewsfeedEvents, firstNewsfeedEvent, lastNewsfeedEvent, totalRedditEvents, " + \
            "firstRedditEvent, " + \
            "lastRedditEvent, totalRedditLinksEvents, firstRedditLinksEvent, lastRedditLinksEvent, " + \
            "totalStackExchangeEvents, firstStackExchangeEvent, lastStackExchangeEvent, totalTwitterEvents, " + \
            "firstTwitterEvent, lastTwitterEvent, totalWebEvents, firstWebEvent, lastWebEvent, totalWikipediaEvents, " + \
            "firstWikipediaEvent, lastWikipediaEvent, totalWordpressEvents, firstWordpressEvent, lastWordpressEvent " + \
            "FROM crossrefeventdatamain.main " + \
            "WHERE objectID like '%" + article['objectID'] + "%';"

        cursor2.execute(boundsQuery)
        mainRow = cursor2.fetchone()

        # ***********Year Range Slider decomissioned until after P3 ***************
        # firstEventList = []
        # lastEventList = []
        # minimumBound = ""
        # maximumBound = ""
        # if mainRow is not None:
        #     if mainRow['totalCambiaEvents'] is not None:
        #         firstEventList.append(mainRow['firstCambiaEvent'])
        #         lastEventList.append(mainRow['lastCambiaEvent'])
        #     if mainRow['totalCrossrefEvents'] is not None:
        #         firstEventList.append(mainRow['firstCrossrefEvent'])
        #         lastEventList.append(mainRow['lastCrossrefEvent'])
        #     if mainRow['totalDataciteEvents'] is not None:
        #         firstEventList.append(mainRow['firstDataciteEvent'])
        #         lastEventList.append(mainRow['lastDataciteEvent'])
        #     if mainRow['totalF1000Events'] is not None:
        #         firstEventList.append(mainRow['firstF1000Event'])
        #         lastEventList.append(mainRow['lastF1000Event'])
        #     if mainRow['totalHypothesisEvents'] is not None:
        #         firstEventList.append(mainRow['firstHypothesisEvent'])
        #         lastEventList.append(mainRow['lastHypothesisEvent'])
        #     if mainRow['totalNewsfeedEvents'] is not None:
        #         firstEventList.append(mainRow['firstNewsfeedEvent'])
        #         lastEventList.append(mainRow['lastNewsfeedEvent'])
        #     if mainRow['totalRedditEvents'] is not None:
        #         firstEventList.append(mainRow['firstRedditEvent'])
        #         lastEventList.append(mainRow['lastRedditEvent'])
        #     if mainRow['totalRedditLinksEvents'] is not None:
        #         firstEventList.append(mainRow['firstRedditLinksEvent'])
        #         lastEventList.append(mainRow['lastRedditLinksEvent'])
        #     if mainRow['totalStackExchangeEvents'] is not None:
        #         firstEventList.append(mainRow['firstStackExchangeEvent'])
        #         lastEventList.append(mainRow['lastStackExchangeEvent'])
        #     if mainRow['totalTwitterEvents'] is not None:
        #         firstEventList.append(mainRow['firstTwitterEvent'])
        #         lastEventList.append(mainRow['lastTwitterEvent'])
        #     if mainRow['totalWebEvents'] is not None:
        #         firstEventList.append(mainRow['firstWebEvent'])
        #         lastEventList.append(mainRow['lastWebEvent'])
        #     if mainRow['totalWikipediaEvents'] is not None:
        #         firstEventList.append(mainRow['firstWikipediaEvent'])
        #         lastEventList.append(mainRow['lastWikipediaEvent'])
        #     if mainRow['totalWordpressEvents'] is not None:
        #         firstEventList.append(mainRow['firstWordpressEvent'])
        #         lastEventList.append(mainRow['lastWordpressEvent'])

        #     noEvents = False
        # else:
        #     noEvents = True

        # if noEvents is False:
        #     minimumBound = str(firstEventList[0])
        #     maximumBound = str(lastEventList[0])

        # for time in firstEventList:
        #     if minimumBound > str(time):
        #         minimumBound = str(time)
        # for time in lastEventList:
        #     if maximumBound < str(time):
        #         maximumBound = str(time)

        # # Grab the years only
        # minimumBound = minimumBound[0:4]
        # maximumBound = maximumBound[0:4]

    # ----------------------------- End of Dynamic Year Range Selector Bounds and Range --------------------------------
    # ----------------------------- Event Count for each platform across 5 years -------------------------------------

    # Size of each list depends on how many years(in chartScript.js) you'd like to display.
    # Queries will be inserted within the array
    #years_list = [2016, 2017, 2018, 2019, 2020]

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

        if mainRow is not None:
            # ***********Year Range Slider decomissioned until after P3 ***************
            # print("Years List passed: ", years_list)

            # cambia event
            if mainRow['totalCambiaEvents'] is not None:

                for year in years_list:
                    cambia_sql = "select count(objectID) count from crossrefeventdatamain.cambiaevent " \
                        "where substr(objectID,17)='"+article_result['doi']+"' " \
                        "and substr(occurredAt,1,4)='"+str(year)+"';"

                cursor2.execute(cambia_sql)

                event_count = cursor2.fetchone()
                cambiaevent.append(event_count['count'])
            # cambiaEvent = [30, 20, 50, 10, 90]  # TBD - delete this line after we upload data in cambia event table for all these years

            # crossrefevent
            if mainRow['totalCrossrefEvents'] is not None:

                for year in years_list:
                    crossref_sql = "select count(objectID) count from crossrefeventdatamain.crossrefevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(crossref_sql)

                    event_count = cursor2.fetchone()
                    crossrefevent.append(event_count['count'])
                # crossrefevent = [5, 7, 14, 18, 25]; # TBD - delete this line after we upload data in cambia event table for all these years

            # dataciteevent
            if mainRow['totalDataciteEvents'] is not None:

                for year in years_list:
                    datacite_sql = "select count(objectID) count from crossrefeventdatamain.dataciteevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(datacite_sql)

                    event_count = cursor2.fetchone()
                    dataciteevent.append(event_count['count'])
                # dataciteevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

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
                # hypothesisevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

            # newsfeedevent
            if mainRow['totalNewsfeedEvents'] is not None:

                for year in years_list:
                    newsfeed_sql = "select count(objectID) count from crossrefeventdatamain.newsfeedevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(newsfeed_sql)

                    event_count = cursor2.fetchone()
                    newsfeedevent.append(event_count['count'])
                # newsfeedevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

            # redditevent
            if mainRow['totalRedditEvents'] is not None:

                for year in years_list:
                    reddit_sql = "select count(objectID) count from crossrefeventdatamain.redditevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(reddit_sql)

                    event_count = cursor2.fetchone()
                    redditevent.append(event_count['count'])
                # redditevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

            # redditlinksevent
            if mainRow['totalRedditLinksEvents'] is not None:

                for year in years_list:
                    redditlinks_sql = "select count(objectID) count from crossrefeventdatamain.redditlinksevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(redditlinks_sql)

                    event_count = cursor2.fetchone()
                    redditlinksevent.append(event_count['count'])
                # redditlinksevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

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
                # stackexchangeevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

            # twitterevent
            if mainRow['totalTwitterEvents'] is not None:

                for year in years_list:
                    twitter_sql = "select count(objectID) count from crossrefeventdatamain.twitterevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(twitter_sql)

                    event_count = cursor2.fetchone()
                    twitterevent.append(event_count['count'])
                # twitterevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

            # webevent
            if mainRow['totalWebEvents'] is not None:

                for year in years_list:
                    web_sql = "select count(objectID) count from crossrefeventdatamain.webevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

                    cursor2.execute(web_sql)

                    event_count = cursor2.fetchone()
                    webevent.append(event_count['count'])
                # webevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

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
        # An unbound local error of article_result was showing up here in the console but not in the flask debugger. This needed to be fixed by creating this else statement to handle a situation where article_result is a None type.
        # This error needed to be fixed for the 500 Internal Server Error when using an ajax call from articleDashboard.html
        # *********** Year Range Slider decomissioned until after P3 ***************
        # minimumBound = ''
        # maximumBound = ''
        # Make sure to add this to the render_template(minimumBound=minimumBound, maximumBound=maximumBound,) function call
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

    return flask.render_template('articleDashboard.html', years_list=years_list, yearInput=yearInput, article_detail=article, events=eventsForArticle, totalEventsSum=totalEventsSum,
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
                                 wordpressEventData=wordpressevent)
