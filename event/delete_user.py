from utils import db_service


def delete(payload):
    db = db_service.DBService()
    db.delete_user(int(payload['userId']))
    return None
