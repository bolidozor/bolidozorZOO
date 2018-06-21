#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
from tornado import web
from tornado import websocket
from . import BaseHandler#, sendMail#, _sql
from . import db_zoo, db_bz
import json
import datetime
import smtplib
import hashlib



#from requests_oauthlib import OAuth2Session

class login(BaseHandler):
    def get(self):
        self.redirect('/')

    def post(self):
        out = db_zoo("SELECT * FROM BolidozorZoo.user WHERE email = '{}'".format(self.get_argument('name')) )[0]
        lpass = hashlib.sha512((self.get_argument('password')+self.get_argument('name')).encode('utf-8')).hexdigest()
        if lpass == out['password']:
            print("OK")
            self.set_secure_cookie("user", self.get_argument("name"))
            self.render("home.hbs", title="Bolidozor", user = self.get_argument("name"), login_msg = '1')
            #self.redirect("/")
        else:
            print("BAD PASS")
            self.redirect("/?login_msg=2")

class logout(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/?login_msg=3")
 
class registration(BaseHandler):
    def get(self):
        self.render('auth.registration.hbs', alert = None)

    def post(self):
        uname = self.get_argument('name')
        uuser = self.get_argument('email')
        upass = hashlib.sha512((self.get_argument('password')+uuser).encode('utf-8')).hexdigest()
        print(uname, uuser, upass)

        query = "INSERT INTO `BolidozorZoo`.`user` (`username`, `email`, `password`, `created`, `name`) VALUES ('{}', '{}', '{}', UTC_TIMESTAMP(), '{}');".format(uuser, uuser, upass, uname)
        out = db_zoo(query)
        print(out)

        self.redirect('/')
        #self.write('registration done')


