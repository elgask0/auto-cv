# core/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Splits a string by the given delimiter and trims whitespace.
    Usage in template: {{ value|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(delimiter)]
    return []
