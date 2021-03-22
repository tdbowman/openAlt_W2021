# Try to read the users MySQL password from a file.
# This passwd.txt file is in the .gitignore
# If the password cannot be read, print error message and exit.

import sys

SITE_KEY = ''
SECRET_KEY = ''

def getPassword():
    try:
        with open("./passwd.txt") as passwd:
            mysql_password = passwd.readline()
        mysql_password = str(mysql_password)
        return mysql_password
    except:
        print("ERROR - MISSING passwd.txt file in this directory.\nCreate passwd.txt with just your password in it.")
        sys.exit()
