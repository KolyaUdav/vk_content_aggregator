import sqlite3

from config import db_name


def open_connect_db():
    return sqlite3.connect(db_name)


def close_connect_db(db):
    db.close()


def remove_from_db(owner_id):
    db = open_connect_db()
    create_sql_request(db, 'DELETE FROM posts')
    create_sql_request(db, 'DELETE FROM images')
    close_connect_db(db)


def create_sql_request(db, req, *params):
    c = db.cursor()

    try:
        if len(params) > 0:
            c.execute(req, params[0])
        else:
            c.execute(req)
    except sqlite3.DatabaseError as err:
        print('Error: ', err)
    else:
        db.commit()

    return c


def get_from_db():
    db = open_connect_db()

    posts = []

    c = create_sql_request(db, 'SELECT * FROM posts')
    posts_row = c.fetchall()

    for pr in posts_row:
        post = {
            'post_id': pr[1],
            'owner_id': pr[2],
            'date': pr[3],
            'text': pr[4],
            'likes_count': pr[5],
        }
        c = create_sql_request(db, 'SELECT source FROM images WHERE post_id = ?', (str(post['post_id']),))
        images_row = c.fetchall()
        post['images'] = images_row
        posts.append(post)

    close_connect_db(db)

    return posts


def add_to_db(data_arr):
    db = open_connect_db()
    c = db.cursor()

    for data_item in data_arr:
        add_post(db=db, cursor=c, post=data_item)

    close_connect_db(db=db)


def add_post(db, cursor, post):
    post_id = '{}_{}'.format(str(post['id']), str(post['owner_id']))
    owner_id = str(post['owner_id'])
    text = post['text']
    count = post['likes_count']
    date = post['date']

    create_sql_request(db,
        'INSERT INTO posts(post_id, owner_id, date, text, likes_count) VALUES(?, ?, ?, ?, ?)',
        (post_id, owner_id, date, text, count,))

    for image in post['images']:
        create_sql_request(db,
            'INSERT INTO images(post_id, owner_id, source) VALUES(?, ?, ?)',
            (post_id, owner_id, image,))
