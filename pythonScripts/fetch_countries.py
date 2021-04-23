# Author: Rihat Rahman
# Lines: 1 - 60
# This script will run with the CRON job to get an updated list of countries and store them in a CSV file.
# The list of countries in search results home page will load from this script.

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


import requests
import csv
from progress.bar import IncrementalBar

try:
    APIResult = requests.get('https://restcountries.eu/rest/v2/all')

    countries = APIResult.json()

    list_of_countries = []

    for country in countries:
        list_of_countries.append(country['name'])

    bar = IncrementalBar('Listing countries in CSV file', max=len(list_of_countries))

    if list_of_countries != []:

        with open('test\\data.csv', mode = 'w', newline = "") as country_file:

            csv_writer = csv.writer(country_file)

            for country in list_of_countries:
                csv_writer.writerow([country])
                bar.next()

            bar.finish()

except:
    print("Error Occurred while calling REST Countries API")