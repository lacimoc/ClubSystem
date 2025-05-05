from utils import db_service


def update(payload):
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
    activity_id = payload['id']
    db.update_activity(capacity, start_time, end_time, title, 'upcoming', description, department, cover, location, registration_time, activity_id)
    return None
