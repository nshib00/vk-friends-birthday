import json
from datetime import datetime

from classes import Friend

now = datetime.now()
today = f'{now.day}.{now.month}'


def year_is_leap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def get_next_friend_birthday_datetime(friend: Friend) -> datetime:
    bday = int(friend.birthday.split('.')[0])
    bmonth = int(friend.birthday.split('.')[1])
    if bmonth < now.month or (bmonth == now.month and bday < now.day):
        byear = now.year + 1
    else:
        byear = now.year
    if bday == 29 and bmonth == 2 and not year_is_leap(byear):
        # если день рождения у друга выпадает на 29 февраля невисокосного года, переносим день рождения на 1 марта
        return datetime(day=1, month=3, year=byear)
    return datetime(day=int(bday), month=int(bmonth), year=byear)

 
def replace_bday_strings_to_datetime(friends_list: list[Friend]) -> None:
    for friend in friends_list:
        friend.birthday = get_next_friend_birthday_datetime(friend) # дата следующего дня рождения в datetime


def sort_friends_by_bday(friends_list: list[Friend]) -> None:
    for i in range(len(friends_list)):
        for j in range(i+1, len(friends_list)):
            if friends_list[j].birthday < friends_list[i].birthday:
                friends_list[j], friends_list[i] = friends_list[i], friends_list[j]


def replace_non_existing_bdays(friends_list: list[Friend]) -> None:
    ''' Заменяет объект datetime с несуществующим днем рождения у друзей, у которых ДР не указан в профиле,
    на строку "День рождения не указан".
    '''
    for friend in friends_list:
        if friend.birthday == datetime(day=1, month=1, year=9999):
            friend.birthday = "День рождения не указан"


def format_friends_list(friends_list: list[Friend]) -> None:
    replace_bday_strings_to_datetime(friends_list)
    sort_friends_by_bday(friends_list)
    replace_non_existing_bdays(friends_list)


def friend_obj_to_dict(friend: Friend) -> dict[str]:
    return {'name': friend.name, 'bdate': friend.birthday}


def dict_to_friend_obj(friend_dict: dict) -> Friend:
    if friend_dict.get('bdate') is None:
        friend_dict['bdate'] = '1.1.9999'
    return Friend(
        name=friend_dict['first_name'] + ' ' + friend_dict['last_name'],
        birthday=friend_dict['bdate']
    )


def get_friends_text(friends_list: list[Friend]) -> str:
    text = ''
    for friend in friends_list:
        if friend.birthday == "День рождения не указан":
            text += friend.name + ' -> ' + friend.birthday
        else:
            bday = friend.birthday
            bday_yymmdd = f"{bday.day}.{bday.month}.{bday.year}"
            text += f'[b]{friend.name}[/]' + ' -> ' + bday_yymmdd + '\n'
    return text


def get_friend_bday_text(friend: Friend, delta: int) -> str:
    if delta == 0:
        return '[bold green]сегодня[/]'
    elif delta == 1:
        return '[bold yellow]завтра[/]'
    elif delta % 10 in (2, 3, 4):
        return f'через [bold #f05729]{delta}[/] дня'
    elif delta % 10 == 1 and delta >= 21:
        return f'через [bold #f05729]{delta}[/] день'
    else:
        return f'через [bold #f05729]{delta}[/] дней'


def get_next_bdays_text(friends_list: list[Friend]) -> str:
    all_friends_text = ''
    for friend in friends_list[:5]:
        delta = (friend.birthday - now).days + 1
        bday_text = get_friend_bday_text(friend, delta)
        all_friends_text += f'[b]{friend.name}[/] -> {bday_text}\n'
    return all_friends_text
