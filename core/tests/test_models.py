import uuid
from django.test import TestCase
from model_mommy import mommy

from core.models import get_file_path

class GetFilePathTestCase(TestCase):

    def setUp(self):
        self.filename = f'{uuid.uuid4()}.png'

    def test_get_file_path(self):
        arquivo = get_file_path(None, 'teste.png')
        self.assertTrue(len(arquivo), len(self.filename))

class ServicosTestCase(TestCase):

    def setUp(self):
        self.servico = mommy.make('Servicos')

    def test_str(self):
        self.assertEquals(str(self.servico), self.servico.servico)

class SubservicosTestCase(TestCase):

    def setUp(self):
        self.subservico = mommy.make('Subservicos')

    def test_str(self):
        self.assertEquals(str(self.subservico), self.subservico.subservico)


class InicialTestCase(TestCase):

    def setUp(self):
        self.inicio = mommy.make('Inicial')

    def test_str(self):
        self.assertEquals(str(self.inicio), self.inicio.inicio)

class SobreTestCase(TestCase):

    def setUp(self):
        self.titulo = mommy.make('Sobre')

    def test_str(self):
        self.assertEquals(str(self.titulo), self.titulo.titulo)

class SobretopicoTestCase(TestCase):

    def setUp(self):
        self.sobretopico = mommy.make('Sobretopico')

    def test_str(self):
        self.assertEquals(str(self.sobretopico), self.sobretopico.sobretopico)

class ProjetosTestCase(TestCase):

    def setUp(self):
        self.titulo = mommy.make('Projetos')

    def test_str(self):
        self.assertEquals(str(self.titulo), self.titulo.titulo)

class SubprojetosTestCase(TestCase):

    def setUp(self):
        self.titulo = mommy.make('Subprojetos')

    def test_str(self):
        self.assertEquals(str(self.titulo), self.titulo.titulo)
