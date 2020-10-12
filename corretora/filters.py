import django_filters
from django_filters import *
from .models import *
from django import forms

# https://youtu.be/nle3u6Ww6Xk


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class CargasFilter(django_filters.FilterSet):

    CHOICES = (("crescente", "Crescente"), ("decrescente", "Decrescente"))

    ordering = django_filters.ChoiceFilter(
        label="Data Orden.", choices=CHOICES, method="filter_by_order"
    )

    transp = django_filters.ModelMultipleChoiceFilter(
        queryset=Transportadora.objects.order_by("nome").all(),
        widget=forms.CheckboxSelectMultiple,
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

    situacao__icontains = django_filters.CharFilter(
        field_name="situacao", label="Situação", lookup_expr="icontains",
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

    class Meta:
        model = Carga
        fields = {
            "motorista": ["icontains"],
            "placa": ["icontains"],
            "data": ["gte", "lte", "exact"],
            "valornf": ["gte", "lte", "icontains"],
            "notafiscal": ["icontains"],
            "pedido__fornecedor__nome": ["icontains"],
            "pedido__cliente__nome_fantasia": ["icontains"],
            "pedido__contrato": ["icontains"],
            "situacao": ["icontains"],
            "peso": ["icontains", "gte", "lte"],
            "pedido__fornecedor__cidade__cidade": ["icontains"],
        }

    def filter_by_order(self, queryset, name, value):
        expression = "data" if value == "crescente" else "-data"
        return queryset.order_by(expression)

