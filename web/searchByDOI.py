import csv
import pandas
import logging
import flask
from flask import send_file

from uploadDOI import downloadDOI

def searchByDOI(mysql, fileName):
    
    cursor = mysql.connection.cursor()

    #directory of doi list
    #CHANGE DIRECTORY TO YOUR DOI LIST CSV
    dir = '../web/uploadFiles/' + fileName
   
    return flask.render_template('download.html')

    return send_file('../web/downloadFiles/' + fileName, as_attachment=True)



