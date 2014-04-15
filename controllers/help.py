import web


views = web.template.render('views/')


class Help:
    def index(self, *args):
        return views.index()