from django import template

register = template.Library()

import calendar
from datetime import datetime

import locale
import time

@register.filter
def nome_mes(datemont):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    numeromes = datetime.now().month
    mes = calendar.month_name[numeromes] 
    return mes

@register.filter
def nome_mes_anterior(datemont):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    numeromes = datetime.now().month
    if numeromes == 1:
        mesanterior == 12
        return calendar.month_name[mesanterior] 
    else:
        mesanterior = numeromes - 1
        return calendar.month_name[mesanterior]

@register.filter
def nome_mes_anteanterior(datemont):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    numeromes = datetime.now().month
    if numeromes == 1:
        mesanterior == 11
        return calendar.month_name[mesanterior] 
    else:
        mesanterior = numeromes - 2
        return calendar.month_name[mesanterior]


        


        