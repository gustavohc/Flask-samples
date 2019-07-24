from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')): # safe way to compare string accross many python, O.S. version and servers
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
