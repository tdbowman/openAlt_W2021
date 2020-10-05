from cr_search_db import get_articles, get_authors_for_article

'''
Call get_articles function in cr_search_db.py: it queries from the database,
and returns a list of articles in Dataframe (pandas)
Returns of articles

TBD: 
For each article, need to get list of authors (commented out at Line 15)
'''
def get_article_search(searchby, search):

    article_df = get_articles(searchby, search) #Dataframe
    article_list = article_df.values.tolist() #convert dataframe into a python list


    '''
    article_list = []
    for article in result:
        author_list = get_authors_for_article(article[0])
        article.append(author_list)
        print('author_list', author_list)
        article_list = article_list.append(article)
    '''

    print('article list size', len(article_list))
    return article_list #return python list

