# Pass this script a DOI and recieve a list of authors
# python getAuthors.py 10.1016/j.ymthe.2019.04.002
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("doi")
args = parser.parse_args()

#doi = '10.1016/j.ymthe.2019.04.002'

try:
    from crossref.restful import Works
    works = Works()
    print ("Working...")
    # Request data from the crossref API, save json as x
    x = works.doi(args.doi)
    if (x['author']):
        authorList = x['author']
        # Truncated example of what the x (json object) now looks like:
        # [{'given': 'Tushar H.', 'family': 'Ganjawala', 'sequence': 'first', 'affiliation': []}, {'given': 'Qi', 'family': 'Lu', 'sequence': 'additional', 'affiliation': []}]
        for index, authorDetail in enumerate(authorList):
            first_name = authorDetail['given']
            last_name = authorDetail['family']
            print(first_name + ' ' + last_name)
            
except ImportError:
    print("You need to install the crossref api with 'pip install crossrefapi' first")
except:
    print("Unspecified error, exiting")
