# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from datetime import datetime
from google.cloud import datastore

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [title, genre, performer, writer, release_date, lyrics, rating, url]
    where all fields are Python strings
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['title'],entity['genre'],entity['performer'],entity['writer'],entity['release_date'],entity['lyrics'],entity['rating'],entity['url']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-arthur-emmanart')

    def select(self):
        query = self.client.query(kind = 'hw4_songs')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, song_entry):
        key = self.client.key('hw4_songs')
        rev = datastore.Entity(key)
        rev.update( {
            'title': song_entry['title'],
            'genre': song_entry['genre'],
            'performer': song_entry['performer'],
            'writer': song_entry['writer'],
            'release_date': song_entry['release_date'],
            'lyrics': song_entry['lyrics'],
            'rating': song_entry['rating'],
            'url': song_entry['url']
            })
        self.client.put(rev)
        return True
