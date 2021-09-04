from django import forms
from django.core.mail.message import EmailMessage
from .models import *


class CompDescargaForm(forms.ModelForm):

    comprovante_descarga = forms.FileField(label="Arquivo")
    data_descarga = forms.DateField(label="Data Descarga", required=False)
    obs_descarga = forms.CharField(
        label="Observação Descarga", widget=forms.Textarea(), required=False
    )

    class Meta:
        model = Carga
        fields = ("comprovante_descarga", "data_descarga", "obs_descarga")


class EnvianotafiscalForm(forms.ModelForm):

    nota_fiscal_arquivo = forms.FileField(label="Nota Fiscal", help_text="Somente arquivo PDF")
    nota_fiscal_xml = forms.FileField(label="XML NF", required=False, help_text="Somente arquivo XML")
    obs = forms.CharField(label="Observação", widget=forms.Textarea(), required=False)

    class Meta:
        model = Carga
        fields = (
            "nota_fiscal_arquivo",
            "nota_fiscal_xml",
            "obs",
        )

