from django import template

register = template.Library()


@register.filter('add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter('add_placeholder')
def add_placeholder(value, arg):
    return value.as_widget(attrs={'placeholder': arg})
