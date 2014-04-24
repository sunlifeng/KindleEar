#!/usr/bin/env python
# -*- coding:utf-8 -*-
from google.appengine.api import memcache

from google.appengine.ext import db

#--------------db models----------------
class Book(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty()
    users = db.StringListProperty()
    builtin = db.BooleanProperty() # 内置书籍不可修改
    #====自定义书籍
    language = db.StringProperty()
    mastheadfile = db.StringProperty() # GIF 600*60
    coverfile = db.StringProperty()
    keep_image = db.BooleanProperty()
    oldest_article = db.IntegerProperty()
    
    #这三个属性只有自定义RSS才有意义
    @property
    def feeds(self):
        return Feed.all().filter('book = ', self.key()).order('time')
        
    @property
    def feedscount(self):
        mkey = '%d.feedscount'%self.key().id()
        mfc = memcache.get(mkey)
        if mfc is not None:
            return mfc
        else:
            fc = self.feeds.count()
            memcache.add(mkey, fc, 86400)
            return fc
    @property
    def owner(self):
        return KeUser.all().filter('ownfeeds = ', self.key())
    
class KeUser(db.Model): # kindleEar User
    name = db.StringProperty(required=True)
    passwd = db.StringProperty(required=True)
    kindle_email = db.StringProperty()
    enable_send = db.BooleanProperty()
    send_days = db.StringListProperty()
    send_time = db.IntegerProperty()
    timezone = db.IntegerProperty()
    book_type = db.StringProperty()
    device = db.StringProperty()
    expires = db.DateTimeProperty()
    ownfeeds = db.ReferenceProperty(Book) # 每个用户都有自己的自定义RSS
    titlefmt = db.StringProperty() #在元数据标题中添加日期的格式
    merge_books = db.BooleanProperty() #是否合并书籍成一本
    
    share_fuckgfw = db.BooleanProperty() #归档和分享时是否需要翻墙
    evernote = db.BooleanProperty() #是否分享至evernote
    evernote_mail = db.StringProperty() #evernote邮件地址
    wiz = db.BooleanProperty() #为知笔记
    wiz_mail = db.StringProperty()
    xweibo = db.BooleanProperty()
    tweibo = db.BooleanProperty()
    facebook = db.BooleanProperty() #分享链接到facebook
    twitter = db.BooleanProperty()
    tumblr = db.BooleanProperty()
    browser = db.BooleanProperty()
    
    @property
    def whitelist(self):
        return WhiteList.all().filter('user = ', self.key())
    
    @property
    def urlfilter(self):
        return UrlFilter.all().filter('user = ', self.key())
    
class Feed(db.Model):
    book = db.ReferenceProperty(Book)
    title = db.StringProperty()
    url = db.StringProperty()
    isfulltext = db.BooleanProperty()
    time = db.DateTimeProperty() #源被加入的时间，用于排序
    
class DeliverLog(db.Model):
    username = db.StringProperty()
    to = db.StringProperty()
    size = db.IntegerProperty()
    time = db.StringProperty()
    datetime = db.DateTimeProperty()
    book = db.StringProperty()
    status = db.StringProperty()

class WhiteList(db.Model):
    mail = db.StringProperty()
    user = db.ReferenceProperty(KeUser)

class UrlFilter(db.Model):
    url = db.StringProperty()
    user = db.ReferenceProperty(KeUser)

class Newses(db.Model):
    section = db.StringProperty()
    title = db.StringProperty()
    url = db.StringProperty()
    content = db.StringProperty()
    brief = db.StringProperty()
    datetime = db.DateTimeProperty()
    #section,url,title,content,brief