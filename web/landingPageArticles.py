#import flask
import flask

#define function to retrieve the total number of artciles in the database
def landingPageArticles(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    #string to query the database to sum up all articles from the _main_ table
    totalSumQuery="SELECT (SELECT COUNT(DISTINCT DOI) FROM doidata._main_ ) AS sumCountArticle"
    
    #execute string's query using cursor
    cursor.execute(totalSumQuery)
    
    #commit
    mysql.connection.commit()
    
    #fetch result
    totalSumArticles = cursor.fetchone()

    #close cursor
    cursor.close()
    
    #return result fetched from the dictionary
    return (totalSumArticles['sumCountArticle'])
    