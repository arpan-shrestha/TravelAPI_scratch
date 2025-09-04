from django.shortcuts import render
import secrets, datetime


def generate_token(user, with_refresh=True):
    access_token = secrets.token_urlsafe(32)
    now = datetime.datetime.now()
    access_token_expire = now + datetime.timedelta(hours=1)

    token_data = {
        "access_token":access_token,
        "access_token_expire":access_token_expire,    
    }

    if with_refresh:
        refresh_token = secrets.token_urlsafe(32)
        refresh_token_expire = now +datetime.timedelta(days=15)
        token_data.update({
            "refresh_token":refresh_token,
            "refresh_token_expire":refresh_token_expire,
        })
    return token_data


