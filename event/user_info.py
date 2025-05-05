from utils import template, db_service, auth_token
import copy
import datetime


def get_user_info(token) -> dict:
    db = db_service.DBService()
    user_id = None
    for user in auth_token.authed_users:
        if user[0] == token:
            user_id = user[1]

    if user_id is None:
        return copy.deepcopy(template.unauthorized_template)

    user_info = db.get_user_info(user_id)

    ret_dict = copy.deepcopy(template.response_template)
    is_admin = user_info[1] == 1
    ret_dict['data'] = {
        "name": user_info[0],
        "id": user_id,
        "role": is_admin
    }
    return ret_dict


def get_all_users() -> dict:
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
