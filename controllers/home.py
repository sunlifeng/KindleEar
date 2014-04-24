#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib,time,datetime
import web
from config import *
from model import * 
from BaseHandler import BaseHandler,login_required


class Home(BaseHandler):
    """
    首页及帐户管理
    """

   
    def index(self, **args):
        """首页"""
        return self.render('home.html',"Home")

    @login_required    
    def delaccount(self,**args):
        """删除账户页面"""
        tips=""    
        name=args["url"][0] 
        login_name= self.getcurrentuser().name          
        if login_name == 'admin' :
            tips = _("Please confirm to delete the account!")
        
        if self.method=="POST":
            name = web.input().get('u')
            if name and (login_name == "admin" or login_name == name):
                u = KeUser.all().filter("name = ", name).get()
                if not u:
                    tips = _("The username '%s' not exist!") % name
                else:
                    if u.ownfeeds:
                        for feed in u.ownfeeds.feeds:
                            feed.delete()
                        u.ownfeeds.delete()
                    u.delete()
                    
                    # 删掉订阅记录
                    for book in Book.all():
                        if book.users and name in book.users:
                            book.users.remove(name)
                            book.put()
                    
                    if login_name == name:
                        raise web.seeother('/logout')
                    else:
                        raise web.seeother('/home/admin')
            else:
                tips = _("The username is empty or you dont have right to delete it!")
            return self.render('delaccount.html', "Delete account",
                    tips=tips, username=name)            
        return self.render('delaccount.html', "Delete account",
                tips=tips,username=name)

    @login_required
    def admin(self,**args):
        """账户管理页面"""
        user = self.getcurrentuser()
        users = KeUser.all() if user.name == 'admin' else None
        if self.method=="POST":
            u,up1,up2 = web.input().get('u'),web.input().get('up1'),web.input().get('up2')
            op,p1,p2 = web.input().get('op'), web.input().get('p1'), web.input().get('p2')
            user = self.getcurrentuser()
            users = KeUser.all() if user.name == 'admin' else None
            if op is not None and p1 is not None and p2 is not None: #修改密码
                try:
                    pwd = hashlib.md5(op).hexdigest()
                    newpwd = hashlib.md5(p1).hexdigest()
                except:
                    tips = _("The password includes non-ascii chars!")
                else:
                    if user.passwd != pwd:
                        tips = _("Old password is wrong!")
                    elif p1 != p2:
                        tips = _("The two new passwords are dismatch!")
                    else:
                        tips = _("Change password success!")
                        user.passwd = newpwd
                        user.put()
                return self.render('admin.html',"Admin",
                    current='admin', user=user, users=users,chpwdtips=tips)
            elif u is not None and up1 is not None and up2 is not None: #添加账户
                if user.name != 'admin':
                    raise web.seeother(r'/')
                elif not u:
                    tips = _("Username is empty!")
                elif up1 != up2:
                    tips = _("The two new passwords are dismatch!")
                elif KeUser.all().filter("name = ", u).get():
                    tips = _("Already exist the username!")
                else:
                    try:                        
                        pwd = hashlib.md5(up1).hexdigest()
                    except:
                        tips = _("The password includes non-ascii chars!")

                    else:
                        myfeeds = Book(title=MY_FEEDS_TITLE,description=MY_FEEDS_DESC,
                            builtin=False,keep_image=True,oldest_article=7)
                        myfeeds.put()
                        au = KeUser(name=u,passwd=pwd,kindle_email='',enable_send=False,
                            send_time=7,timezone=TIMEZONE,book_type="mobi",
                            ownfeeds=myfeeds,merge_books=False)
                        au.expires = datetime.datetime.utcnow()+datetime.timedelta(days=180)
                        au.put()
                        users = KeUser.all() if user.name == 'admin' else None
                        tips = _("Add a account success!")                        
                return self.render('admin.html',"Admin",
                    current='admin', user=user, users=users,actips=tips)
            else:
                user = self.getcurrentuser()
                users = KeUser.all() if user.name == 'admin' else None
                return self.render('admin.html',"Admin",
            current='admin', user=user, users=users)

        return self.render('admin.html',"Admin",
            current='admin', user=user, users=users)

    @login_required    
    def settings(self,**args):
        """用户信息设置"""
        tips = ""
        user= self.getcurrentuser()       
        if self.method=="POST":
            kemail = web.input().get('kindleemail')
            mytitle = web.input().get("rt")
            if not kemail:
                tips = _("Kindle E-mail is requied!")
            elif not mytitle:
                tips = _("Title is requied!")
            else:
                user.kindle_email = kemail
                user.timezone = int(web.input().get('timezone', TIMEZONE))
                user.send_time = int(web.input().get('sendtime'))
                user.enable_send = bool(web.input().get('enablesend'))
                user.book_type = web.input().get('booktype')
                user.device = web.input().get('devicetype') or 'kindle'
                user.titlefmt = web.input().get('titlefmt')
                alldays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                user.send_days = [day for day in alldays if web.input().get(day)]
                user.merge_books = bool(web.input().get('mergebooks'))
                user.put()
                myfeeds = user.ownfeeds
                myfeeds.language = web.input().get("lng")
                myfeeds.title = mytitle
                myfeeds.keep_image = bool(web.input().get("keepimage"))
                myfeeds.oldest_article = int(web.input().get('oldest', 7))
                myfeeds.users = [user.name] if web.input().get("enablerss") else []
                myfeeds.put()
                tips = _("Settings Saved!")

        return self.render('setting.html',"Setting",
            current='setting',user=user,tips=tips)
        #return self.redirect(r"/setting")

    def MySubscription(self,**args):
        user = self.getcurrentuser()
        tips=args["url"]
        myfeeds = user.ownfeeds.feeds if user.ownfeeds else None
        if self.method=="POST":
            user = self.getcurrentuser()
            title = web.input().get('t')
            url = web.input().get('url')
            isfulltext = bool(web.input().get('fulltext'))
            if not title or not url:
                return self.GET(_("Title or url is empty!"))
            
            if not url.lower().startswith('http'): #http and https
                url = 'http://' + url
            assert user.ownfeeds
            Feed(title=title,url=url,book=user.ownfeeds,isfulltext=isfulltext,
                time=datetime.datetime.utcnow()).put()
            memcache.delete('%d.feedscount'%user.ownfeeds.key().id())
            raise web.seeother('/home/MySubscription')
        return self.render('my.html', "My subscription",current='my',
            books=Book.all().filter("builtin = ",True),myfeeds=myfeeds,tips=tips)
