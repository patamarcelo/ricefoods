from django.test import TestCase

from core.forms import ContatoForm

class ContatoFormTestCase(TestCase):

    def setUp(self):
        self.nome = 'Pata'
        self.email = 'Pata@gmail.com'
        self.mensagem = 'mensagem'
        
        self.dados = {
            'nome': self.nome,
            'email': self.email,
            'mensagem': self.mensagem
        }

        self.form = ContatoForm(data=self.dados) #ContatoForm(request.POST)
    
    def test_send_mail(self):
        form1 = ContatoForm(data=self.dados)
        form1.is_valid()
        res1 = form1.send_mail()

        form2 = self.form
        form2.is_valid()
        res2 = form2.send_mail()

        self.assertEquals(res1, res2)