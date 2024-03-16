from datetime import datetime

import requests

from friends import load_friends_list, get_friends_from_json
from utils import format_friends_list, get_friends_text, get_next_bdays_text
from user import get_saved_user_id, save_user_id
from vk import get_vk_user_id_by_shortname
from rich.console import Console
from rich.panel import Panel


vk_user_id = get_saved_user_id()

now = datetime.now()
console = Console()


def print_friends(friends: list) -> None:
    friends_text = get_friends_text(friends)
    console.print(
        Panel.fit(friends_text, title=f'Дни рождения (всего {len(friends)})')
    )


def print_next_bdays(friends: list) -> None:
    console.print(
        Panel.fit(get_next_bdays_text(friends), title='5 ближайших дней рождения')
    )


def parse_friends(user_id: int | str, reload: bool = False, next_birthday: bool = False) -> None:
    friends = load_friends_list(user_id=user_id if reload else None)
    if user_id != vk_user_id:
        save_user_id(user_id)
    format_friends_list(friends)
    if friends:
        print_friends(friends)
        if next_birthday:
           print_next_bdays(friends) 
        


def parse_friends_offline(next_birthday: bool = False):
    friends = get_friends_from_json()
    format_friends_list(friends)
    if friends:
        print_friends(friends)
        if next_birthday:
           print_next_bdays(friends) 


def ask_next_bday() -> bool:
    next_bday_input_text = '[b]Показать друзей с ближайшими днями рождения?[/b] [[green]1[/green] - да, [red]0[/red] - нет] '
    return console.input(next_bday_input_text) == '1'


def main():  
    try:
        requests.get('https://google.com')
    except requests.exceptions.ConnectionError:
        print(' * Программа работает в оффлайн-режиме * ')
        next_bday = ask_next_bday()
        parse_friends_offline(next_birthday=next_bday)
    else:
        reload = console.input('[b]Обновить данные?[/b] [[green]1[/green] - да, [red]0[/red] - нет] ') == '1'
        if reload:
            input_user_id = console.input(
                'Если хотите посмотреть данные другого пользователя, введите его [b]короткое имя[/b] или [b]ID[/b] в VK.\n'
                '🛈 Если пользователя менять не нужно, нажмите [i]Enter[/i], чтобы пропустить. '
            )
            if input_user_id.isdigit():
                user_id = int(input_user_id)
            else:
                if input_user_id:
                    user_id = get_vk_user_id_by_shortname(shortname=input_user_id)
                else:
                    user_id = ''
        elif not reload or not input_user_id:
            user_id = get_saved_user_id() 
        next_bday = ask_next_bday()
        parse_friends(user_id, reload=reload, next_birthday=next_bday)


if __name__ == '__main__':
    main()