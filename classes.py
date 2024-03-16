from datetime import datetime
from dataclasses import dataclass


@dataclass
class Friend:
    name: str
    birthday: str | datetime


class InternetConnectionError(Exception):
    pass


class VKApiError(Exception):
    pass
