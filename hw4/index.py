# from flask import Flask, redirect, request, url_for, render_template
# from model_pylist import model
from flask import render_template
from flask.views import MethodView
from Model.model_sqlite3 import model

class Index(MethodView):
    """
    Handles the landing page route.
    Displays links to view all songs and add new songs.
    """
    def get(self):
        """
        Returns the landing page template.
        :return: Rendered HTML template
        """
        return render_template('index.html')