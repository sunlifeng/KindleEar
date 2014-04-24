import web
from model import * 
from BaseHandler import BaseHandler,login_required


class Home(BaseHandler):
    """

    """
    @login_required
    def index(self, **args):
        return self.render('home.html',"Home")

    @login_required    
    def settings(self,**args):

        user= self.getcurrentuser()
        return self.render('setting.html',"Setting",
            current='setting',user=user)
        #return self.redirect(r"/setting")
