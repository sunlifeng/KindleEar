#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__      = "bellven"
__version__     = "0.1"

from base import BaseFeedBook

def getBook():
    return bv

class bv(BaseFeedBook):
    title                 = u'商业价值'
    description           = u'商业价值｜更创新，更智慧，更可持续的商业'
    language = 'zh-cn'
    feed_encoding = "utf-8"
    page_encoding = "utf-8"
    mastheadfile = "mh_bv.gif"
    coverfile =  'cv_bv.jpg'
    keep_image = True
    fulltext_by_readability = True
    fulltext_by_instapaper = False
    oldest_article = 1
    feeds = [
            (u'商业价值','http://content.businessvalue.com.cn/feed',True)
           ]
