# Author: Tabish
import flask
from flask import Flask
from flask import send_file
from flask_mysqldb import MySQL
from flask import request, jsonify, redirect, flash
import json
import os

def editconfigfile():
    # current directory
    path = os.getcwd()
    # parent directory
    parent = os.path.dirname(path)
    config_path = os.path.join(parent, "config", "openAltConfig.json")
    # config file
    f = open(config_path)
    APP_CONFIG = json.load(f)

    #for i in APP_CONFIG:
        #print(i)
        #for key,value in APP_CONFIG[i].items():
            #print(str(key) + " = " + str(value))
        #print("\n")
    #os.system("start " + config_path)
    return flask.render_template('adminChooseUpdate.html')

if __name__=="__main__":
    editconfigfile()
