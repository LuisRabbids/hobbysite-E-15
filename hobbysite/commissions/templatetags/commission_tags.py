from django import template

register = template.Library()

@register.filter(name='get_item') # You can optionally name it here if you want to call it differently in template
def get_item(dictionary, key):
    """
    Allows dictionary item access in Django templates using a variable key.
    Usage: {{ my_dictionary|get_item:my_key_variable }}
    """
    return dictionary.get(key)