#!/usr/bin/env python
# -*- coding:utf-8 -*-



import web
import jinja2
import gettext
from lib.helper import singleton

class BaseHandler(object):
    " URL请求处理类的基类，实现一些共同的工具函数 "
    def __init__(self):
        session=singleton.session
        if not session.get('lang'):
            session.lang = self.browerlang()
            
    def render(self, templatefile, title='KindleEar', **kwargs):
        kwargs.setdefault('nickname', session.get('username'))
        kwargs.setdefault('lang', session.get('lang', 'en'))
        kwargs.setdefault('version', __Version__)
        return jjenv.get_template(templatefile).render(title=title, **kwargs)
