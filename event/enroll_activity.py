from utils import db_service
from utils import auth_token


def enroll(payload, token):
    db = db_service.DBService()
    active_id = payload['id']
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    db.enroll_activity(active_id, user_id)
    return None


def cancel_enroll(payload, token):
    db = db_service.DBService()
    active_id = payload['activityId']
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    db.cancel_enroll_activity(active_id, user_id)
    return None
