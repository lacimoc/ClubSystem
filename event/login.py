from utils import auth_token, template
import copy


def login(payload: dict) -> None:
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
