#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import web_controller
import webapp2
from google.appengine.api import xmpp



hendler = web_controller.Handler()

urls = (
   "/(.*)", "Gear",
)



class Gear:
    def GET(self, args = False):       
        return hendler.control(args)

    def POST(self,args=False):
        return hendler.control(args)

application = web.application(urls, globals())
appbot = application.wsgifunc()   

class XMPPHandler(webapp2.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == 'hello':
            message.reply("Greetings!")
    def get(self):
        return "hello world"



app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)


    