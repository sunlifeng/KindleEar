#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gettext
import web
import jinja2
from model import * 
from lib.helper import Singleton,singleton


jjenv = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                            extensions=["jinja2.ext.do",'jinja2.ext.i18n'])
session=singleton.session
def set_lang(lang):
    """ 设置网页显示语言 """
    tr = gettext.translation('lang', 'i18n', languages=[lang])
    tr.install(True)
    jjenv.install_gettext_translations(tr)

def login_required(f):
    def new_f(*args, **kwargs):
        if (session.get('login') != 1) :
            return web.seeother(r'/login')
        else: 
            return f(*args, **kwargs)
    new_f.__name__=f.__name__
    return new_f


class BaseHandler(object):
    " URL请求处理类的基类，实现一些共同的工具函数 "
    def __init__(self):
        set_lang("zh-cn") 
        self.env = web.ctx.get('env')
        self.method = web.ctx.get('method')
        #self.params = params
 
    def getcurrentuser(self):
        if self.logined():
            u = KeUser.all().filter("name = ", session.username).get()
            if not u:
                raise web.seeother(r'/login')
            return u
        else:
            return None

    def redirect(self,path):
         return web.seeother(path)

    def logined(self):
        return True if session.get('login') == 1 else False

    def render(self, templatefile, title='KindleEar', **kwargs):        
        """ """
        kwargs.setdefault('nickname', session.get('username'))
        kwargs.setdefault('lang', session.get('lang', 'en'))
        #kwargs.setdefault('version', __Version__)
    
        try:
            return jjenv.get_template(templatefile).render(title=title, **kwargs)
        except Exception, e:
            return e           