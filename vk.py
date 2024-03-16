import os

import requests
from dotenv import find_dotenv, load_dotenv

from classes import VKApiError


load_dotenv(find_dotenv())
token = os.getenv('ACCESS_TOKEN')


def build_vk_api_request_url(method: str, vk_user_id: int | str, params: dict | None = None) -> str:
    url = f"https://api.vk.com/method/{method}?user_id={vk_user_id}&access_token={token}&v=5.191"
    if params is not None:
        param_string = ''
        for param_name, param_value in params.items():
            param_string += f'&{param_name}={param_value}'
        url += param_string
    return url


def get_friends(user_id: str) -> list[dict]:
    vk_friends_response = requests.get(
        build_vk_api_request_url(
            method="friends.get",
            params={"fields": "bdate"},
            vk_user_id=user_id
        )
    ).json()
    try:
        if 'error' in vk_friends_response:
            raise VKApiError(vk_friends_response["error"])
        return vk_friends_response["response"]["items"]
    except Exception as e:
        print(f'Возникла ошибка: {e.__class__.__name__}: {e}.')


def get_vk_user_id_by_shortname(shortname: str) -> int:
    vk_user_response = requests.get(
        build_vk_api_request_url(
            method="users.get",
            params={"user_ids": shortname, "fields": "screen_name"},
            vk_user_id=shortname
        )
    ).json()
    return vk_user_response['response'][0]['id']
