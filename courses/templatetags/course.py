from django import template

# Registry object where custom tags and filters are registered
register = template.Library()


@register.filter
def model_name(obj):
    """Return the model name of any object, usable as: {{ obj|model_name }}"""
    try:
        # _meta holds the model's metadata; model_name is e.g. 'text', 'video'
        return obj._meta.model_name
    except AttributeError:
        return None