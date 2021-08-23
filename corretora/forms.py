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

