from django import template


def subtract(value, arg):
    return value - min([e.id for e in arg])+1


register = template.Library()
register.filter('subtract', subtract)
