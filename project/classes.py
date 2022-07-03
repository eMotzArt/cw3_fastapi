import os
import json
from paths import DATA_PATH_ABS

class Repository:
    def __init__(self):
        self.source_file = os.path.join(DATA_PATH_ABS, 'data.json')

    def get_all_posts(self):
        with open(self.source_file) as file:
            all_posts = json.load(file)
        return all_posts

    def add_like(self, post_id):
        ...

    def add_view(self, post_id):
        ...

    def add_comment(self, post_id, name, comment):
        ...



x = Repository()
y = Repository().get_all_posts()
pass
