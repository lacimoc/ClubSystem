import hashlib
import time
import uuid
import bcrypt
from utils import db_service


authed_users = []
admin_authed_users: list[str] = []


def auth(token: str) -> bool:
    """
    通过token验证用户是否登录
    :param token: 用户token
    :return: 登录成功返回True，否则返回False
    """
    for user in authed_users:
        if user[2] < time.time():
            authed_users.remove(user)
    for user in authed_users:
        if token == user[0]:
            user[2] = time.time() + 600
            return True
    return False


def admin_auth(token: str) -> bool:
    """
    通过token验证管理员是否登录
    :param token: 用户token
    :return: 是管理员登录返回True，否则返回False
    """
    if token in admin_authed_users:
        return True
    else:
        return False


def login(username: str, password: str) -> str:
    """
    通过用户名和密码登录，并返回token
    :param username: 用户名
    :param password: 密码
    :return: 登录成功返回token，否则返回空字符串
    """
    db = db_service.DBService()
    db_pwd = db.get_password(username)
    if db_pwd is None:
        return ''
    if bcrypt.checkpw(password.encode('utf-8'), db_pwd):
        access_token = generate_token(username)
        user_id = db.get_user_id(username)
        authed_users.append([access_token, user_id, time.time()+600])
        if db.is_admin(int(user_id)):
            admin_authed_users.append(access_token)
        return access_token
    else:
        return ''


def generate_token(username: str) -> str:
    """
    通过用户名生成token
    :param username: 用户名
    :return: 生成的token
    """
    data = username+str(uuid.uuid4())
    return str(hashlib.sha256(data.encode('utf-8')).hexdigest())
