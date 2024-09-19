# core/templatetags/custom_filters.py


import base64
from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    if value:
        return [item.strip() for item in value.split(delimiter)]
    return []

@register.filter
def b64encode(value):
    return base64.b64encode(value).decode('utf-8')