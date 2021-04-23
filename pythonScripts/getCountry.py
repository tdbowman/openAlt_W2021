# This script extracts country information from affiliation data (may contain country or state name) 
# and returns country name.
# returns empty string if country infromation doesn't exist
# author: Rihat Rahman
# Lines 1-88
#-------------------------------------------------------------
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
from iso3166 import countries
import us

def extract_country(affiliation):

    affiliation_attributes = affiliation.split(",")
    location = affiliation_attributes[len(affiliation_attributes) - 1].strip()


    # check if country exists (country name)
    for country in countries:

        country_extended_name = country[0].split(",")
        country_name = country_extended_name[0]


        if country_name.upper() in location.upper():
            return country_name


        elif ("USA" in location.upper()) or ("United States" in location.upper()):
            return "United States of America"


        elif "UK" in location.upper():

            if "Ukraine" in location.upper():
                return "Ukraine"

            else:
                return "United Kingdom"


        elif "UAE" in location.upper():
            return "United Arab Emirates"


        elif "BRASIL" in location.upper():
            return "Brazil"


        elif "RUSSIA" in location.upper():
            return "Russia"


    states = us.states.STATES

    # check by US states
    for state in states:

        if any ([str(state.name) in location, location == str(state.abbr)]):
            return 'United States'

        if (len(location) >= 3):
            if (location[0:2] == str(state.abbr)) & ((location[2] == " ") | (location[2] == "-") | (location[2].isdigit())):
                return 'United States'

    return ""
#-------------------------------------------------------------