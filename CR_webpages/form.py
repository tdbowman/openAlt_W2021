# You must search exactly for a doi like this one
# 10.1016/j.ymthe.2019.04.002
from flask import Flask, request, render_template  
import json
from crossref.restful import Works
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
      x = works.doi(search)
      if (x['author']):
         authorList = x['author']
         # Truncated example of what the x (json object) now looks like:
         # [{'given': 'Tushar H.', 'family': 'Ganjawala', 'sequence': 'first', 'affiliation': []}, {'given': 'Qi', 'family': 'Lu', 'sequence': 'additional', 'affiliation': []}]
         templist = []
         for index, authorDetail in enumerate(authorList):
            templist.append(authorDetail['given'])
            templist.append(authorDetail['family'])
      #return str(templist)
   return render_template('cross_ref.html', authorList=str(templist))
  
if __name__=='__main__': 
   app.run() 
