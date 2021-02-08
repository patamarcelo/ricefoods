from django import template

register = template.Library()

import calendar

from datetime import timedelta 
from datetime import datetime
# import datetime
import dateutil.relativedelta

import locale
import time

today = datetime.now()

class CounterNode(template.Node):

  def __init__(self):
    self.count = 0

  def render(self, context):
    self.count += 1
    return self.count

@register.tag
def contador(parser, token):
  return CounterNode()

@register.filter
def dias_da_semana(teste): 
    dias_escritos=["Segunda-Feira","Terça-Feira","Quarta-Feira","Quinta-Feira","Sexta-Feira","Sábado","Domingo"]
    semana_atual = {}
    semana_seguinte = {}            
    for i in range(7):
        data_atual = today if today.weekday() == i else today - timedelta(days=today.weekday() - i)
        dia_da_semana_numero = data_atual.weekday()
        data_atual_timestamp = data_atual.timestamp()
        day_fromtmsp = datetime.fromtimestamp(data_atual_timestamp)
        data_atual_humana = day_fromtmsp.strftime("%d/%m/%Y") 
        dia_escrito = dias_escritos[dia_da_semana_numero]
        semana_atual[dia_escrito] = data_atual_humana                    
    for i in range(7):
        data_atual = (today + timedelta(days=7)) if today.weekday() == i else (today + timedelta(days=7)) - timedelta(days=today.weekday() - i)
        dia_da_semana_numero = data_atual.weekday()
        data_atual_timestamp = data_atual.timestamp()
        day_fromtmsp = datetime.fromtimestamp(data_atual_timestamp)
        data_atual_humana = day_fromtmsp.strftime("%d/%m/%Y") 
        dia_escrito = dias_escritos[dia_da_semana_numero]
        semana_seguinte[dia_escrito] = data_atual_humana           
    
    
    return semana_atual, semana_seguinte

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
    monthdelta = dateutil.relativedelta.relativedelta(months=1)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)


@register.filter
def nome_mes_conforme_dict(datemont):
    variavel = datemont
    print(variavel)
    numerodomes = datemont.split('-')[-1]        
    print(f'Numero do mes: {numerodomes} - {type(numerodomes)}')
    return nomes.get(int(numerodomes))

@register.filter
def nome_mes_anteanterior(datemont):    
    monthdelta = dateutil.relativedelta.relativedelta(months=2)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes) 


@register.filter
def nome_mes_tresanterior(datemont):
    monthdelta = dateutil.relativedelta.relativedelta(months=3)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)

@register.filter
def nome_mes_quatroanterior(datemont):    
    monthdelta = dateutil.relativedelta.relativedelta(months=4)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)

@register.filter
def nome_mes_cincoanterior(datemont):    
    monthdelta = dateutil.relativedelta.relativedelta(months=5)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)

@register.filter
def nome_mes_seisanterior(datemont):    
    monthdelta = dateutil.relativedelta.relativedelta(months=6)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)

@register.filter
def nome_mes_seteanterior(datemont):    
    monthdelta = dateutil.relativedelta.relativedelta(months=7)    
    numeromes = datetime.now() - monthdelta    
    numeromes = numeromes.month
    return nomes.get(numeromes)

