#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
from tornado import web
from tornado.web import asynchronous
from tornado import websocket
from tornado import gen
from . import BaseHandler#, sendMail#, _sql
from . import db_zoo, db_bz
import json
import datetime
import smtplib
import hashlib
import time

import os
cwd = os.getcwd()
print(cwd)

from handlers.app.celerytasks import bolidozor_db


class base(BaseHandler):
    def get(self):
        self.render('app.classification.hbs')



class get_meteor(BaseHandler):
    #@asynchronous
    @gen.coroutine
    def get(self):
        out = bolidozor_db.delay('''
                SELECT 
                    bolidozor_met.id AS id,
                    file AS file,
                    bolidozor_met.obstime AS obstime,
                    noise,
                    peak_f,
                    mag,
                    duration,
                    filename,
                    id_observer,
                    id_server,
                    filepath,
                    id_zoo_user as zoo_user,
                    headecho as zoo_headecho,
                    tail as zoo_tail,
                    datetime as zoo_datetime
                FROM
                    MLABvo.bolidozor_met
                        INNER JOIN
                    bolidozor_fileindex ON bolidozor_met.file = bolidozor_fileindex.id
                        LEFT JOIN
                    zoo_classification ON bolidozor_met.id = zoo_classification.id_met
                WHERE
                    (duration > 1)
                    AND
                    (bolidozor_met.obstime BETWEEN '2018-06-10 00:00:00' AND '2018-06-11 00:00:00')
                ORDER BY bolidozor_met.id DESC LIMIT 10;
            ''')
        print(out)
        print(out.ready())
        while not out.ready():
            print("cekam..")
            yield gen.sleep(0.25)
            #yield gen.moment

        print(out.get())
        self.write(repr(out.get()))
        self.finish()
