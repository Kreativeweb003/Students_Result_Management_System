from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Look up a dict value by a variable key inside a template, e.g.
    {{ existing_results|get_item:student.id }}
    Django templates can't do dictionary[variable] directly, so this fills the gap.
    """
    if not dictionary:
        return None
    return dictionary.get(key)