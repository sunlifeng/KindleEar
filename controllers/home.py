import web


views = web.template.render('views/')


class Home:
    def index(self, *args):
        return views.index()