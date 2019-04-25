import requests
import json

from config import *
from db_manager import add_to_db, remove_from_db, get_from_db


def shell(data):
    t = int(len(data) / 2)
    while t > 0:
        for i in range(len(data) - t):
            j = i
            while j >= 0 and data[j]['likes']['count'] > data[j + t]['likes']['count']:
                data[j], data[j + t] = data[j + t], data[j]
                j -= 1
        t = int(t / 2)

    return data


def calculate_middle_likes(items):
    total_like_count = 0

    for i in range(len(items)):
        total_like_count += items[i - 1]['likes']['count']

    return total_like_count / len(items)


def create_popular_posts(posts, middle_likes_count):
    popular_posts = []

    for post in posts:
        likes = int(post['likes']['count'])
        reposts = int(post['reposts']['count'])

        if likes > middle_likes_count * 3:
            popular_posts.append(post)

    return popular_posts


def create_post_dict(posts):
    post_objects = []

    for post in posts:
        images = []

        try:
            for att in post['attachments']:
                image = att['photo']['photo_604']

                if image is not False:
                    images.append(image)
        except KeyError:
            print('Image KeyError')

        post_dict = {
            'id': post['id'],
            'owner_id': post['owner_id'],
            'date': post['date'],
            'text': post['text'],
            'likes_count': post['likes']['count'],
            'images': images,
        }
        post_objects.append(post_dict)

    return post_objects


def load_posts(group_domain):
    all_posts = []

    offset = 0

    while True:
        result = requests.get('https://api.vk.com/method/wall.get',
            params={
                'access_token': access_token,
                'domain': group_domain,
                'count': '100',
                'offset': offset,
                'v': '5.52'
            }
        )
        posts = result.json()
        try:
            posts_items = posts['response']['items']
            oldest_post_date = posts_items[99]['date']

            if oldest_post_date < one_year_ago:
                break

            all_posts.extend(posts_items)

            offset += 100
        except KeyError:
            print('Key error')

    return all_posts


def get_posts_from_vk():
    all_popular_posts = []

    for group_domain in group_domains_arr:
        all_posts = load_posts(group_domain=group_domain)
        middle_likes = calculate_middle_likes(items=all_posts)
        popular_posts = create_popular_posts(posts=all_posts, middle_likes_count=middle_likes)
        popular_posts = shell(data=popular_posts)
        posts = create_post_dict(popular_posts)
        all_popular_posts.extend(posts)

    add_posts_to_db(posts=all_popular_posts)
    posts = get_posts_from_db()

    return posts


def get_posts_from_db():
    return get_from_db()


def add_posts_to_db(posts):
    remove_from_db(owner_id=posts[0]['owner_id'])
    add_to_db(data_arr=posts)


'''
    {'id': 2020559, 'from_id': -91050183, 'owner_id': -91050183, 'date': 1546205167,
    'marked_as_ads': 0, 'post_type': 'post', 'text': '',
    'attachments': [{'type': 'photo', 'photo': {'id': 456634593, 'album_id': -7, 'owner_id': -91050183, 'user_id': 100,
    'photo_75': 'https://pp.userapi.com/c7006/v7006173/405f2/FabmXRE1K8k.jpg', 'photo_130':
    'https://pp.userapi.com/c7006/v7006173/405f3/xLaaQebMkQg.jpg', 'photo_604':
    'https://pp.userapi.com/c7006/v7006173/405f4/2v0rwcn3ZR4.jpg', 'photo_807':
    'https://pp.userapi.com/c7006/v7006173/405f5/iE6VAc9OUDM.jpg', 'width': 556,
    'height': 616, 'text': '', 'date': 1546205167, 'post_id': 2020559, 'access_key':
    'ecc5e3a7c7752eb42c'}}],
    'post_source': {'type': 'api'}, 'comments': {'count': 3344, 'can_post': 1},
    'likes': {'count': 59706, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
    'reposts': {'count': 258, 'user_reposted': 0}}
'''
