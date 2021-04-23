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

# This script extracts university information from affiliation data
# returns name of university
# returns empty string of university information doesn't exist
# author: Rihat Rahman
# Lines 1-52
#-------------------------------------------------------------

import pandas as pd

def extract_university(affiliation):

    df = pd.read_csv('pythonScripts/world-universities.csv')

    affiliation_attributes = affiliation.split(",")

    for attribute in affiliation_attributes:

        for index, row in df.iterrows():

            university = (index, row['university_name'])
            university_name = university[1]

            if attribute.strip().upper() in university_name.strip().upper():
                return university_name

    return ""
#-------------------------------------------------------------
