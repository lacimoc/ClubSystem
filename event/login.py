from utils import auth_token
from settings import template
import copy


def login(payload: dict) -> dict:
    """
    通过用户名和密码的表单登录，成功返回token，失败返回401错误模版
    :param payload: 包含用户名和密码的表单
    :return: 含有token的表单
    """
    try:
        username = payload['username']
        password = payload['password']
    except KeyError:
        ret_payload = copy.deepcopy(template.response_template)
        ret_payload['code'] = 401
        ret_payload['data']['token'] = ''
        return ret_payload
    access_token = auth_token.login(username, password)
    if access_token != '':
        ret_payload = copy.deepcopy(template.response_template)
        ret_payload['data']['token'] = access_token
        return ret_payload
    else:
        ret_payload = copy.deepcopy(template.response_template)
        ret_payload['code'] = 401
        ret_payload['data']['token'] = access_token
        return ret_payload
