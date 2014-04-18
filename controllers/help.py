#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import jinja2
import gettext
from books import BookClasses, BookClass
from model import *

jjenv = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                            extensions=["jinja2.ext.do",'jinja2.ext.i18n'])
#session = web.session.Session(application, store, initializer={'username':'','login':0,"lang":''})

def set_lang(lang):
    """ 设置网页显示语言 """
    tr = gettext.translation('lang', 'i18n', languages=[lang])
    tr.install(True)
    jjenv.install_gettext_translations(tr)

class Help:
    
    def __init__(self):
        set_lang("zh-cn")
    def render(self, templatefile, title='KindleEar', **kwargs):        
        try:
            return jjenv.get_template(templatefile).render(title=title, **kwargs)
        except Exception, e:
            return e        
    
    def index(self, **args):	
    	#return "run here "
        try:

        	return jjenv.get_template('dbviewer.html').render(title="index", 
                **args)
        except Exception, e:
        	return e 
        
    def temp(self,**args):
    	try:
           books=BookClasses()
    	   return  self.render("help.html",'temp',books=books)
    	except Exception, e:
    	   web.notfound()
    		