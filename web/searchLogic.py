import flask
from datetime import datetime

def searchLogic(mysql):
    #global mysql
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
