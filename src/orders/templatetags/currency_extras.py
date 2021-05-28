from django import template
import locale

register = template.Library()


@register.filter
def currencier(pesos):
    locale.setlocale(locale.LC_ALL, 'es_AR')
    return locale.currency(pesos)
