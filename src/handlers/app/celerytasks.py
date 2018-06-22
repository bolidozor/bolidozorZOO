#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import json

import MySQLdb as mdb
import pymysql.cursors

from celery.result import AsyncResult
from celery import Celery

app = Celery('jobs', backend='amqp', broker='amqp://zoo:zoo@localhost:5672/zoo')


#
###
# celery -A celerytasks worker --hostname=zoo@blackhole
###
#

@app.task
def bolidozor_db(query, read = False, db='MLABvo'):
    print("#>", query)
    time.sleep(3)
    result = None
    connection = pymysql.connect(host="localhost", user="root", passwd="root", db=db, use_unicode=True, charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    try:
        cursorobj = connection.cursor()
        cursorobj.execute(query)
        result = cursorobj.fetchall()
        if not read:
            connection.commit()
    except Exception as e:
            print("Err", e)
    connection.close()
    return result




if __name__ == '__main__':
	app.start()