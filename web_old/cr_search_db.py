from connect_mysql import sql_connect
from pandas import DataFrame

'''
Get articles by searchby (dropdown box) and search box text input
'''
def get_articles(searchby, search):

    doi_query = """SELECT objectID, articleTitle, journalName, articleDate FROM main WHERE main.objectID= '%s' """

    author_query = """SELECT objectID, articleTitle, journalName, articleDate, author.givenName, author.familyName FROM main INNER JOIN article_to_author ON main.autoArticleID=article_to_author.articleID INNER JOIN author ON article_to_author.authorID=author.authorID WHERE author.givenName= '%s' AND author.familyName='%s' """

    journal_query = """SELECT objectID, articleTitle, journalName, articleDate FROM main WHERE main.journalName like '%s' """

    article_query = """SELECT objectID, articleTitle, journalName, articleDate FROM main WHERE main.articleTitle like '%s' """

    cnx = sql_connect() #call connect function
    cursor = cnx.cursor() #create cursor

#execute search queries based on dropdown box selection
    if searchby =='doi':
        print(' DOI Query ')
        cursor.execute(doi_query % (search))

    if searchby == 'author':
        #search box input for author contains first & last name separated by a space
        #but in the database, they are two different columns so we have to split them
        name = search.split()
        print ( 'given name  : ', name[0])
        print('family  name  : ', name[1])
        print(' Author Query ')
        cursor.execute(author_query % (name[0], name[1]))

    if searchby == 'journal':
        search = '%' + search + '%'
        cursor.execute(journal_query % search)
        print(' Journal Query ')

    if searchby == 'article':
        search = '%'+search+'%'
        cursor.execute(article_query % search)
        print(' article Query ')

    #create dataframe out of the cursor result set
    article_df = DataFrame(cursor.fetchall())
    print(article_df)

    #close cursor and connection
    cursor.close()
    cnx.close()
    return article_df

'''
Get list of authors for a DOI
TBD
Need to modify the query
'''
def get_authors_for_article(doi):

    get_author_name_query = """SELECT  author.givenName, author.familyName FROM main INNER JOIN article_to_author ON main.autoArticleID=article_to_author.articleID INNER JOIN author ON article_to_author.authorID=author.authorID WHERE main.objectID = '%s' """
    cnx = sql_connect()
    cursor = cnx.cursor()
    cursor.execute(get_author_name_query % doi)
    author_df = DataFrame(cursor.fetchall())
    print ('author_df  ', author_df )
    cursor.close()
    cnx.close()
    return author_df

