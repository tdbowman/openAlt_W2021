# author: Rihat Rahman
# This script extracts country information from affiliation data (may contain country or state name) 
# and returns country name.
# returns None if country infromation doesn't exist
# date: February 6, 2021

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


        elif "USA" in location.upper():
            return "United States"


        elif "UK" in location.upper():

            if "Ukraine" in location.upper():
                return "Ukraine"

            else:
                return "United Kingdom"


        elif "UAE" in location.upper():
            return "United Arab Emirates"


        elif "BRASIL" in location.upper():
            return "Brazil"


    states = us.states.STATES

    # check by US states
    for state in states:

        if any ([str(state.name) in location, location == str(state.abbr)]):
            return 'United States'

        if (len(location) >= 3):
            if (location[0:2] == str(state.abbr)) & ((location[2] == " ") | (location[2] == "-") | (location[2].isdigit())):
                return 'United States'

    return None