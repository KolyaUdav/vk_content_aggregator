from datetime import datetime


access_token='8a1d45996c7340413b4f5ddf50467eda7fdd7af1251e4073fc456190d0a9b0303227a23bdd6bfe2814f07'
one_year_ago = datetime.now().timestamp() - 31536000 # 31536000 = 1 year
db_name = 'aggregator.db'

group_domains_arr = [
    'godnota_txt',
    'tproger',
]
