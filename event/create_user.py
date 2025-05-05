from utils import db_service


def add_user(payload):
    db = db_service.DBService()
    username = payload['username']
    name = payload['name']
    password = payload['password']
    department = int(payload['departmentId'][-1])
    is_admin = payload['isAdmin']
    db.create_user(department, username, password, name, is_admin)
    return None
