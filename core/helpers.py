from core import Backend


def user_session_by_user(base_url):
    session = Backend(base_url)
    return session
