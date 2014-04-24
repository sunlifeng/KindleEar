#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
#import jinja2
#import gettext
from books import BookClasses, BookClass
from model import *
from BaseHandler import BaseHandler,login_required


class Help(BaseHandler):
    def __init__(self):
        #super(BaseHandler,self).__init__()
        super(Help, self).__init__() 
        #self.singleton=Singleton()
        #self.session=singleton.session
    #@login_required      
    def index(self, **args):
        self.redirect(r"/")
        #return self.login_required()        
        try:
            #return dir(self)
            return self.render('dbviewer.html','index',books=Book.all(),users=KeUser.all(),
            feeds=Feed.all().order('book'),current='Help', **args)
            
        except Exception, e:
            return web.notfound() 
    @login_required      
    def temp(self,**args):
    	try:
           books=BookClasses()
    	   return  self.render("help.html",'temp',books=books,**args)
    	except Exception, e:
    	   web.notfound()
    		