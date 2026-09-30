from core import Backend


def user_session_by_user(base_url, auth_headers=None, *, verify=True):
    return Backend(base_url, auth_headers=auth_headers, verify=verify)
