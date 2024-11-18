from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Appends a CSS class to form field widgets in templates.
    """
    return value.as_widget(attrs={'class': arg})
