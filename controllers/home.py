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
        #default_log.warn("test")
        return self.render('home.html',"Home")


    def login(self,**args):

        def CheckAdminAccount():
            #判断管理员账号是否存在
            #如果管理员账号不存在，创建一个，并返回False，否则返回True
            u = KeUser.all().filter("name = ", 'admin').get()
            if not u:            
                myfeeds = Book(title=MY_FEEDS_TITLE,description=MY_FEEDS_DESC,
                        builtin=False,keep_image=True,oldest_article=7)
                myfeeds.put()
                au = KeUser(name='admin',passwd=hashlib.md5('admin').hexdigest(),
                    kindle_email='',enable_send=False,send_time=8,timezone=TIMEZONE,
                    book_type="mobi",device='kindle',expires=None,ownfeeds=myfeeds,merge_books=False)
                au.put()
                return False
            else:
                return True
        tips = ''
        if self.method=="POST":
            name, passwd = web.input().get('u'), web.input().get('p')
            if name.strip() == '':
                tips = _("Username is empty!")
                return self.render('login.html',"Login",nickname='',tips=tips)
            elif len(name) > 25:
                tips = _("The len of username reached the limit of 25 chars!")
                return self.render('login.html',"Login",nickname='',tips=tips,username=name)
            elif '<' in name or '>' in name or '&' in name:
                tips = _("The username includes unsafe chars!")
                return self.render('login.html',"Login",nickname='',tips=tips)
            CheckAdminAccount() #确认管理员账号是否存在
            try:
                pwdhash = hashlib.md5(passwd).hexdigest()
            except:
                u = None
            else:
                u = KeUser.all().filter("name = ", name).filter("passwd = ", pwdhash).get()            
            if u:
                self.set_session("login",1)
                self.set_session("username",u.name)
                if u.expires: #用户登陆后自动续期
                    u.expires = datetime.datetime.utcnow()+datetime.timedelta(days=180)
                    u.put()
                raise web.seeother(r'/home/mysubscription')


        tips = ''
        if not CheckAdminAccount():
            tips = _("Please use admin/admin to login at first time.")
        else:
            tips = _("Please input username and password.")                  
        if self.get_session('login') == 1:
            web.seeother(r'/')
        else:
            return self.render('login.html',"Login",tips=tips)


    @login_required
    def mgrpwd(self,**args):
        user = self.getcurrentuser()
        name=args["url"][0] 
        tips = _("Please input new password to confirm!")
        if self.method=="POST":
              name, p1, p2 = web.input().get('u'),web.input().get('p1'),web.input().get('p2')              
              u = KeUser.all().filter("name = ", name).get()
              if user.name=="admin":
                if not u:
                    tips = _("The username '%s' not exist!") % name
                elif p1 != p2:
                    tips = _("The two new passwords are dismatch!")
                else:
                    try:
                        pwd = hashlib.md5(p1).hexdigest()
                    except:
                        tips = _("The password includes non-ascii chars!")
                    else:
                        u.passwd = pwd
                        u.put()
                        tips = _("Change password success!")


              tips = _("Please input new password to confirm!")
        return self.render('adminmgrpwd.html', "Change password",
            tips=tips,username=name)
    
    @login_required
    def delfeed(self,**args):
        user = self.getcurrentuser()
        id=args["url"][0]
        if not id:
            return "the id is empty!<br />"
        try:
            id = int(id)
        except:
            return "the id is invalid!<br />"
        feed = Feed.get_by_id(id)
        if feed:
            feed.delete()
        raise web.seeother('/home/mysubscription')

    @login_required
    def logout(self,**args):
        if self.get_session('login')==1:
            self.set_session('login',0)
            self.set_session('username','')
        self.redirect("/")

        pass
    @login_required
    def logs(self,**args):
        """投递日志"""
        user = self.getcurrentuser()
        mylogs = DeliverLog.all().filter("username = ", user.name).order('-time').fetch(limit=10)
        logs = {}
        if user.name == 'admin':
            for u in KeUser.all().filter("name != ", 'admin'):
                ul = DeliverLog.all().filter("username = ", u.name).order('-time').fetch(limit=5)
                if ul:
                    logs[u.name] =  ul
        return self.render('logs.html', "Deliver log", current='logs',
            mylogs=mylogs, logs=logs)

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

    @login_required
    def unsubscription(self,**args):        
        id=args["url"][0]
        username=self.getcurrentuser().name
        if not id:
            return "the id is empty!<br />"
        try:
            id = int(id)
        except:
            return "the id is invalid!<br />"            
        bk = Book.get_by_id(id)
        if not bk:
            return "the book(%d) not exist!<br />" % id        
        if username in bk.users:
            bk.users.remove(username)
            bk.put()
        raise web.seeother('/home/mysubscription')

    @login_required
    def subscription(self,**args):
        """订阅"""
        id=args["url"][0]
        username=self.getcurrentuser().name

        if not id:
            return "the id is empty!<br />"
        try:
            id = int(id)
        except:
            return "the id is invalid!<br />"
        bk = Book.get_by_id(id)
        if not bk:
            return "the book(%d) not exist!<br />" % id
        if username not in bk.users:
            bk.users.append(username)
            bk.put()
        raise web.seeother('/home/mysubscription')

    @login_required
    def mysubscription(self,**args):
        """已有的订阅"""
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
