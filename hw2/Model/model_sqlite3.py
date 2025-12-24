from .Model import Model
from datetime import date
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    """
    SQLite3 implementation of the Model class.
    Handles database operations for song entries.
    """
    def __init__(self):
        """
        Initialize database connection and create songs table if it doesn't exist.
        """
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from songs")
        except sqlite3.OperationalError:
            cursor.execute("create table songs (title, genre, performer, writer, release_date, lyrics, rating, url)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database as a list of tuples.
        :return: List of tuples containing all song rows from database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()

    #def insert(self, name, email, message):
    def insert(self, song_entry):
        """
        Inserts song entry into database.
        :param song_entry: Dictionary containing song fields
        :return: True if successful
        """
        params = {
            'title': song_entry['title'],
            'genre': song_entry['genre'],
            'performer': song_entry['performer'],
            'writer': song_entry['writer'],
            'release_date': song_entry['release_date'],
            'lyrics': song_entry['lyrics'],
            'rating': song_entry['rating'],
            'url': song_entry['url']
        }
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(
            """insert into songs (title, genre, performer, writer, release_date, lyrics, rating, url) 
            VALUES (:title, :genre, :performer, :writer, :release_date, :lyrics, :rating, :url)""", params)
        connection.commit()
        cursor.close()
        return True