import flask


def articleDashboardLogic(mysql, mysql2, years_list):

    # connect to Dr Bowman's database
    cursor = mysql.connection.cursor()

    # connect to crossrefeventdatamain
    cursor2 = mysql2.connection.cursor()

    #cursor to display total number of events
    cursor3 = mysql.connection.cursor()

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
            author_sql = "select id,name from author where fk = " + \
                str(fk) + ";"
            cursor.execute(author_sql)
            author_list = cursor.fetchall()

        article = {'objectID': article_result['doi'], 'articleTitle': article_result['title'],
                   'journalName': article_result['container_title'],
                   'articleDate': article_result['published_print_date_parts'],
                   'author_list': author_list}

    cursor.close()

    # ---------------------------------- ARTICLE EVENTS --------------------------------------------
    eventsForArticle = []

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
    # Size of each list depends on how many years(in chartScript.js) you'd like to display.
    # Queries will be inserted within the array
    years_list = [2016, 2017, 2018, 2019, 2020]

    # cambia event
    cambiaEvent = []
    for year in years_list:
        cambia_sql = "select count(objectID) count from crossrefeventdatamain.cambiaevent " \
                     "where substr(objectID,17)='"+article_result['doi']+"' " \
                     "and substr(occurredAt,1,4)='"+str(year)+"';"

        cursor2.execute(cambia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        cambiaEvent.append(event_count['count'])
    # cambiaEvent = [30, 20, 50, 10, 90]  # TBD - delete this line after we upload data in cambia event table for all these years

    # crossrefevent
    crossrefevent = []
    for year in years_list:
        crossref_sql = "select count(objectID) count from crossrefeventdatamain.crossrefevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(crossref_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        crossrefevent.append(event_count['count'])
    # crossrefevent = [5, 7, 14, 18, 25]; # TBD - delete this line after we upload data in cambia event table for all these years

    # dataciteevent
    dataciteevent = []
    for year in years_list:
        datacite_sql = "select count(objectID) count from crossrefeventdatamain.dataciteevent " \
                       "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(datacite_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        dataciteevent.append(event_count['count'])
    # dataciteevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # f1000event
    f1000event = []
    for year in years_list:
        f1000_sql = "select count(objectID) count from crossrefeventdatamain.f1000event " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(f1000_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        f1000event.append(event_count['count'])

    # hypothesisevent
    hypothesisevent = []
    for year in years_list:
        hypothesis_sql = "select count(objectID) count from crossrefeventdatamain.hypothesisevent " \
                         "where substr(objectID,17)='" + article_result['doi'] + "' " \
                         "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(hypothesis_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        hypothesisevent.append(event_count['count'])
    # hypothesisevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # newsfeedevent
    newsfeedevent = []
    for year in years_list:
        newsfeed_sql = "select count(objectID) count from crossrefeventdatamain.newsfeedevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(newsfeed_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        newsfeedevent.append(event_count['count'])
    # newsfeedevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditevent
    redditevent = []
    for year in years_list:
        reddit_sql = "select count(objectID) count from crossrefeventdatamain.redditevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(reddit_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditevent.append(event_count['count'])
    # redditevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditlinksevent
    redditlinksevent = []
    for year in years_list:
        redditlinks_sql = "select count(objectID) count from crossrefeventdatamain.redditlinksevent " \
                          "where substr(objectID,17)='" + article_result['doi'] + "' " \
                          "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(redditlinks_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditlinksevent.append(event_count['count'])
    # redditlinksevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # stackexchangeevent
    stackexchangeevent = []
    for year in years_list:
        stackexchange_sql = "select count(objectID) count from crossrefeventdatamain.stackexchangeevent " \
                            "where substr(objectID,17)='" + article_result['doi'] + "' " \
                            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(stackexchange_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        stackexchangeevent.append(event_count['count'])
    # stackexchangeevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # twitterevent
    twitterevent = []
    for year in years_list:
        twitter_sql = "select count(objectID) count from crossrefeventdatamain.twitterevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(twitter_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        twitterevent.append(event_count['count'])
    # twitterevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # webevent
    webevent = []
    for year in years_list:
        web_sql = "select count(objectID) count from crossrefeventdatamain.webevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(web_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        webevent.append(event_count['count'])
    # webevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wikipediaevent
    wikipediaevent = []
    for year in years_list:
        wikipedia_sql = "select count(objectID) count from crossrefeventdatamain.wikipediaevent " \
            "where substr(objectID,17)='" + article_result['doi'] + "' " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wikipedia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wikipediaevent.append(event_count['count'])
    # wikipediaevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wordpressevent
    wordpressevent = []
    for year in years_list:
        wordpress_sql = "select count(objectID) count from crossrefeventdatamain.wordpressevent " \
                        "where substr(objectID,17)='" + article_result['doi'] + "' " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wordpress_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wordpressevent.append(event_count['count'])
    # wordpressevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years
    
    
    TotalEventsQuerySum = "SELECT (SELECT COUNT(totalEvents ) FROM crossrefeventdatamain.main WHERE objectID like '%" + \
        article['objectID'] + "%') AS sumCount;"
    cursor3.execute(TotalEventsQuerySum)
    mysql.connection.commit()
    totalEventsSum = cursor3.fetchone()
    cursor3.close()


    return flask.render_template('articleDashboard.html', article_detail=article, events=eventsForArticle, totalEventsSum=totalEventsSum['sumCount'],
                                 cambiaEventData=cambiaEvent,
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
