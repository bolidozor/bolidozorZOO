#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado
#from tornado import web
from tornado import ioloop
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web
import json
#import sqlite3
import MySQLdb as mdb
import time
import os


#from handlers import rtmap, count, multibolid, auth, admin, stations, around, timeline
from handlers import admin, auth
from handlers.app import multimeteor, classification
from handlers import _sql, BaseHandler


def wwwCleanName(string):
    return ''.join( c for c in string if c not in '?:!/;-_#$%^!@., (){}[]' )


class HomePage(BaseHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print("web", addres)
        login_msg = self.get_argument('login_msg', None)
        self.render("home.hbs", title="Bolidozor", user=self.get_secure_cookie("login"), login_msg = login_msg)

class ClientsHandler(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        #print cl
        self.render("index.html")


tornado.options.define("port", default=8881, help="port", type=int)
tornado.options.define("debug", default=True, help="debug mode")
tornado.options.parse_config_file("/home/roman/BolidozorZOO.conf")

class WebApp(tornado.web.Application):

    def __init__(self, config={}):

        name = 'BolidozorZOO'
        server = 'rtbolidozor.cz'

        server_url = '{}:{}'.format(server, tornado.options.options.port)
        print(server_url)

        handlers =[
            (r'/', HomePage),
            (r'/aa/', classification.get_meteor),

            #(r'/login/oauth/github', auth.),
            (r'/login', auth.login),
            (r'/logout', auth.logout),
            #(r'/login', auth.login),
            #(r'/logout/', auth.logout),
            #(r'/logout', auth.logout),
            (r'/newuser', auth.registration),

            (r'/app/multimeteor', multimeteor.base),
            (r'/app/classification', classification.base),

            (r'/(favicon.ico)', web.StaticFileHandler, {'path': '.'}),
            (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
            (r"/(robots.txt)", tornado.web.StaticFileHandler, {'path': './static/'}),
            (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
            (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
            (r"/(.*\.css)", tornado.web.StaticFileHandler,{"path": './www/css/' }),
            (r"/(.*\.wav)", tornado.web.StaticFileHandler,{"path": './www/wav/' }),
           #(r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
            (r"/(.*)", HomePage),
        ]
        settings = dict(
            cookie_secret="ROT13IrehaxnWrArwyrcfvQvixnAnFirgr",
            template_path= "templates/",
            static_path= "static/",
            #xsrf_cookies=True,
            xsrf_cookies=False,
            name="RTbolidozor",
            server_url="rtbolidozor.astro.cz",
            site_title="RTbolidozor",
            login_url="/login",
            #ui_modules=modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
            autoreload=True
        )

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebApp())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
