#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__      = "bellven"
__version__     = "0.1"

from base import BaseFeedBook

def getBook():
    return kr

class kr(BaseFeedBook):
    title                 = u'36氪'
    description           = u'36氪｜关注互联网创业'
    language = 'zh-cn'
    feed_encoding = "utf-8"
    page_encoding = "utf-8"
    mastheadfile = "mh_36kr.gif"
    coverfile =  'cv_36kr.jpg'
    keep_image = True
    fulltext_by_readability = True
    fulltext_by_instapaper = False
    oldest_article = 1
    feeds = [
            (u'36氪','http://www.36kr.com/feed',True)
           ]
