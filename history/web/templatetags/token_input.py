from django import template

register = template.Library()


@register.inclusion_tag('components/token.html')
def token_input(_token):
    return {'token': _token}
