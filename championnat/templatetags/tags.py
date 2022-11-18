from dateutil import tz
from django import template

register = template.Library()


@register.simple_tag
def change_timeZone(obj):
    return obj.astimezone(tz=tz.gettz("Africa/Tunis"))
