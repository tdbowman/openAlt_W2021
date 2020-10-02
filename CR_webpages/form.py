# You must search exactly for a doi like this one
# 10.1016/j.ymthe.2019.04.002
from flask import Flask, request, render_template  
import json
from crossref.restful import Works
import connect_mysql
from pandas import DataFrame

works = Works()


# Flask constructor 
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def cr_home():
   return render_template('crossRefhome.html')


@app.route('/cr_search', methods =["GET", "POST"])
def cr_search():
   print ( 'Hi I am in cr_search')
   if request.method == "POST": 
      search = str(request.form.get("search"))
      print(search)
      input = str(request.form.get("inputChoice"))
      print(input)
      x = works.doi(search)
      if (x['author']):
         authorList = x['author']
         # Truncated example of what the x (json object) now looks like:
         # [{'given': 'Tushar H.', 'family': 'Ganjawala', 'sequence': 'first', 'affiliation': []}, {'given': 'Qi', 'family': 'Lu', 'sequence': 'additional', 'affiliation': []}]
         templist = []
         for index, authorDetail in enumerate(authorList):
            templist.append(authorDetail['given'])
            templist.append(authorDetail['family'])


         #print(article_df)

      if (input == '1'):
            article_df = connect_mysql.get_articles()
            article_list = []
            for row in article_df.index:
               print( '----3->', article_df.loc[row][3])
               #article_list[row][1] = article_df.loc[row][3]
               print('--5--->', article_df.loc[row][5])
               #article_list[row][2] = article_df.loc[row][5]
               print('--4--->', article_df.loc[row][4])
               #article_list[row][3] = article_df.loc[row][4]

               article_list = article_df.values.tolist()
               print (article_list)

            return render_template('cross_ref_DOIsearch.html', article_list=article_list)
      if (input=='2'):
            return render_template('cross_ref.html', authorList=str(templist))
      if (input=='3'):
            return render_template('cross_ref.html', authorList=str(templist))

   #return render_template('cross_ref.html', authorList=str(templist))
  
if __name__=='__main__': 
   app.run() 
