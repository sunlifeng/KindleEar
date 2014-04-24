#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import jinja2
import gettext
from books import BookClasses, BookClass
from model import *
from BaseHandler import BaseHandler




class Help(BaseHandler):
   
    
    def index(self, **args):
        return web.input()
        try:


            return self.render('dbviewer.html','index',books=Book.all(),users=KeUser.all(),
            feeds=Feed.all().order('book'),current='Help', **args)
            
        except Exception, e:
            return web.notfound() 
        
    def temp(self,**args):
    	try:
           books=BookClasses()
    	   return  self.render("help.html",'temp',books=books,**args)
    	except Exception, e:
    	   web.notfound()
    		