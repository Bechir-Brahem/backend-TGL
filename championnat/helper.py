import datetime

from dateutil import tz


def get_now(): return datetime.datetime.now().astimezone(tz=tz.gettz('Africa/Tunis'))
