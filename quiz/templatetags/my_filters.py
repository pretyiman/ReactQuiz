from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter(name='to_uppercase')
def to_uppercase(value):
    return value.upper()
