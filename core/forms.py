from django import forms
from django.core.mail.message import EmailMessage

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())
    assunto = forms.CharField(label='Assunto', max_length=100, required=False)
    
    def send_mail(self): 
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        mensagem = self.cleaned_data['mensagem']
        assunto = self.cleaned_data['assunto']


        if assunto == "":
            conteudo = f'Nome: {nome}\nE-mail: {email}\nMensagem: {mensagem}'
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
    
    