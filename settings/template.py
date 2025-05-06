response_template = {
    'code': 200,
    'msg': 'ok',
    'data': {}
}

unauthorized_template = {
    'code': 401,
    'msg': 'Unauthorized',
    'data': {}
}

activity_template = {
    "total": 15,
    "current_page": 1,
    "page_size": 10,
    "activities": [
        {
            "id": "act_001",
            "title": "前端技术交流会",
            "cover": "http://127.0.0.1:5000/static/zayu.png",
            "status": "registered",
            "time": "2024-03-20T14:00:00Z",
            "location": "线上会议",
            "registration_time": "2024-03-15T09:30:00Z",
            "max_participants": 100,
            "current_participants": 85
        }
    ]
}

activity_detail_template = [
    {
        "id": "act_001",
        "title": "Vue3技术研讨会",
        "cover": "http://127.0.0.1:5000/static/zayu.png",
        "startTime": "2024-03-25T09:00:00Z",
        "endTime": "2024-03-25T17:00:00Z",
        "location": "线上会议",
        "capacity": 100,
        "enrolled": 85,
        "status": "upcoming",
        "description": "深入探讨Vue3最新特性...",
        "department": "技术部"
    }
]
