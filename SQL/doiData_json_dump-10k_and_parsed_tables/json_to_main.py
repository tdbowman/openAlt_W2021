import sys
import pprint
import json
#import 
import time
import datetime
from collections import OrderedDict 
import traceback


import mysql.connector
from mysql.connector import errors
from _db import db #keep keys in separate file, keys.py

##### DB CREDENTIALS #####
HOST = db['host']
USER = db['user']
PASSWD = db['pword']
DATABASE = db['schema']
TABLE = db['table']
##########################


def db_connect():
    try:
        db = mysql.connector.connect(user=USER, password=PASSWD,host=HOST,database=DATABASE,use_unicode=True,charset='utf8')
        db.autocommit = False
    except Exception as e:
        sys.exit("Can't connect to MySQL database")
    return db


"""
    # 46=7 columns in table
    _insert_query = f"INSERT IGNORE INTO `{DATABASE}`.`_main_` (`DOI`, `URL`, `abstract`, `alternative_id`, `archive`, `article_number`, `container_title`, `created_date_parts`, `created_date_time`, `created_timestamp`, `deposited_date_parts`, `deposited_date_time`, `deposited_timestamp`, `fk`, `indexed_date_parts`, `indexed_date_time`, `indexed_timestamp`, `is_referenced_by_count`, `issue`, `issued`,  `issued_date_parts`, `issued_date_time`, `issued_timestamp`,  `language`, `member`, `original_title`, `page`, `prefix`, `published_online_date_parts`, `published_online_date_time`, `published_online_timestamp`, `published_print_date_parts`, `published_print_date_time`, `published_print_timestamp`, `publisher`, `publisher_location`, `reference_count`, `references_count`, `score`, `short_container_title`, `short_title`, `source`, `subtitle`, `title`, `type`, `update_policy`, `volume`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
"""
def insert_bulk(_values, _fks, _query):

    if _values is None or _query is None or _fks is None:
        return False   


    _db = db_connect()
    _cursor = _db.cursor(prepared=True)
    _cursor.execute('SET NAMES utf8mb4')
    _cursor.execute("SET CHARACTER SET utf8mb4")
    _cursor.execute("SET character_set_connection=utf8mb4")
    _cursor.execute("SET @@session.time_zone='+00:00';")

    try:
        _db.ping(True)
        _cursor.executemany(_query, _values)
        _db.commit()

    except mysql.connector.Error as err:
        traceback.print_exc()
        #error ocurs,rollback
        _db.rollback()    

        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
        sys.exit("STOPPED")



    try:
        _db.ping(True)
        _fk_query = f"UPDATE `{DATABASE}`.`_json` SET flag=1 WHERE `id`=?;"
        _cursor.executemany(_fk_query, _fks)
        _db.commit()

    except mysql.connector.Error as err:
        traceback.print_exc()
        #error ocurs,rollback
        _db.rollback()    

        print(err)
        print("FKs Error Code:", err.errno)
        print("FKs SQLSTATE", err.sqlstate)
        print("FKs Message", err.msg)
        sys.exit("STOPPED")





def key_exists(_k, _d):

    if _k in _d:
        return _d[_k]
    else:
        return None

def primary_keyVals(d):
    _obj = dict()

    for k, v in d.items():

        #datetime columns
        if k == 'created':
            if 'date-time' in v:
                _obj['created-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['created-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['created-timestamp'] = v['timestamp']

        elif k == 'indexed':
            if 'date-time' in v:
                _obj['indexed-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['indexed-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['indexed-timestamp'] = v['timestamp']


        elif k == 'deposited':
            if 'date-time' in v:
                _obj['deposited-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['deposited-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['deposited-timestamp'] = v['timestamp']


        elif k == 'published-print':
            if 'date-time' in v:
                _obj['published-print-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['published-print-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['published-print-timestamp'] = v['timestamp']                

        elif k == 'published-online':
            if 'date-time' in v:
                _obj['published-online-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['published-online-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['published-online-timestamp'] = v['timestamp']     

        elif k == 'issued':
            if 'date-time' in v:
                _obj['issued-date-time'] = datetime.datetime.fromisoformat(v['date-time'].replace('Z', '+00:00'))

            if 'date-parts' in v:
                for x in v['date-parts']:
                    if isinstance(x, list):
                        _separator = '/'.join(str(v) for v in x)

                _obj['issued-date-parts'] = _separator

            if 'timestamp' in v:
                _obj['issued-timestamp'] = v['timestamp']    

        # other columns
        elif k == 'alternative-id':
            _list_length = len(v)
            if _list_length == 0:
                _obj['alternative-id'] = None
            elif _list_length == 1:
                _obj['alternative-id'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['alternative-id'] = _separator

        elif k == 'archive':
            _list_length = len(v)
            if _list_length == 0:
                _obj['archive'] = None
            elif _list_length == 1:
                _obj['archive'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['archive'] = _separator

        elif k == 'subtitle':
            _list_length = len(v)
            if _list_length == 0:
                _obj['subtitle'] = None
            elif _list_length == 1:
                _obj['subtitle'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['title'] = _separator

        elif k == 'title':
            _list_length = len(v)
            if _list_length == 0:
                _obj['title'] = None
            elif _list_length == 1:
                _obj['title'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['title'] = _separator

        elif k == 'original-title':
            _list_length = len(v)
            if _list_length == 0:
                _obj['original-title'] = None
            elif _list_length == 1:
                _obj['original-title'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['original-title'] = _separator

        elif k == 'container-title':
            _list_length = len(v)
            if _list_length == 0:
                _obj['container-title'] = None
            elif _list_length == 1:
                _obj['container-title'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['container-title'] = _separator                


        elif k == 'short-title':
            _list_length = len(v)
            if _list_length == 0:
                _obj['short-title'] = None
            elif _list_length == 1:
                _obj['short-title'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['short-title'] = _separator     

        elif k == 'short-container-title':
            _list_length = len(v)
            if _list_length == 0:
                _obj['short-container-title'] = None
            elif _list_length == 1:
                _obj['short-container-title'] = v[0]
            else:
                _separator = ' | '.join(str(x) for x in v)
                _obj['short-container-title'] = _separator        

        elif isinstance(v, list):
            pass
        elif isinstance(v,dict):
            pass
        else:
            _obj[k] = v

    dict1 = OrderedDict(sorted(_obj.items())) 
    return dict(dict1)

def notKey(dict, key): 
    if key not in dict.keys(): 
        return True 
    else: 
        return False

## Insert work into MySQL ##
def store_work(_data, _fk):

    # check for missing data and set to NULL
    if _fk is None:
        return False      

    if _data is not None:

        #47 columns
        _defaults = ['DOI', 'URL', 'abstract', 'alternative-id', 'archive', 'article-number', 'container-title', 'created-date-time', 'created-date-parts', 'created-timestamp', 'deposited-date-time', 'deposited-date-parts', 'deposited-timestamp',  'fk', 'indexed-date-time', 'indexed-date-parts', 'indexed-timestamp', 'is-referenced-by-count', 'issue', 'issued', 'issued-date-time', 'issued-date-parts', 'issued-timestamp', 'language', 'member', 'original-title', 'page', 'prefix', 'published-online-date-time', 'published-online-date-parts', 'published-online-timestamp', 'published-print-date-time', 'published-print-date-parts', 'published-print-timestamp', 'publisher', 'publisher-location',  'reference-count', 'references-count', 'score', 'short-container-title', 'short-title', 'source', 'subtitle', 'title', 'type', 'update-policy', 'volume']
        
        _data = primary_keyVals(_data)
        _data['fk'] = _fk

        if not set(_defaults).issubset(_data):
            for key in _defaults:
                if notKey(_data, key):
                    _data[key] = None
                elif key == 'score':
                    _data[key] = float(_data[key])
                elif key == 'is-referenced-by-count':
                    _data[key] = int(_data[key])
                elif key == 'reference-count':
                    _data[key] = int(_data[key])
                elif key == 'references-count':
                    _data[key] = int(_data[key])
                else:
                    _data[key] = str(_data[key])


        _data = OrderedDict(sorted(_data.items()))
        _values = list(_data.values())

    else:
        _values = [None,None,None,None,None,None,None,None,None,None,None,None,None,_fk,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


    return _values



######################################################################
if __name__ == "__main__": 

    start_time = time.time()


    # PrettyPrint
    pp = pprint.PrettyPrinter(indent=4)

    # Connect to MySQL
    cnx = mysql.connector.connect(user=USER, password=PASSWD,host=HOST,database=DATABASE,use_unicode=True,charset='utf8')

    cursor = cnx.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute("SET CHARACTER SET utf8mb4;")
    cursor.execute("SET character_set_connection=utf8mb4;")
    cursor.execute("SET @@session.time_zone='+00:00';")

    # get count
    cursor.execute(f"SELECT count(*) FROM `{DATABASE}`.`{TABLE}` WHERE `flag` IS NULL;")
    count = cursor.fetchone()[0]

    ##
    batch_size = 1000 # how many at the same time

    print(f"{count} total records")

    _bucket = list()
    _fks = list()

    for offset in range(0, count, batch_size):
        
        cursor.execute(f"SELECT `id`, `json` FROM `{DATABASE}`.`_json` WHERE `flag` IS NULL LIMIT %s OFFSET %s", (batch_size, offset))
        for row in cursor:
            _fk = row[0]
            _json = row[1]
            _myjson = None
            
            try:
                _myjson = json.loads(_json)
            except ValueError as err:
                print(f"VALUE ERROR: {err} for {_fk}")
                _myjson = None
            except KeyError as err:
                print(f"KEY ERROR: {err} for {_fk}")
                _myjson = None
            except TypeError as err:
                print(f"TYPE ERROR: {err} for {_fk}")
                _myjson = None

            _bucket.append(store_work(_myjson, _fk))
            _fks.append((_fk,))

        #47 columns
        _insert_query = f"INSERT IGNORE INTO `{DATABASE}`.`_main_` (`DOI`, `URL`, `abstract`, `alternative_id`, `archive`, `article_number`, `container_title`, `created_date_parts`, `created_date_time`, `created_timestamp`, `deposited_date_parts`, `deposited_date_time`, `deposited_timestamp`, `fk`, `indexed_date_parts`, `indexed_date_time`, `indexed_timestamp`, `is_referenced_by_count`, `issue`, `issued`,  `issued_date_parts`, `issued_date_time`, `issued_timestamp`,  `language`, `member`, `original_title`, `page`, `prefix`, `published_online_date_parts`, `published_online_date_time`, `published_online_timestamp`, `published_print_date_parts`, `published_print_date_time`, `published_print_timestamp`, `publisher`, `publisher_location`, `reference_count`, `references_count`, `score`, `short_container_title`, `short_title`, `source`, `subtitle`, `title`, `type`, `update_policy`, `volume`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"


        #pp.pprint(_bucket)
        insert_bulk(_bucket, _fks, _insert_query)


    cursor.close()
    cnx.close()
    print("--- %s seconds ---" % (time.time() - start_time))

    #50 batch size for 5000 => --- 2.1230015754699707 seconds ---
    #1000 batch size for 5000 => 
