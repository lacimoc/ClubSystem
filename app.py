import uuid

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import event.activity
import event.password
import event.user
from event import login, export_excel
from utils import auth_token

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "https://home.icuhome.space:12006"}})


# 获取用户信息
@app.route('/api/getUserInfo')
def api_get_user_info():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        return jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        api_get_user_info_response = jsonify(
            event.user.get_user_info(request.headers.get('Authorization').split('Bearer ')[1]))
        return api_get_user_info_response
    else:
        return jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})


# 获取用户活动
@app.route('/api/getUserActivities', methods=['GET', 'POST'])
def api_get_user_activities():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_get_user_activities_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_user_activities_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        try:
            api_get_user_activities_response = jsonify(
                event.activity.get_user_activity_info(request.headers.get('Authorization').split('Bearer ')[1]))
            return api_get_user_activities_response
        except Exception as e:
            import traceback
            traceback.print_exc()
            api_get_user_activities_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_get_user_activities_response
    else:
        api_get_user_activities_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_user_activities_response


# 删除已报名的活动
@app.route('/api/deleteActivity', methods=['GET', 'POST'])
def api_delete_activity():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_delete_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_delete_activity_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.activity.delete_activity(payload)
            return jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        except Exception as e:
            api_delete_activity_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_delete_activity_response
    else:
        api_delete_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_delete_activity_response


# 获取所有活动
@app.route('/api/getActivities', methods=['GET', 'POST'])
def api_get_activities():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_get_activities_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_activities_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        api_get_activities_response = jsonify(
            event.activity.get_activities_info(request.headers.get('Authorization').split('Bearer ')[1]))
        return api_get_activities_response
    else:
        api_get_activities_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_activities_response


# 登录
@app.route('/api/auth/login', methods=['GET', 'POST'])
def api_auth_login():
    payload = request.get_json()
    api_auth_login_response = jsonify(login.login(payload))
    return api_auth_login_response


# 获取部门
@app.route('/api/getDepartments', methods=['GET', 'POST'])
def api_get_departments():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_get_departments_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_departments_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        api_get_departments_response = jsonify({'code': 200, 'msg': 'ok', 'data': ['技术部', '办公室部', '策划部', '财务部', '电竞部', '社务部', '宣传部']})
        return api_get_departments_response
    else:
        api_get_departments_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_departments_response


# 创建活动
@app.route('/api/createActivity', methods=['GET', 'POST'])
def api_create_activity():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_create_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_create_activity_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.activity.create_activity(payload)
        except Exception as e:
            api_create_activity_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_create_activity_response
        api_create_activity_response = jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        return api_create_activity_response
    else:
        api_create_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_create_activity_response


# 上传图片
@app.route('/api/upload', methods=['GET', 'POST'])
def api_upload():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_upload_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_upload_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        file = request.files['file']
        file_name = str(uuid.uuid4())
        file_path = './static/uploads/' + file_name + '.jpg'
        file.save(file_path)
        api_upload_response = jsonify({'code': 200, 'msg': 'ok', 'data': {'url': 'https://home.icuhome.space:12007/static/uploads/' + file_name + '.jpg'}})
        return api_upload_response
    else:
        api_upload_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_upload_response


# 注册活动
@app.route('/api/enrollActivity', methods=['GET', 'POST'])
def api_enroll_activity():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_enroll_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_enroll_activity_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.activity.enroll_activity(payload, request.headers.get('Authorization').split('Bearer ')[1])
            return jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        except Exception as e:
            api_enroll_activity_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_enroll_activity_response
    else:
        api_enroll_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_enroll_activity_response


# 获取所有用户
@app.route('/api/getUsers', methods=['GET', 'POST'])
def api_get_users():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_get_users_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_users_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        api_get_users_response = jsonify(event.user.get_all_users())
        return api_get_users_response
    else:
        api_get_users_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_get_users_response


# 创建用户
@app.route('/api/createUser', methods=['GET', 'POST'])
def api_create_user():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_create_user_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_create_user_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.user.add_user(payload)
        except Exception as e:
            api_create_user_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_create_user_response
        api_create_user_response = jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        return api_create_user_response
    else:
        api_create_user_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_create_user_response


# 删除用户
@app.route('/api/deleteUser', methods=['GET', 'POST'])
def api_delete_user():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_delete_user_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_delete_user_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.user.delete_user(payload)
        except Exception as e:
            api_delete_user_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_delete_user_response
        api_delete_user_response = jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        return api_delete_user_response
    else:
        api_delete_user_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_delete_user_response


# 重置密码
@app.route('/api/resetPassword', methods=['GET', 'POST'])
def api_reset_password():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_reset_password_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_reset_password_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.password.reset_password(payload)
        except Exception as e:
            api_reset_password_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_reset_password_response
        api_reset_password_response = jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        return api_reset_password_response
    else:
        api_reset_password_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_reset_password_response


# 取消报名
@app.route('/api/cancelActivity', methods=['GET', 'POST'])
def api_cancel_activity():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_cancel_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_cancel_activity_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.activity.cancel_enroll_activity(payload, request.headers.get('Authorization').split('Bearer ')[1])
            return jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        except Exception as e:
            api_cancel_activity_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_cancel_activity_response
    else:
        api_cancel_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_cancel_activity_response


# 更新活动信息
@app.route('/api/updateActivity', methods=['GET', 'POST'])
def api_update_activity():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_update_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_update_activity_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.activity.update_activity(payload)
        except Exception as e:
            api_update_activity_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_update_activity_response
        api_update_activity_response = jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        return api_update_activity_response
    else:
        api_update_activity_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_update_activity_response


# 更改密码
@app.route('/api/changePassword', methods=['GET', 'POST'])
def api_change_password():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_change_password_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_change_password_response

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        payload = request.get_json()
        try:
            event.password.change_password(payload, request.headers.get('Authorization').split('Bearer ')[1])
            return jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        except Exception as e:
            api_change_password_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_change_password_response
    else:
        api_change_password_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_change_password_response


# 导出excel
@app.route('/api/export', methods=['GET', 'POST'])
def api_export():
    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == 'Bearer':
        api_export_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_export_response

    if not auth_token.admin_auth(request.headers.get('Authorization').split('Bearer ')[1]):
        return jsonify({'code': 403, 'msg': 'Permission denied', 'data': {}})

    if auth_token.auth(request.headers.get('Authorization').split('Bearer ')[1]):
        try:
            payload = request.get_json()
            file_name = export_excel.export(payload['activity_id'])
            if file_name == '':
                return jsonify({'code': 200, 'msg': 'ok', 'data': {}})
        except Exception as e:
            import traceback
            traceback.print_exc()
            api_export_response = jsonify({'code': 500, 'msg': str(e), 'data': {}})
            return api_export_response
        api_export_response = send_file(f'./static/form/{file_name}', as_attachment=True)
        return api_export_response
    else:
        api_export_response = jsonify({'code': 401, 'msg': 'Unauthorized', 'data': {}})
        return api_export_response


# 静态路由
@app.route('/static/<path:path>', methods=['GET', 'POST'])
def static_file(path):
    response = app.send_static_file(path)
    return response


if __name__ == '__main__':
    app.run(port=12008)
