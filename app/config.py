import os

read_delay = 600
grab_delay = 3600
 
db_news = {
    'host': os.environ.get('DB_NEWS_HOST', 'host.docker.internal'),
    'port': int(os.environ.get('DB_NEWS_PORT', 3306)),
    'user': os.environ.get('DB_NEWS_USER', 'root'),
    'password': os.environ.get('DB_NEWS_PASSWORD', 'root'),
    'database': os.environ.get('DB_NEWS_NAME', 'local_db_news'),
    #'charset':'utf8',
    }

# aws_configs = {
#     "bucket": "clipdata",
#     "credentials": {
#         "aws_access_key_id": "AKIA3PPZC5PNUVDGE224",
#         "aws_secret_access_key": "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",
#         "region_name": "eu-west-1"
#     }
# }

telegram = {
    "session_name": os.environ.get('SESSION_NAME', 'newsfeed'), 
    "api_id": int(os.environ.get('API_ID', 0)), 
    "api_hash": os.environ.get('API_HASH', None)
}

channel = {
    "id": int(os.environ.get('CHANNEL_ID', 0)),
    "name": ''
}
