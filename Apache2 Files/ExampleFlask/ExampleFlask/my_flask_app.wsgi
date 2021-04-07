#!/usr/bin/python

import sys

sys.path.insert(0, '/ExampleFlask/ExampleFlask/')

from my_flask_app import app as application
application.secret_key = 'hello'
