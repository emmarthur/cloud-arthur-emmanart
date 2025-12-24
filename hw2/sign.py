from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from Model.model_sqlite3 import model

class Sign(MethodView):
    """
    Handles the add new song route.
    Displays form for adding songs and processes form submissions.
    """
    def get(self):
        """
        Returns the add song form template.
        :return: Rendered HTML template with form
        """
        return render_template('sign.html')

    def post(self):
        """
        Accepts POST requests and processes the form.
        Inserts new song entry into database and redirects to landing page.
        :return: Redirect to landing page
        """
        md = model()
        song_entry = {
            'title': request.form['title'],
            'genre': request.form['genre'],
            'performer': request.form['performer'],
            'writer': request.form['writer'],
            'release_date': request.form['release_date'],
            'lyrics': request.form['lyrics'],
            'rating': request.form['rating'],
            'url': request.form['url']
        }
        md.insert(song_entry)
        return redirect(url_for('index'))