#!/usr/bin/env python
# coding:utf-8

import tornado
from tornado import httpserver
from tornado.web import RequestHandler 
from tornado.options import define, options
import os
import os.path

define("port", default=7788, help="run on the given port", type=int)
define("ip", default="192.168.1.244", help="run on the given ip", type=str)

ssl_path = os.path.abspath("../../ssl/")

def gen_app(urls=None, settings=None):
    if not urls:
        urls=[]
    if not settings:
        settings={}
    return tornado.web.Application(urls, **settings)


def gen_server(app, ssl_option):
    if not app:
        return
    if not ssl_option:
        ssl_option={}
    return httpserver.HTTPServer(app, ssl_option)


class HelloHandler(RequestHandler):
    def get(self):
        print 'hello ..'
        self.write('Hello, body!')

class MainHandler(RequestHandler):
    def get(self):
        print 'main ..'
        self.write('Hello, body!')

if __name__ == "__main__":
    tornado.options.parse_command_line()

    '''
    urls = [
            (r"/hello", HelloHandler),
            (r"/", MainHandler),
        ]


    app = gen_app(urls)
    svr = gen_server(app, ssl)
    '''

    ssl = {
        "certfile": os.path.join(ssl_path, "server.crt"),
        "keyfile": os.path.join(ssl_path, "server.key"),
    } 
    settings = {
        }
    application = tornado.web.Application([
                        (r"/", MainHandler),
                        (r"/hello", HelloHandler),
                    ],
                    debug=True)
    server = httpserver.HTTPServer(application, ssl_options=ssl)
    server.listen(options.port)
    print('Server started at port %s' % options.port)
    tornado.ioloop.IOLoop.instance().start()
