from flask import Flask
from flask import render_template

from content import get_posts_from_vk, get_posts_from_db

import webbrowser
import json


webbrowser.open('http://127.0.0.1:5000/', new=2, autoraise=True)

app = Flask(__name__)

my_db = 'aggregator.db'

@app.route('/')
def load_list():
    return render_template('post_list.html')


@app.route('/load_content')
def load_content():
    print('load content')
    posts = get_posts_from_vk()
    return json.dumps(posts, ensure_ascii=False)


@app.route('/load_cached')
def load_cached():
    posts = get_posts_from_db()
    return json.dumps(posts, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
