import mysql.connector
from pandas import DataFrame

def sql_connect():
    cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='crossrefeventdata')
    return cnx


def get_articles():
    print ( "In get_articles ---------------------")
    cnx = sql_connect()
    print("Got SQl connection ---------------------")
    cursor = cnx.cursor()
    query = ("SELECT objectID, uniqueEventID, articleID, articleTitle, "
             + "journalName, articleDate, articleURL "
             + "FROM main ")

    cursor.execute(query)


    article_df = DataFrame(cursor.fetchall())
    #print ( " Article df " , article_df)
    #print ( ' ****************************')
    '''
    for article in cursor:
        print(article[0])
        print(article[1])
        print(article[2])
        print(article[3])
        print(article[4])
        print('-----------------')
    '''
    cursor.close()
    cnx.close()
    return article_df
