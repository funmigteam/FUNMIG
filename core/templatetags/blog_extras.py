from django import template


register = template.Library()


@register.filter


def split(value, arg):


    if value:


        return [item.strip() for item in str(value).split(arg)]


    return []

