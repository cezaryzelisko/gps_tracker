import requests

from gps_tracker.utils.config_parser import parse_config

SAFE_STATUS_CODES = [200, 201]


def get_url(section, option):
    endpoints = parse_config()['endpoints']
    return '/'.join([endpoints['root'], section, endpoints[section][option]])


def post(section, option, body, additional_headers=None, additional_cookies=None):
    url = get_url(section, option)
    headers = {'Content-Type': 'application/json'}
    cookies = {}
    if additional_headers:
        headers.update(additional_headers)
    if additional_cookies:
        cookies.update(additional_cookies)
    response = requests.post(url, json=body, headers=headers, cookies=cookies)
    if response.status_code in SAFE_STATUS_CODES:
        return response.status_code, response.json()
    else:
        return response.status_code, {}


def obtain_token(username, password):
    body = {'username': username, 'password': password}
    return post('auth', 'obtain_token', body)


def refresh_token(refresh):
    body = {'refresh': refresh}
    return post('auth', 'refresh_token', body)
