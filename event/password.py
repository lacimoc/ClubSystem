from utils import db_service, auth_token


def reset_password(payload):
    db = db_service.DBService()
    db.reset_password(int(payload['userId']))
    return None


def change_password(payload, token):
    db = db_service.DBService()
    user_id = None
    for user in auth_token.authed_users:
        if user[0] == token:
            user_id = user[1]
    db.update_password(user_id, payload['new_password'])
    return None
