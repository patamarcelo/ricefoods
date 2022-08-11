import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from stdimage.models import StdImageField

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    name =filename.split('.')[0] 
    filename = f'/corretora/fotosite/{uuid.uuid4()}__{name}.{ext}'
    return filename

class Base(models.Model):
    criados = models.DateField(_('Criação'), auto_now_add=True)
    modificado = models.DateField(_('Atualização'), auto_now=True)
    ativo = models.BooleanField(_('Ativo ?'), default=True)

    class Meta:
        abstract = True

class Inicial(Base):
    inicio = models.CharField(_('Ínicio'), max_length=100)
    palavras = models.CharField(_('Palavras'), max_length=100)    
    descricao = models.TextField(_('Descrição'), max_length=150)    
    
    class Meta:
        verbose_name = _('Inicial')
        verbose_name_plural = _('Iniciais')

    def __str__(self):
        return self.inicio

class Servicos(Base):

    servico = models.CharField(_('Servico'), max_length=100)
    descricao = models.TextField(_('Decrição'), max_length=100)
    item1 = models.CharField(_('Item 1'), max_length=30)
    item2 = models.CharField(_('Item 2'), max_length=30)
    imagem = StdImageField(_('Imagem'), upload_to=get_file_path, variations={'thumb': {'width': 690, 'height': 398, 'crop': True}})

    class Meta:
        verbose_name = _('Serviço')
        verbose_name_plural = _('Serviços')

    def __str__(self):
        return self.servico

class Subservicos(Base):
    subservico = models.CharField(_('Subserviço'), max_length=100)
    topico1 = models.CharField(_('Topico 1 '), max_length=100)
    descricao1 = models.TextField(_('Descrição 1'), max_length=140)
    topico2 = models.CharField(_('Topico 2 '), max_length=100)
    descricao2 = models.TextField(_('Descrição 2'), max_length=140)
    topico3 = models.CharField(_('Topico 3'), max_length=100)
    descricao3 = models.TextField(_('Descrição 3'), max_length=140)

    class Meta:
        verbose_name = _('Subservico')
        verbose_name_plural = _('Subservicos')

    def __str__(self):
        return self.subservico




class Sobre(Base):

    titulo = models.CharField(_('Titulo'), max_length=100)
    texto = models.TextField(_('Texto'), max_length=500)
    pessoa = models.CharField(_('Pessoa'), max_length=40)
    imagem = StdImageField(_('Imagem'), upload_to=get_file_path, variations={'thumb': {'width': 1920, 'height': 1280, 'crop': True}})
    
    class Meta:
        verbose_name = _('Sobre')
        verbose_name_plural = _('Sobre')

    def __str__(self):
        return self.titulo

   

class Sobretopico(Base):
    
    ICONE_CHOICES = (
        ('fa-binoculars', _('binoculos')),
        ('fa-list-alt', _('lista')),
        ('fa-chart-pie', _('grafico pizza')),
        ('fa-truck', _('caminhão')),
        ('fa-warehouse', _('armazem')),
    )
    sobretopico = models.CharField(_('Tópico'), max_length=100)
    descricao = models.TextField(_('Descrição'), max_length=200)
    icone = models.TextField(_('Icone'), max_length=18, choices=ICONE_CHOICES)
    
    
    class Meta:
        verbose_name = _('Sobretopico')
        verbose_name_plural = _('Sobretopicos')

    def __str__(self):
        return self.sobretopico



class Projetos(Base):

    SUB_CHOICES = (
        ('originacao', _('Originação')),
        ('abast', _('Abastecimento')),
        ('impexp', _('Importação e Exportação')),
        ('logistica', _('Logística')),
    )

    LINK_CHOICES = (
        ('project-1', _('projeto1')),
        ('project-2', _('projeto2')),
        ('project-3', _('projeto3')),
        ('project-4', _('projeto4')),
        ('project-5', _('projeto5')),
        ('project-6', _('projeto6')),
        ('project-7', _('projeto7')),
        ('project-8', _('projeto8')),
        
    )

    titulo = models.CharField(_('Título'), max_length=100)
    subtitulo = models.CharField(_('Subtítulo'), max_length=100)
    descricao = models.TextField(_('Descrição'), max_length=250)
    descricao2 = models.TextField(_('Descrição Paragrafo 2'), max_length=250, blank=True)
    area = models.TextField(_('Area'), max_length=12, choices=SUB_CHOICES)
    area2 = models.TextField(_('Area2'), max_length=12, choices=SUB_CHOICES, blank=True)
    area3 = models.TextField(_('Area3'), max_length=12, choices=SUB_CHOICES, blank=True)
    area4 = models.TextField(_('Area4'), max_length=12, choices=SUB_CHOICES, blank=True)
    link = models.TextField(_('Area'), max_length=12, choices=LINK_CHOICES, unique=True)
    imagem = StdImageField(_('Imagem'), upload_to=get_file_path, variations={'thumb': {'width': 722, 'height': 702, 'crop': True}})

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')

    def __str__(self):
        return self.titulo
    

class Subprojetos(Base):
    titulo = models.CharField(_('Título'), max_length=100)
    descricao = models.TextField(_('Descrição'), max_length=150)    
    topico1 = models.CharField(_('Tópico 1'), max_length=100)
    topico2 = models.CharField(_('Tópico 2'), max_length=100)
    imagem = StdImageField(_('Imagem'), upload_to=get_file_path, variations={'thumb': {'width':1920, 'height': 1280, 'crop': True}})

    class Meta:
        verbose_name = _('Subprojeto')
        verbose_name_plural = _('Subprojetos')

    def __str__(self):
        return self.titulo


    