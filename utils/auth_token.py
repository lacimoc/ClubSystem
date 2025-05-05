import hashlib
import time
import uuid
import bcrypt
from utils import db_service


authed_users = []
admin_authed_users = []


def auth(token) -> bool:
    for user in authed_users:
        if user[2] < time.time():
            authed_users.remove(user)
    for user in authed_users:
        if token == user[0]:
            user[2] = time.time() + 600
            return True
    return False


def admin_auth(token) -> bool:
    if token in admin_authed_users:
        return True
    else:
        return False


def login(username, password) -> str:
    db = db_service.DBService()
    db_pwd = db.get_password(username)
    if db_pwd is None:
        return ''
    if bcrypt.checkpw(password.encode('utf-8'), db_pwd):
        access_token = generate_token(username)
        user_id = db.get_user_id(username)
        authed_users.append([access_token, user_id, time.time()+600])
        if db.is_admin(user_id):
            admin_authed_users.append(access_token)
        return access_token
    else:
        return ''


def generate_token(username) -> str:
    data = username+str(uuid.uuid4())
    return str(hashlib.sha256(data.encode('utf-8')).hexdigest())
