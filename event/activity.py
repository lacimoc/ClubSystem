import copy

from utils import db_service, auth_token
from settings import template


def get_user_activity_info(token):
    db = db_service.DBService()
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    activities = db.get_user_activity_info(user_id)
    response = copy.deepcopy(template.response_template)
    response['data'] = {
        "total": 15,
        "current_page": 1,
        "page_size": 10,
        "activities": [
            {
                "id": activity[0],
                "title": activity[1],
                "cover": activity[7],
                "status": "registered",
                "time": activity[3],
                "location": activity[8],
                "registration_time": "2024-03-15T09:30:00Z",
                "max_participants": activity[10],
                "current_participants": activity[9]
            } for activity in activities
        ]
    }
    return response


def delete_activity(payload):
    db = db_service.DBService()
    activity_id = payload['activityId']
    db.delete_activity(activity_id)
    return None


def get_activities_info(token):
    db = db_service.DBService()
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    activities = db.get_activities(user_id)
    if type(activities) is not tuple:
        response = copy.deepcopy(template.response_template)
        return response
    response = copy.deepcopy(template.response_template)
    if auth_token.admin_auth(token):
        response['data'] = [
            {
                "id": str(activity[0]),
                "title": activity[1],
                "cover": activity[7],
                "startTime": activity[3],
                "endTime": activity[4],
                "location": activity[8],
                "capacity": activity[10],
                "enrolled": activity[9],
                "status": activity[2],
                "description": activity[5],
                "department": activity[6],
                "registration_time": activity[11]
            } for activity in activities[0]
        ]
    else:
        response['data'] = [
            {
                "id": str(activity[0]),
                "title": activity[1],
                "cover": activity[7],
                "startTime": activity[3],
                "endTime": activity[4],
                "location": activity[8],
                "capacity": activity[10],
                "enrolled": activity[9],
                "status": activity[2],
                "description": activity[5],
                "department": activity[6],
                "registration_time": activity[11]
            } for activity in activities[0] if activity[6] == activities[1][0]
        ]
    return response


def create_activity(payload):
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


def enroll_activity(payload, token):
    db = db_service.DBService()
    active_id = payload['id']
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    db.enroll_activity(active_id, user_id)
    return None


def cancel_enroll_activity(payload, token):
    db = db_service.DBService()
    active_id = payload['activityId']
    users = auth_token.authed_users
    for user in users:
        if user[0] == token:
            user_id = user[1]
            break
    db.cancel_enroll_activity(active_id, user_id)
    return None


def update_activity(payload):
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
