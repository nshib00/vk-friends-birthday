import codecs
import json
import time

from classes import Friend
from utils import dict_to_friend_obj
from vk import get_friends


def load_friends_data_to_json(friends_list: list[dict], update_time: int) -> None:
    minimize_friends_data(friends_list)
    with open('saved_friends.json', 'w', encoding='UTF-8') as friends_file:
        json.dump(
            {'last_time_updated': update_time, 'friends': friends_list},
            friends_file,
            indent=4,
            ensure_ascii=False,
        )


def get_friends_from_json() -> list[Friend]:
    try:
        friends_list = json.load(codecs.open('saved_friends.json', 'r', 'utf-8-sig'))
        return [
            dict_to_friend_obj(f) for f in friends_list['friends']
        ]
    except json.decoder.JSONDecodeError:
        return []


def get_friends_last_update_time() -> int:
    try:
        with open('saved_friends.json', encoding='UTF-8') as friends_file:
            updated = json.load(friends_file)['last_time_updated']
            return updated
    except json.decoder.JSONDecodeError:
        return 0


def load_friends_list(user_id: int | None = None) -> list:
    friends_last_updated = get_friends_last_update_time()
    if time.time() - friends_last_updated > 86400 or user_id is not None:
        # Cписок друзей перезаписывается, если:
        # 1. прошло более 1 дня с момента последнего обновления списка друзей;
        # 2. в программу передан новый user_id.
        print('Выполняется запрос к VK API...')
        friends = get_friends(user_id)
        load_friends_data_to_json(
            friends_list=friends, update_time=int(time.time())
        )
    return get_friends_from_json()


def minimize_friends_data(friends_list: list[dict]) -> None:
    for friend in friends_list:
        if friend.get("deactivated") == "deleted":
            friends_list.remove(friend)
            continue
        for key in ('id', 'track_code', 'can_access_closed', 'is_closed'):
            friend.pop(key)






