from django import forms
from django.core.mail.message import EmailMessage
from django.utils.translation import gettext_lazy as _

class ContatoForm(forms.Form):
    nome = forms.CharField(label=_('Nome'), max_length=100)
    email = forms.EmailField(label=_('E-mail'), max_length=100)
    mensagem = forms.CharField(label=_('Mensagem'), widget=forms.Textarea())
    assunto = forms.CharField(label=_('Assunto'), max_length=100, required=False)
    
    def send_mail(self): 
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        mensagem = self.cleaned_data['mensagem']
        assunto = self.cleaned_data['assunto']

        n = _('nome')
        e = _('email')
        m = _('mensagem')
        a = _('assunto')

        if assunto == "":
            conteudo = f'{n}: {nome}\n{e}: {email}\n{m}: {mensagem}'
        else:
            conteudo = f'Nome: {nome}\nE-mail: {email}\nTelefone: {mensagem}\nInteresse: {assunto}'
        
        mail = EmailMessage(
            subject=nome,
            body=conteudo,
            from_email='contato@gdourado.com.br',
            to=['contato@gdourado.com.br',],
            headers={'Reply-To': email}
        )
        mail.send()
    
    