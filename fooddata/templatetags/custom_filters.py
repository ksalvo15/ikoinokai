from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Filter to get dictionary value by key."""
    return dictionary.get(key)