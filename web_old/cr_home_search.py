# You must search exactly for a doi like this one
# 10.1016/j.ymthe.2019.04.002
from flask import Flask, request, render_template  
import json
from crossref.restful import Works
from cr_search_process import get_article_search
from pandas import DataFrame

works = Works()


# Flask constructor 
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def cr_home():
   return render_template('crossRefhome.html')

'''
Service for search button
request input: "search" (text entered by user) and "searchby" (dropdown box)
'''
@app.route('/cr_search', methods =["GET", "POST"])
def cr_search():
   print ( 'Hi I am in cr_search')

   if request.method == "POST":
       #get form items
      search = str(request.form.get("search"))
      print(search)
      searchby = str(request.form.get("dropdownSearchBy"))
      print(searchby)

      #call get_article_search in cr_search_process.py
      article_list = get_article_search(searchby, search)

      '''
      x = works.doi(search)
      if (x['author']):
         authorList = x['author']
         # Truncated example of what the x (json object) now looks like:
         # [{'given': 'Tushar H.', 'family': 'Ganjawala', 'sequence': 'first', 'affiliation': []}, {'given': 'Qi', 'family': 'Lu', 'sequence': 'additional', 'affiliation': []}]
         templist = []
         for index, authorDetail in enumerate(authorList):
            templist.append(authorDetail['given'])
            templist.append(authorDetail['family'])
     '''

      #render article list to cr_search_results.html page
      return render_template('cr_search_result.html', article_list=article_list)

'''
Service for article title link in Search Results page, that leads to article dashboard page
'''
@app.route('/cr_article', methods =["GET", "POST"])
def cr_article():
   print('Hi I am in cr_article')
   #TBD: call process and database, get details about article for article dashboard

   #render the result to Article Dashboard page
   #return render_template('cr_article.html', article list_sourceref) -- this list includes references from all source tables
   return render_template('cr_article.html')

'''
Service for author name link in Search Results page, that leads to author dashboard page
'''
@app.route('/cr_author', methods =["GET", "POST"])
def cr_author():
   print('Hi I am in cr_author')
   #TBD: call process and database, get details about author for author dashboard

   # render the result to Author Dashboard page
   # return render_template('cr_author.html', author list_sourceref) -- this list includes references from all source tables
   return render_template('cr_author.html')

'''
Service for journal name link in Search Results page, that leads to journal dashboard page
'''
@app.route('/cr_journal', methods =["GET", "POST"])
def cr_journal():
   print('Hi I am in cr_journal')
   #TBD: call process and database, get details about journal for journal dashboard

   # render the result to Journal Dashboard page
   # return render_template('cr_journal.html', journal list_sourceref) -- this list includes references from all source tables
   return render_template('cr_journal.html')

if __name__=='__main__': 
   app.run() 
