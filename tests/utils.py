import datetime


def set_up_mock_auth_post(mock_post):
    access_timestamp = int(datetime.datetime.now().timestamp())

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        'access': 'access_token',
        'refresh': 'refresh_token',
        'accessExpiresAt': access_timestamp,
        'refreshExpiresAt': access_timestamp + 3600
    }

    return mock_post
