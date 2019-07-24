from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'asdf'),
    User(2, 'user2', 'abcxyz')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')): # safe way to compare string accross many python, O.S. version and servers
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
