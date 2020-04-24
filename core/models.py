import uuid
from django.db import models

from stdimage.models import StdImageField

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Base(models.Model):
    criados = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo ?', default=True)

    class Meta:
        abstract = True

class Inicial(Base):
    inicio = models.CharField('Ínicio', max_length=100)
    palavras = models.CharField('Palavras', max_length=100)    
    descricao = models.TextField('Descrição', max_length=150)    
    
    class Meta:
        verbose_name = 'Inicial'
        verbose_name_plural = 'Iniciais'

    def __str__(self):
        return self.inicio

class Servicos(Base):

    servico = models.CharField('Servico', max_length=100)
    descricao = models.TextField('Decrição', max_length=100)
    item1 = models.CharField('Item 1', max_length=30)
    item2 = models.CharField('Item 2', max_length=30)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 690, 'height': 398, 'crop': True}})

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.servico

class Subservicos(Base):
    subservico = models.CharField('Subserviço', max_length=100)
    topico1 = models.CharField('Topico 1 ', max_length=100)
    descricao1 = models.TextField('Descrição 1', max_length=140)
    topico2 = models.CharField('Topico 2 ', max_length=100)
    descricao2 = models.TextField('Descrição 2', max_length=140)
    topico3 = models.CharField('Topico 3', max_length=100)
    descricao3 = models.TextField('Descrição 3', max_length=140)

    class Meta:
        verbose_name = 'Subservico'
        verbose_name_plural = 'Subservicos'

    def __str__(self):
        return self.subservico




class Sobre(Base):

    titulo = models.CharField('Titulo', max_length=100)
    texto = models.TextField('Texto', max_length=500)
    pessoa = models.CharField('Pessoa', max_length=40)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 1920, 'height': 1280, 'crop': True}})
    
    class Meta:
        verbose_name = 'Sobre'
        verbose_name_plural = 'Sobre'

    def __str__(self):
        return self.titulo

   

class Sobretopico(Base):
    
    ICONE_CHOICES = (
        ('fa-binoculars', 'binoculos'),
        ('fa-list-alt', 'lista'),
        ('fa-chart-pie', 'grafico pizza'),
        ('fa-truck', 'caminhão'),
        ('fa-warehouse', 'armazem'),
    )
    sobretopico = models.CharField('Tópico', max_length=100)
    descricao = models.TextField('Descrição', max_length=200)
    icone = models.TextField('Icone', max_length=12, choices=ICONE_CHOICES)
    
    
    class Meta:
        verbose_name = 'Sobretopico'
        verbose_name_plural = 'Sobretopicos'

    def __str__(self):
        return self.sobretopico



class Projetos(Base):

    SUB_CHOICES = (
        ('originacao', 'Originação'),
        ('abast', 'Abastecimento'),
        ('impexp', 'Importação e Exportação'),
        ('logistica', 'Logística'),
    )

    LINK_CHOICES = (
        ('project-1', 'projeto1'),
        ('project-2', 'projeto2'),
        ('project-3', 'projeto3'),
        ('project-4', 'projeto4'),
        ('project-5', 'projeto5'),
        ('project-6', 'projeto6'),
        ('project-7', 'projeto7'),
        ('project-8', 'projeto8'),
        
    )

    titulo = models.CharField('Título', max_length=100)
    subtitulo = models.CharField('Subtítulo', max_length=100)
    descricao = models.TextField('Descrição', max_length=250)
    descricao2 = models.TextField('Descrição Paragrafo 2', max_length=250, blank=True)
    area = models.TextField('Area', max_length=12, choices=SUB_CHOICES)
    area2 = models.TextField('Area2', max_length=12, choices=SUB_CHOICES, blank=True)
    area3 = models.TextField('Area3', max_length=12, choices=SUB_CHOICES, blank=True)
    area4 = models.TextField('Area4', max_length=12, choices=SUB_CHOICES, blank=True)
    link = models.TextField('Area', max_length=12, choices=LINK_CHOICES, unique=True)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 722, 'height': 702, 'crop': True}})

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return self.titulo
    

class Subprojetos(Base):
    titulo = models.CharField('Título', max_length=100)
    descricao = models.TextField('Descrição', max_length=150)    
    topico1 = models.CharField('Tópico 1', max_length=100)
    topico2 = models.CharField('Tópico 2', max_length=100)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width':1920, 'height': 1280, 'crop': True}})

    class Meta:
        verbose_name = 'Subprojeto'
        verbose_name_plural = 'Subprojetos'

    def __str__(self):
        return self.titulo


    