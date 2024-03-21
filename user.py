import json
from pathlib import Path


def make_info_file_path() -> Path:
    info_file_path = Path('info.json')
    info_file_path.touch()
    if not open(info_file_path).readline():
        with open(info_file_path, 'w') as info_file:
            info_file.write('""')
    return info_file_path


def get_saved_user_id() -> int:
    info_file_path = make_info_file_path()
    with open(info_file_path) as info_file:
        uid = json.load(info_file)
    return uid


def save_user_id(uid: int) -> None:
    info_file_path = make_info_file_path()
    with open(info_file_path, 'w') as info_file:
        json.dump(uid, info_file, indent=4)
