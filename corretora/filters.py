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
    
    CHOICES7 = ((51000, 'Rodotrem'),(39000, 'Bitrem'),(36900, 'Bicaçamba'), (36000, 'Vanderléia'), (33000, 'LS Trucada'),(25500, 'Toco'))
    
    tipo_veiculo_carregado = django_filters.ChoiceFilter(
        label="Tipo Veículo",  choices=CHOICES7, method="tipo_veiculo_carregado_query"
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
    
    obs__icontains = django_filters.CharFilter(
        field_name="obs",
        label="Observação",
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
            "obs": ["icontains"],
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
    
    def tipo_veiculo_carregado_query(self, queryset, name, value):
        return queryset.filter(veiculo=value)
    

    def filtrando_comissao(self, queryset, name, value):
        expression = True if value == "True" else False
        return queryset.filter(pgcomissao=expression)
    
    def com_sem_comissao(self, queryset, name, value):
        if value == "True":
            c = Carga.objects.all()
            qs_ids_1 = [i.id for i in c if i.comissaocasca != None and i.comissaocasca > 0]
            return queryset.filter(id__in=qs_ids_1)
        elif value == "False":
            c = Carga.objects.all()
            qs_ids_2 = [i.id for i in c if i.comissaocasca == None or i.comissaocasca == 0]
            return queryset.filter(id__in=qs_ids_2)
        else:
            return queryset