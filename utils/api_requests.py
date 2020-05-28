import requests

from .config_parser import parse_config


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
    if response.status_code != 200:
        return response.status_code, {}
    else:
        return response.status_code, response.json()


def obtain_token(username, password):
    body = {'username': username, 'password': password}
    return post('auth', 'obtain_token', body)


def refresh_token(refresh):
    body = {'refresh': refresh}
    return post('auth', 'refresh_token', body)
