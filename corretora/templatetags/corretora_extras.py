from django import template

register = template.Library()

import calendar
from datetime import datetime

import locale
import time


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


nomes = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


@register.filter
def nome_mes(datemont):

    numeromes = datetime.now().month
    mes = nomes.get(numeromes)
    return mes


@register.filter
def nome_mes_anterior(datemont):

    numeromes = datetime.now().month
    if numeromes == 1:        
        return nomes.get(12)
    else:
        mesanterior = numeromes - 1
        return nomes.get(mesanterior)


@register.filter
def nome_mes_anteanterior(datemont):

    numeromes = datetime.now().month
    if numeromes == 1:        
        return nomes.get(11)
    else:
        mesanterior = numeromes - 2
        return nomes.get(mesanterior)


@register.filter
def nome_mes_tresanterior(datemont):

    numeromes = datetime.now().month
    if numeromes == 1:        
        return nomes.get(10)
    else:
        mestresanterior = numeromes - 3
        return nomes.get(mestresanterior)

