import django_filters
from django_filters import *
from .models import *
from django import forms
from django.db.models import Q

# https://youtu.be/nle3u6Ww6Xk


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass



class CargasFilter(django_filters.FilterSet):

    CHOICES = (("crescente", "Crescente"), ("decrescente", "Decrescente"))

    ordering = django_filters.ChoiceFilter(
        label="Data Orden.", choices=CHOICES, method="filter_by_order"
    )
    
    CHOICES2 = (('False', 'Aberto'),('True', 'Pago'))
    
    
    pgcomissaoa = django_filters.ChoiceFilter(
        field_name="pgcomissao",   label="Comissão",  choices=CHOICES2, method="filtrando_comissao"
    )
    
    CHOICES3 = (('True', 'Contém'),('False', 'Não Contém'))
    
    
    comcomissao = django_filters.ChoiceFilter(
        label="Comissão ?",  choices=CHOICES3, method="com_sem_comissao"
    )

    CHOICES4 = (('True', 'Contém'),('False', 'Não Contém'))
    
    com_comissao_frete = django_filters.ChoiceFilter(
        label="Comi. F. ?",  choices=CHOICES4, method="com_sem_comissao_f"
    )
    
    CHOICES5 = (('True', 'Contém'),('False', 'Não Contém'))
    
    com_comprovante_descarga = django_filters.ChoiceFilter(
        label="Comp. D. ?",  choices=CHOICES5, method="com_comprovante_d"
    )
    
    CHOICES6 = (('True', 'Faturado'),('False', 'Não Fat'))
    
    com_fatura_terceiros = django_filters.ChoiceFilter(
        label="Fat. Terc. ?",  choices=CHOICES6, method="frete_com_fatura"
    )
    
    

    transp = django_filters.ModelMultipleChoiceFilter(
        queryset=Transportadora.objects.order_by("nome").all(),
        widget=forms.CheckboxSelectMultiple,
    )

    pedido__produto__icontains = django_filters.CharFilter(
        field_name="pedido__produto", label="Produto", lookup_expr="icontains",
    )

    motorista__icontains = django_filters.CharFilter(
        field_name="motorista", label="Motorista", lookup_expr="icontains",
    )
    placa__icontains = django_filters.CharFilter(
        field_name="placa", label="Placa", lookup_expr="icontains"
    )
    data = django_filters.DateFilter(
        field_name="data", label="Data =", lookup_expr="exact"
    )
    data__gte = django_filters.DateFilter(
        field_name="data", label="Data >=", lookup_expr="gte"
    )
    data__lte = django_filters.DateFilter(
        field_name="data", label="Data <=", lookup_expr="lte"
    )
    
    data_agenda = django_filters.DateFilter(
        field_name="data_agenda", label="Descarga =", lookup_expr="exact"
    )
    data_agenda__gte = django_filters.DateFilter(
        field_name="data_agenda", label="Descarga >=", lookup_expr="gte"
    )
    data_agenda__lte = django_filters.DateFilter(
        field_name="data_agenda", label="Descarga <=", lookup_expr="lte"
    )

    notafiscal__icontains = django_filters.CharFilter(
        field_name="notafiscal", label="Nota Fiscal", lookup_expr="icontains"
    )

    pedido__fornecedor__nome__icontains = django_filters.CharFilter(
        field_name="pedido__fornecedor__nome",
        label="Fornecedor",
        lookup_expr="icontains",
    )
    pedido__cliente__nome_fantasia__icontains = django_filters.CharFilter(
        field_name="pedido__cliente__nome_fantasia",
        label="Cliente",
        lookup_expr="icontains",
    )

    pedido__contrato__icontains = django_filters.CharFilter(
        field_name="pedido__contrato", label="Contrato", lookup_expr="icontains",
    )

    CHOICES_SITUACAO = (('Agendado', 'Agendado'),('Carregado', 'Carregado'))
    
    
    situacao = django_filters.ChoiceFilter(
        field_name="situacao",   label="Situação",  choices=CHOICES_SITUACAO
    )    
    
    
    peso__icontains = django_filters.NumberFilter(
        field_name="peso", label="Peso =", lookup_expr="icontains"
    )
    peso__gte = django_filters.NumberFilter(
        field_name="peso", label="Peso >=", lookup_expr="gte"
    )
    peso__lte = django_filters.NumberFilter(
        field_name="peso", label="Peso <=", lookup_expr="lte"
    )

    valornf__icontains = django_filters.NumberFilter(
        field_name="valornf", label="Valor NF", lookup_expr="icontains"
    )
    valornf__gte = django_filters.NumberFilter(
        field_name="valornf", label="Valor NF >=", lookup_expr="gte"
    )
    valornf__lte = django_filters.NumberFilter(
        field_name="valornf", label="Valor NF <=", lookup_expr="lte"
    )

    pedido__fornecedor__cidade__cidade__icontains = django_filters.CharFilter(
        field_name="pedido__fornecedor__cidade__cidade",
        label="Cidade",
        lookup_expr="icontains",
    )
    
    fatura_frete_terceiros__numero__icontains = django_filters.CharFilter(
        field_name="fatura_frete_terceiros__numero",
        label="Fatura Nº",
        lookup_expr="icontains",
    )

    class Meta:
        model = Carga
        fields = {
            "motorista": ["icontains"],
            "placa": ["icontains"],
            "data": ["gte", "lte", "exact"],
            "data_agenda": ["gte", "lte", "exact"],
            "valornf": ["gte", "lte", "icontains"],
            "notafiscal": ["icontains"],
            "pedido__fornecedor__nome": ["icontains"],
            "pedido__cliente__nome_fantasia": ["icontains"],
            "pedido__contrato": ["icontains"],            
            "peso": ["icontains", "gte", "lte"],
            "pedido__fornecedor__cidade__cidade": ["icontains"],
            "fatura_frete_terceiros__numero": ["icontains"],
        }

    def filter_by_order(self, queryset, name, value):
        expression = "data" if value == "crescente" else "-data"
        return queryset.order_by(expression)
    
    def com_sem_comissao_f(self, queryset, name, value):
        expression = True if value == "True" else False
        return queryset.filter(gera_comi_frete=expression)
    
    def com_comprovante_d(self, queryset, name, value):
        if value == "True":
            return queryset.filter(comprovante_descarga__startswith='/correto')
        else:
            return queryset.filter(~Q(comprovante_descarga__startswith='/correto'))
    
    def frete_com_fatura(self, queryset, name, value):
        expression = ~Q(fatura_frete_terceiros=None) if value == "True" else Q(fatura_frete_terceiros=None)
        return queryset.filter(expression).filter(comi_frete_total__gt=0)
    

    def filtrando_comissao(self, queryset, name, value):
        qs = set()
        c = Carga.objects.all()
        for i in c:
            if i.comissaocasca != None:
                if i.comissaocasca > 0:
                    qs.add(i.id)        
        expressa = "True" if value == "True" else "False"
        return queryset.filter(id__in=qs).filter(pgcomissao=expressa)
    
    def com_sem_comissao(self, queryset, name, value):
        qs = set()
        qs2 = set()
        c = Carga.objects.all()
        for i in c:
            if i.comissaocasca != None:
                if i.comissaocasca > 0:
                    qs.add(i.id)        
                else:
                    qs2.add(i.id)
            else:
                qs2.add(i.id)
        if value == "True":
            return queryset.filter(id__in=qs)
        elif value == "False":
            return queryset.filter(id__in=qs2)
        else:
            return queryset