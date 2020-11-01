import flask

def articleDashboardLogic(mysql, mysql2):
    
    # connect to Dr Bowman's database
    cursor = mysql.connection.cursor()

    # connect to crossrefeventdatamain
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
            author_sql = "select id,name from author where fk = " + \
                str(fk) + ";"
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
    twitterEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.twitterevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%' "

    # "UNION ALL " not working meaning it only displays columns for the first query but nothing else.
    wikipediaEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.wikipediaevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%';"

    hypothesisEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.hypothesisevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%';"

    newsfeedEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.newsfeedevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    redditEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.redditevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    redditLinksEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.redditlinksevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    stackexchangeEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.stackexchangeevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    webEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.webevent "
    "WHERE objectID like '%" + \
        article['objectID'] + "%'; "

    wordpressEventQuery = "SELECT subjectID,sourceID,relationType,objectID FROM crossrefeventdatamain.wordpressevent "
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
                             'relationType': tweet['relationType'],
                             'media': 'twitter',
                             'media_color': '#1DA1F2',
                             'objectID': tweet['objectID']}
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
                             'media': 'wiki',
                             'media_color': '#D7D8D9',
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
                             'relationType': hypo['relationType'],
                             'media': 'hypothesis',
                             'media_color': '#D22C7F',
                             'objectID': hypo['objectID']}
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
                             'relationType': news['relationType'],
                             'media': 'newsfeed',
                             'media_color': '#a89ae5',
                             'objectID': news['objectID']}
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
                             'relationType': red['relationType'],
                             'media': 'reddit',
                             'media_color': '#FF4500',
                             'objectID': red['objectID']}
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
                             'relationType': redl['relationType'],
                             'media': 'redditlinks',
                             'media_color': '#983333',
                             'objectID': redl['objectID']}
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
                             'relationType': stack['relationType'],
                             'media': 'stackex',
                             'media_color': '#ee874e',
                             'objectID': stack['objectID']}
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
                             'relationType': web['relationType'],
                             'media': 'web',
                             'media_color': '#257E22',
                             'objectID': web['objectID']}
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
                             'relationType': word['relationType'],
                             'media': 'wordpress',
                             'media_color': '#e3b9c7',
                             'objectID': word['objectID']}
                eventsForArticle.append(eachEvent)

    # ---------- End of Article Events ---------
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

    return flask.render_template('articleDashboard.html', article_detail=article, events=eventsForArticle,
                                 cambiaEventData=cambiaEvent,
                                 crossrefeventdatamain=crossrefevent,
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
