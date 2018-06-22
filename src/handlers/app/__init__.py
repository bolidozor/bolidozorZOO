#!/usr/bin/python
# -*- coding: utf-8 -*-

# tento soubor ma link ve slozce ./plugins
# original je umisten ve slozce ./handlers

import tornado
import tornado.web
#import pymongo
import hashlib, uuid
import functools
#import bson

import pymysql.cursors
import MySQLdb as mdb

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):


        #self.db_zoo = pymysql.connect(host="localhost", user="root", passwd="root", db='BolidozorZoo', use_unicode=True, charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        #self.db_bz = pymysql.connect(host="localhost", user="root", passwd="root", db='BolidozorZoo', use_unicode=True, charset="utf8", cursorclass=pymysql.cursors.DictCursor)

        login = self.get_secure_cookie("user")
        #if login:
        #    login = str(login, encoding="utf-8")
        #    out = db_zoo("SELECT * FROM BolidozorZoo.user WHERE email = '{}'".format(login) )[0]
        #    print("LOGIN", out)

        '''
        if login and user_db.get('user', False) == login:
            self.actual_user = user_db
            self.role = set(user_db['role'])
            
            print("prava uzivatele \t", self.role)
            print ("Uzivatel je prihlasen", login)

            self.logged = True
            return None
        

        else:
        '''
        #print ("uzivatel neni korektne prihlasen")
        #self.logged = False
        return None


    def get_current_user(self):
        login = self.get_secure_cookie("user", None)
        if not login:
            return None
        login = db_zoo("SELECT * FROM BolidozorZoo.user WHERE email = '{}';".format(login.decode("utf-8")))
        print(login)
        self.actual_user = login[0]
        return login[0]
      

    def authorized(self, required = [], sudo = True):
        print("AUTHORIZED.....")
        if self.get_current_user():
            if sudo:
                required = required + ['sudo']
            req = set(required)
            intersection = list(self.role&req)
            if  bool(intersection):
                return intersection
            else:
                print("Go To ERRRRRR")
                self.redirect('/?err=authorized')
        else:
            self.redirect('/login')






class home(BaseHandler):
    def get(self, param=None):
        self.write("Ahoj :) ")


def db_zoo(query, read = False):
    return _sql(query, read = read, db = 'BolidozorZoo')

def db_bz(query, read = False):
    return _sql(query, read = read, db = 'MLABvo')

def _sql(query, read=False, db="MLABvo"):
        #print "#>", query
        connection = pymysql.connect(host="localhost", user="root", passwd="root", db=db, use_unicode=True, charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        try:
            cursorobj = connection.cursor()
            result = None
            cursorobj.execute(query)
            result = cursorobj.fetchall()
            if not read:
                connection.commit()
        except Exception as e:
            print("Err", e)
            return e
        connection.close()
        return result
