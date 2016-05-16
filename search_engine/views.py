from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

search = Blueprint('search', __name__, template_folder='templates')


class HomeView(MethodView):
    def get(self):
        return render_template('index.html')

class SearchView(MethodView):
    def get(self):
        return render_template('search.html')

class ResultView(MethodView):
    def get(self):
        return render_template('result.html')

class NEVennView(MethodView):
    def get(self):
        return render_template('ne_venn.html')
        


# Register the urls
# search.add_url_rule('/', view_func=HomeView.as_view('index'))
# search.add_url_rule('/search', view_func=SearchView.as_view('list'))
# search.add_url_rule('/result', view_func=ResultView.as_view('view'))