#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import jinja2
import gettext

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
        
    def index(self, **args):	
    	#return "run here "
        try:
        	return jjenv.get_template('dbviewer.html').render(title="index", **args)
        except Exception, e:
        	return e 
        #return 
    def temp(self,**args):
    	try:
    		pass
    	except Exception, e:
    	   web.notfound()
    		