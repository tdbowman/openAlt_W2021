import mysql.connector


'''
Get connection from SQL database
'''
def sql_connect():
    cnx = mysql.connector.connect(user='root', password='****',
                              host='127.0.0.1',
                              database='crossrefeventdata')
    return cnx

