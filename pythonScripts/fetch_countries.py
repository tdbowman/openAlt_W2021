# Author: Rihat Rahman
# Lines: 1 - 27
# This script will run with the CRON job to get an updated list of countries and store them in a CSV file.
# The list of countries in search results home page will load from this script.

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