# author: Rihat Rahman
# This script extracts university information from affiliation data
# returns name of university
# returns None of university information doesn't exist

import pandas as pd


def extract_university(affiliation):

    df = pd.read_csv('world-universities.csv')

    affiliation_attributes = affiliation.split(",")

    for attribute in affiliation_attributes:

        for index, row in df.iterrows():

            university = (index, row['university_name'])
            university_name = university[1]

            if attribute.strip().upper() == university_name.strip().upper():
                return university_name

    return None