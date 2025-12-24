from flask import render_template
from flask.views import MethodView
from Model.model_sqlite3 import model

class View(MethodView):
    """
    Handles the view all songs route.
    Retrieves and displays all song entries from the database.
    """
    def get(self):
        """
        Retrieves all songs from database and renders the view template.
        :return: Rendered HTML template with list of songs
        """
        md = model()
        entries = [dict(title=row[0], genre=row[1], performer=row[2], writer=row[3], release_date=row[4], lyrics=row[5], rating=row[6], url=row[7]) for row in md.select()]
        return render_template('view.html',entries=entries)