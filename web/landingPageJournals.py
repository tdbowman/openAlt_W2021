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
#import flask
import flask

#define function to retrieve the total number of journals in the database 
def landingPageJournals(mysql):
    #global mysql
    cursor = mysql.connection.cursor()

    #string to query the database to sum up all journals from _main_ table
    totalSumQuery="SELECT (SELECT COUNT( DISTINCT container_title) FROM doidata._main_ ) AS sumCountJournal"

    #execute string's query using cursor 
    cursor.execute(totalSumQuery)

    #commit
    mysql.connection.commit()
    
    #fetch result
    totalSumJournals = cursor.fetchone()

    #close cursor
    cursor.close()
    
    #return result fetched from dictionary
    return (totalSumJournals['sumCountJournal'])

