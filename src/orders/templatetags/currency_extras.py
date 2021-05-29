from django import template
import locale

register = template.Library()


@register.filter
def currencier(pesos):
    try:
        locale.setlocale(locale.LC_ALL, 'es_AR')
        return locale.currency(pesos)
    except TypeError:
        return locale.currency(pesos[0])
