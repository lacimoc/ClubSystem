from utils import db_service, auth_token


def reset_password(payload: dict) -> None:
    """
    通过表单重置密码
    :param payload: 包含用户id的表单
    :return: None
    """
    db = db_service.DBService()
    db.reset_password(int(payload['userId']))
    return None


def change_password(payload: dict, token: str) -> None:
    """
    通过表单和token修改密码
    :param payload: 包含新密码的表单
    :param token: 用户的token
    :return: None
    """
    db = db_service.DBService()
    user_id = None
    for user in auth_token.authed_users:
        if user[0] == token:
            user_id = user[1]
    db.update_password(int(user_id), payload['new_password'])
    return None
