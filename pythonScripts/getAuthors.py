"""
MIT License

Copyright (c) 2020 tdbowman-CompSci-F2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Pass this script a DOI and recieve a list of authors
# python getAuthors.py 10.1016/j.ymthe.2019.04.002
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("doi")
args = parser.parse_args()

try:
    from crossref.restful import Works
    works = Works()
    print ("Working...")
    # Request data from the crossref API, save json as x
    x = works.doi(args.doi)
    if (x['author']):
        authorList = x['author']
        for index, authorDetail in enumerate(authorList):
            first_name = authorDetail['given']
            last_name = authorDetail['family']
            print(first_name + ' ' + last_name)
            
except ImportError:
    print("You need to install the crossref api with 'pip install crossrefapi' first")
except:
    print("Unspecified error, exiting")
