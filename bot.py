#!/usr/bin/env python
# -*- coding: utf-8 -*-


import web
from google.appengine.api.xmpp import *

class XmppHandler(xmpp_handlers.CommandHandler):
    """Handler class for all XMPP activity."""

    def text_message(self, message=None):
        self.help_command(message=message)   

    def help_command(self, message=None):
        """
        */help*
        show usage.  """
        rstr = "/help*        show usage.  \n"    
        message.reply(rstr)
    
    def version_command(self, message=None):
        """
        */version*
        show version number.  """
        message.reply("tw-bot Version: %s")


urls = (
  '/(.*)', 'XmppHandler',)
application = web.application(urls, globals())
app = application.wsgifunc()
