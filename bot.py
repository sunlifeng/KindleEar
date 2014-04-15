#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import web_controller
hendler = web_controller.Handler()

urls = (
   "/(.*)", "Gear",
)
class Gear:
    def GET(self, args = False):
        return "hello world"
        return hendler.control(args)
    def POST(self,args=False):
        return hendler.control(args)


application = web.application(urls, globals())
appbot = application.wsgifunc()       