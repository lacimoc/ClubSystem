from utils import db_service, auth_token


def change(payload, token):
    db = db_service.DBService()
    user_id = None
    for user in auth_token.authed_users:
        if user[0] == token:
            user_id = user[1]
    db.update_password(user_id, payload['new_password'])
    return None
