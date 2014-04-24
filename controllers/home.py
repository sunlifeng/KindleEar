import web
from BaseHandler import BaseHandler,login_required


class Home(BaseHandler):
    @login_required
    def index(self, *args):
        return self.redirect(r"/")