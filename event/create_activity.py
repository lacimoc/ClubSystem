from utils import db_service


def create(payload):
    db = db_service.DBService()
    capacity = int(payload['capacity'])
    start_time = payload['startTime']
    end_time = payload['endTime']
    registration_time = payload['registration_time']
    title = payload['title']
    description = payload['description']
    department = payload['department']
    cover = payload['cover']
    location = payload['location']
    db.create_activity(capacity, 0, start_time, end_time, title, 'upcoming', description, department, cover, location, registration_time)
    return None
