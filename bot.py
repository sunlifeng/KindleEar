#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import webapp2
from google.appengine.api import xmpp

class XMPPHandler(webapp2.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == 'hello':
            message.reply("Greetings!")
    def get(self):
        return "hello world"



app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)