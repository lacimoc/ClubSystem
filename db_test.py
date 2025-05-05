from utils import db_service


if __name__ == '__main__':
    db = db_service.DBService()
    db.init_db()
    print(db.get_user_activity_info("2"))
