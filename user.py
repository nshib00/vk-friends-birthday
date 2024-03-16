import json


def get_saved_user_id() -> int:
    with open('info.json') as info_file:
        uid = json.load(info_file)
    return uid


def save_user_id(uid: int) -> None:
    with open('info.json', 'w') as info_file:
        json.dump(uid, info_file, indent=4)
