import copy
import datetime

from utils import db_service, auth_token
from settings import template


def add_user(payload: dict) -> None:
    """
    通过表单添加用户
    :param payload: 用户信息表单
    :return: None
    """
    db = db_service.DBService()
    username = payload['username']
    name = payload['name']
    password = payload['password']
    department = int(payload['departmentId'][-1])
    is_admin = payload['isAdmin']
    db.create_user(department, username, password, name, is_admin)
    return None


def delete_user(payload: dict) -> None:
    """
    通过表单删除用户
    :param payload: 用户信息表单
    :return: None
    """
    db = db_service.DBService()
    db.delete_user(int(payload['userId']))
    return None


def get_user_info(token: str) -> dict:
    """
    通过token获取用户信息
    :param token: 用户token
    :return: 用户信息
    """
    db = db_service.DBService()
    user_id = None
    for user in auth_token.authed_users:
        if user[0] == token:
            user_id = user[1]

    if user_id is None:
        return copy.deepcopy(template.unauthorized_template)

    user_info = db.get_user_info(int(user_id))

    ret_dict = copy.deepcopy(template.response_template)
    is_admin = user_info[1] == 1
    ret_dict['data'] = {
        "name": user_info[0],
        "id": user_id,
        "role": is_admin
    }
    return ret_dict


def get_all_users() -> dict:
    """
    获取所有用户信息
    :return: 所有用户信息
    """
    db = db_service.DBService()
    all_users = db.get_all_users()
    users = []
    for user in all_users:
        # 2025-05-01 19:39:15转换为ISO 8601格式
        join_time = datetime.datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S')
        is_admin = user[4] == 1
        users.append({
            "id": str(user[0]),
            "username": user[1],
            "createdAt": datetime.datetime.fromtimestamp(join_time.timestamp()).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "departmentId": 'dept_0' + str(user[3]),
            "isAdmin": is_admin,
            "name": user[5]
        })
    ret_dict = copy.deepcopy(template.response_template)
    ret_dict['data'] = users
    return ret_dict
