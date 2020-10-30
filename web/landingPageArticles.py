import flask

def landingPageArticles(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    totalSumQuery="SELECT (SELECT COUNT(DISTINCT DOI) FROM dr_bowman_doi_data_tables._main_ ) AS sumCountArticle"

    cursor.execute(totalSumQuery)
    mysql.connection.commit()
    totalSumArticles = cursor.fetchone()

    print(totalSumArticles)

    cursor.close()
    return (totalSumArticles['sumCountArticle'])
    