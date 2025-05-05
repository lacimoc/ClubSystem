from utils import db_service


def reset(payload):
    db = db_service.DBService()
    db.reset_password(int(payload['userId']))
    return None
