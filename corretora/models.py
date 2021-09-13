from django.db import models
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models import F, FloatField, Sum, Avg, Count

from datetime import timedelta
import datetime
from simple_history.models import HistoricalRecords
import dateutil.relativedelta

from decimal import Decimal
import uuid
from ricef.settings import *

from django.forms import ValidationError
from django.contrib import messages
from django import forms




def get_file_path_notafiscal(instance, filename):
    ext       = filename.split('.')[-1]
    name      = filename.split('.')[0]
    date_file = datetime.datetime.now().strftime('%Y%m%d')
    mot_name  = ''.join(instance.motorista.split()).lower() 
    filename  = f'/corretora/notasfiscais/{instance.pedido.cliente.nome_fantasia}/{date_file}_{name}_{str(uuid.uuid4())[:8]}.{ext}'
    return filename

def get_file_path_comprovantes(instance, filename):
    ext       = filename.split('.')[-1]
    name      = filename.split('.')[0]
    date_file = datetime.datetime.now().strftime('%Y%m%d')
    mot_name  = ''.join(instance.motorista.split()).lower() 
    filename  = f'/corretora/comprovantes/{instance.transp.nome}/{date_file}_{instance.placa}_{mot_name}_{str(uuid.uuid4())[:8]}__{name}.{ext}'
    return filename

def get_file_path_pedidos(instance, filename):
    ext       = filename.split('.')[-1]
    name      = filename.split('.')[0].replace('/',"").replace(" ","_")
    date_file = datetime.datetime.now().strftime('%Y%m%d')
    filename  = f'/corretora/pedidos/{instance.cliente.nome_fantasia}/{date_file}_{instance.contrato}__{name}.{ext}'
    return filename

class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).upper()


class Base(models.Model):
    criados    = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateTimeField('Atualização', auto_now=True)
    ativo      = models.BooleanField('Ativo', default=True)    


    class Meta:
        abstract = True
        

UF_CHOICES = (
    ('AC', 'Acre'), 
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RS', 'Rio Grande do Sul'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)

NOMES_DATAS = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

BASE_CARTAOVP = (
    ('palmares', 'Palmares'),
    ('rio_grande', 'Granjas - RG'),
    ('jaguarao', 'Jaguarão')
)

def get_last_cartao_base():
    query = CartaoVp.objects.all()
    if not query:
        last_used = 'palmares'
    else:
        last_used = CartaoVp.objects.all().last().cartao_base
    return last_used



class CartaoVp(Base):
    cartao_numero    = models.CharField('Número do Cartão',max_length=16, help_text="Somente os 16 números", unique=True)
    cartao_base      = models.CharField('Local Cartão', max_length=17, choices=BASE_CARTAOVP, default=get_last_cartao_base)
    cartao_utilizado = models.BooleanField('Cartão já Utilizado?', default=False, help_text="Informar se o cartão já foi utilizado")
    obs              = models.TextField('Observação', max_length=500, blank=True)
    history          = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Cartão VP'
        verbose_name_plural = 'Cartoēs VP'


    def __str__(self):
        return self.cartao_numero
    
    @property
    def get_cartao_base(self):
        return self.get_cartao_base_display()

    


class Cidade(Base):
    cidade = models.CharField('Cidade', max_length=40, unique=True)
    estado = models.TextField('Estado', max_length=12, choices=UF_CHOICES)

    class Meta:
        ordering = ['cidade']
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return self.cidade

class EmpresaCorretora(Base):
    nome          = models.CharField('Nome', max_length=50)
    cnpj_cpf      = models.CharField('CNPJ/CPF', max_length=14, unique=True, null=True, help_text="digite apenas números")
    insc_estadual = models.CharField('Inscrição Estadual',  unique=True, max_length=13,null=True,help_text="digite apenas números")
    banco         = models.CharField('Banco', max_length=10, blank=True)
    agencia       = models.CharField('Agencia', max_length=5,blank=True, help_text="digite apenas números")
    conta         = models.CharField('Conta', max_length=12,blank=True, help_text="digite apenas números")
    endereco      = models.CharField('Endereço', max_length=50)
    cidade        = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado        = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    obs           = models.TextField('Observação', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Corretora'
        verbose_name_plural = 'Corretoras'

    def __str__(self):
        return self.nome




PROD_CHOICES = (
    ('Arroz em Casca', 'Arroz em Casca'),
    ('Arroz Beneficiado', 'Arroz Beneficiado'),
    ('Semente', 'Semente'),
    ('Acucar', 'Açucar')
)


class Fornecedor(Base):
    nome          = models.CharField('Nome', max_length=50)
    cnpj_cpf      = models.CharField('CNPJ/CPF', max_length=14, unique=True, null=True, help_text="digite apenas números")
    insc_estadual = models.CharField('Inscrição Estadual',  unique=True, max_length=13,null=True,help_text="digite apenas números")
    banco         = models.CharField('Banco', max_length=10, blank=True)
    agencia       = models.CharField('Agencia', max_length=5,blank=True, help_text="digite apenas números")
    conta         = models.CharField('Conta', max_length=12,blank=True, help_text="digite apenas números")
    cidade        = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado        = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    endereco      = models.CharField('Endereço', max_length=50, default='', blank=True, null=True)
    obs           = models.TextField('Observação', max_length=500, blank=True)

    recebe_email_notafiscal = models.BooleanField('Recebe Nota Fiscal E-mail', default=False)
    email_notafiscal_1      = models.EmailField('E-mail Nota Fiscal 1', max_length=50, blank=True)
    email_notafiscal_2      = models.EmailField('E-mail Nota Fiscal 2', max_length=50, blank=True)
    email_notafiscal_3      = models.EmailField('E-mail Nota Fiscal 3', max_length=50, blank=True)
    email_notafiscal_4      = models.EmailField('E-mail Nota Fiscal 4', max_length=50, blank=True)
    email_notafiscal_5      = models.EmailField('E-mail Nota Fiscal 5', max_length=50, blank=True)

    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.nome

def set_default_fornecedor():
    return Fornecedor.objects.get_or_create(nome='Fornecedor Deletado')[0] #(objeto, boolean)
       

class Cliente(Base):
    nome            = models.CharField('Nome', max_length=50)
    nome_fantasia   = models.CharField('Nome Fantasia', max_length=50)
    cnpj_cpf        = models.CharField('CNPJ/CPF', max_length=14,  unique=True,  null=True, help_text="digite apenas números")
    insc_estadual   = models.CharField('Inscrição Estadual',  unique=True,  max_length=10, help_text="digite apenas números",null=True)
    telefone        = models.CharField('Telefone',max_length=11, help_text="digite apenas números", null=True)
    endereco        = models.CharField('Endereço', max_length=50)
    cidade          = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado          = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    color           = models.CharField('Cor', max_length=20, default='whitesmoke')
    dias_descarga   = models.PositiveIntegerField('Desc. do Carr.', default=3,help_text="dias para a descarga do carregamento")
    veiculos_dia    = models.PositiveIntegerField('Veiculos Dia', default=10, help_text="máximo veículos descarga por dia")
    descarga_sabado = models.BooleanField('Descarga Sábado', default=False)
    obs             = models.TextField('Observação', max_length=500, blank=True)

    recebe_email_notafiscal = models.BooleanField('Recebe Nota Fiscal E-mail', default=False)
    email_notafiscal_1      = models.EmailField('E-mail Nota Fiscal 1', max_length=50, blank=True)
    email_notafiscal_2      = models.EmailField('E-mail Nota Fiscal 2', max_length=50, blank=True)
    email_notafiscal_3      = models.EmailField('E-mail Nota Fiscal 3', max_length=50, blank=True)
    email_notafiscal_4      = models.EmailField('E-mail Nota Fiscal 4', max_length=50, blank=True)
    email_notafiscal_5      = models.EmailField('E-mail Nota Fiscal 5', max_length=50, blank=True)

    def mesanterior(self):
        lastm = today.month - 1 if today.month > 1 else 12
        lastmy = today.year if today.month > lastm else today.year -1
        pass
    
    def comissaosemanacasca(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        comisemanacda = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comisemana = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comisemanasemente = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comisemanacda == None:
                self.comissaosemanacasca = 0
                return self.comissaosemanacasca            
            else:
                self.comissaosemanacasca = comisemanacda
                return self.comissaosemanacasca
        elif 'iamant' in filt:
            if comisemanasemente == None:
                self.comissaosemanacasca = 0
                return self.comissaosemanacasca            
            else:
                self.comissaosemanacasca = comisemanasemente
                return self.comissaosemanacasca
        else:
            if comisemana == None:
                self.comissaosemanacasca = 0
                return self.comissaosemanacasca
            else:
                self.comissaosemanacasca = comisemana
                return self.comissaosemanacasca
    
    def comissaomescasca(self):
        filt = self.nome_fantasia
        today = datetime.date.today()        
        comimescascacda = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimescasca = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimessemente = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']

        if 'CDA' in filt:
            if comimescascacda == None:
                self.comissaomescasca = 0
                return self.comissaomescasca            
            else:
                self.comissaomescasca = comimescascacda
                return self.comissaomescasca
        elif 'iamant' in filt:
            if comimessemente == None:
                self.comissaomescasca = 0
                return self.comissaomescasca            
            else:
                self.comissaomescasca = comimessemente
                return self.comissaomescasca
        else:
            if comimescasca == None:
                self.comissaomescasca = 0
                return self.comissaomescasca
            else:
                self.comissaomescasca = comimescasca
                return self.comissaomescasca
    
    
    def comissaomescascaanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        
        monthdelta = dateutil.relativedelta.relativedelta(months=1)            
        lastms = datetime.datetime.now() - monthdelta  
        lastm = lastms.month              
        lastmy = lastms.year
        
        comimesanteriorcascacda = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteriorcasca = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteriorsemente = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimesanteriorcascacda == None:
                self.comissaomescascaanterior = 0
                return self.comissaomescascaanterior            
            else:
                self.comissaomescascaanterior = comimesanteriorcascacda
                return self.comissaomescascaanterior
        elif 'iamant' in filt:
            if comimesanteriorsemente == None:
                self.comissaomescascaanterior = 0
                return self.comissaomescascaanterior            
            else:
                self.comissaomescascaanterior = comimesanteriorsemente
                return self.comissaomescascaanterior
        else:
            if comimesanteriorcasca == None:
                self.comissaomescascaanterior = 0
                return self.comissaomescascaanterior
            else:
                self.comissaomescascaanterior = comimesanteriorcasca
                return self.comissaomescascaanterior
    
    
    def comissaomescascaanteanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()

        monthdelta = dateutil.relativedelta.relativedelta(months=2)            
        lastmms = datetime.datetime.now() - monthdelta  
        lastmm = lastmms.month      
        lastmmy = lastmms.year
        
        comimesanteanteriorcascacda = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteanteriorcasca = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteanteriorsemente = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimesanteanteriorcascacda == None:
                self.comissaomescascaanteanterior = 0
                return self.comissaomescascaanteanterior            
            else:
                self.comissaomescascaanteanterior = comimesanteanteriorcascacda
                return self.comissaomescascaanteanterior
        elif 'iamant' in filt:
            if comimesanteanteriorsemente == None:
                self.comissaomescascaanteanterior = 0
                return self.comissaomescascaanteanterior            
            else:
                self.comissaomescascaanteanterior = comimesanteanteriorsemente
                return self.comissaomescascaanteanterior
        else:
            if comimesanteanteriorcasca == None:
                self.comissaomescascaanteanterior = 0
                return self.comissaomescascaanteanterior
            else:
                self.comissaomescascaanteanterior = comimesanteanteriorcasca
                return self.comissaomescascaanteanterior
    
    
    def comissaomescascatresanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        
        monthdelta = dateutil.relativedelta.relativedelta(months=3)            
        lastmms3 = datetime.datetime.now() - monthdelta  
        lastmm3 = lastmms3.month              
        lastmmy3 = lastmms3.year
        
        comimescascatresanteriorcda = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimestresanteriorcasca = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimestresanteriorsemente = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimescascatresanteriorcda == None:
                self.comissaomescascatresanterior = 0
                return self.comissaomescascatresanterior            
            else:
                self.comissaomescascatresanterior = comimescascatresanteriorcda
                return self.comissaomescascatresanterior
        elif 'iamant' in filt:
            if comimestresanteriorsemente == None:
                self.comissaomescascatresanterior = 0
                return self.comissaomescascatresanterior            
            else:
                self.comissaomescascatresanterior = comimestresanteriorsemente
                return self.comissaomescascatresanterior
        else:
            if comimestresanteriorcasca == None:
                self.comissaomescascatresanterior = 0
                return self.comissaomescascatresanterior
            else:
                self.comissaomescascatresanterior = comimestresanteriorcasca
                return self.comissaomescascatresanterior
   
    def comissaomescascaquatroanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()

        monthdelta = dateutil.relativedelta.relativedelta(months=4)            
        lastmms3 = datetime.datetime.now() - monthdelta          
        lastmm3 = lastmms3.month              
        lastmmy3 = lastmms3.year

        comimescascatresanteriorcda = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimestresanteriorcasca = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimestresanteriorsemente = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimescascatresanteriorcda == None:
                self.comissaomescascaquatroanterior = 0
                return self.comissaomescascaquatroanterior            
            else:
                self.comissaomescascaquatroanterior = comimescascatresanteriorcda
                return self.comissaomescascaquatroanterior
        elif 'iamant' in filt:
            if comimestresanteriorsemente == None:
                self.comissaomescascaquatroanterior = 0
                return self.comissaomescascaquatroanterior            
            else:
                self.comissaomescascaquatroanterior = comimestresanteriorsemente
                return self.comissaomescascaquatroanterior
        else:
            if comimestresanteriorcasca == None:
                self.comissaomescascaquatroanterior = 0
                return self.comissaomescascaquatroanterior
            else:
                self.comissaomescascaquatroanterior = comimestresanteriorcasca
                return self.comissaomescascaquatroanterior

    def comissaomescascacincoanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()

        monthdelta = dateutil.relativedelta.relativedelta(months=5)            
        lastmms5 = datetime.datetime.now() - monthdelta  
        lastmm5 = lastmms5.month      
        lastmmy5 = lastmms5.year
        
        comimescascacincoanteriorcda = Carga.objects.filter(data__year=lastmmy5, data__month=lastmm5).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimescincoanteriorcasca = Carga.objects.filter(data__year=lastmmy5, data__month=lastmm5).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimescincoanteriorsemente = Carga.objects.filter(data__year=lastmmy5, data__month=lastmm5).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimescascacincoanteriorcda == None:
                self.comissaomescascacincoanterior = 0
                return self.comissaomescascacincoanterior            
            else:
                self.comissaomescascacincoanterior = comimescascacincoanteriorcda
                return self.comissaomescascacincoanterior
        elif 'iamant' in filt:
            if comimescincoanteriorsemente == None:
                self.comissaomescascacincoanterior = 0
                return self.comissaomescascacincoanterior            
            else:
                self.comissaomescascacincoanterior = comimescincoanteriorsemente
                return self.comissaomescascacincoanterior
        else:
            if comimescincoanteriorcasca == None:
                self.comissaomescascacincoanterior = 0
                return self.comissaomescascacincoanterior
            else:
                self.comissaomescascacincoanterior = comimescincoanteriorcasca
                return self.comissaomescascacincoanterior

    def comissaomescascaseisanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()

        monthdelta = dateutil.relativedelta.relativedelta(months=6)            
        lastmms6 = datetime.datetime.now() - monthdelta  
        lastmm6 = lastmms6.month              
        lastmmy6 = lastmms6.year
        
        comimescascaseisanteriorcda = Carga.objects.filter(data__year=lastmmy6, data__month=lastmm6).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesseisanteriorcasca = Carga.objects.filter(data__year=lastmmy6, data__month=lastmm6).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesseisanteriorsemente = Carga.objects.filter(data__year=lastmmy6, data__month=lastmm6).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        if 'CDA' in filt:
            if comimescascaseisanteriorcda == None:
                self.comissaomescascaseisanterior = 0
                return self.comissaomescascaseisanterior            
            else:
                self.comissaomescascaseisanterior = comimescascaseisanteriorcda
                return self.comissaomescascaseisanterior
        elif 'iamant' in filt:
            if comimesseisanteriorsemente == None:
                self.comissaomescascaseisanterior = 0
                return self.comissaomescascaseisanterior            
            else:
                self.comissaomescascaseisanterior = comimesseisanteriorsemente
                return self.comissaomescascaseisanterior
        else:
            if comimesseisanteriorcasca == None:
                self.comissaomescascaseisanterior = 0
                return self.comissaomescascaseisanterior
            else:
                self.comissaomescascaseisanterior = comimesseisanteriorcasca
                return self.comissaomescascaseisanterior
            
    
    
    def comissaoabertocasca(self):
        filt = self.nome_fantasia               
        comiabertocda = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comiaberto = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(((F('peso') / 50) * F('pedido__preco_produto')) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comiabertosemente = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']

        # totaiscomissao = [comiabertocda, comiaberto, comiabertosemente]
        # self.comissaoabertocasca = 0
        # for i in totaiscomissao:
        #     if i != None:
        #         self.comissaoabertocasca = i + self.comissaoabertocasca
        #     else:
        #         self.comissaoabertocasca = 0 + self.comissaoabertocasca
        #     return self.comissaoabertocasca

        if 'CDA' in filt:
            if comiabertocda == None:
                self.comissaoabertocasca = 0
                return self.comissaoabertocasca            
            else:
                self.comissaoabertocasca = comiabertocda
                return self.comissaoabertocasca
        elif 'iamante' in filt:
            if comiabertosemente == None:
                self.comissaoabertocasca = 0
                return self.comissaoabertocasca
            else:
                self.comissaoabertocasca = comiabertosemente
                return self.comissaoabertocasca
        else:
            if comiaberto == None:
                self.comissaoabertocasca = 0
                return self.comissaoabertocasca
            else:
                self.comissaoabertocasca = comiaberto
                return self.comissaoabertocasca
        



                
    def comissaoabertocascatotal(self):
        filt = self.nome_fantasia
        comiabertototalcda = Carga.objects.filter(pedido__cliente__nome='CDA').filter(pgcomissao=False).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comiabertototal = Carga.objects.exclude(pedido__cliente__nome='CDA').filter(pgcomissao=False).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comiabertosementetotal = Carga.objects.filter(pgcomissao=False).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']


        totaiscomissao = [comiabertototalcda, comiabertototal, comiabertosementetotal]
        self.comissaoabertocascatotal = 0
        for i in totaiscomissao:
            if i != None:
                self.comissaoabertocascatotal = i + self.comissaoabertocascatotal
            else:
                self.comissaoabertocascatotal = 0 + self.comissaoabertocascatotal
        return self.comissaoabertocascatotal


    
    def comissao_geral_por_cliente(self):
        comissaopordata = {}
        comissaopordata_ordenado = {}
        filt = self.nome_fantasia
        for i in range(0,7):
            monthdelta = dateutil.relativedelta.relativedelta(months=i)
            numeromes = datetime.datetime.now() - monthdelta
            anoalterado =  numeromes.year
            mesalterado =  numeromes.month            
            chave_dict = f'{anoalterado}-{mesalterado}'
            if 'CDA' in filt:
                query_carregado = Carga.objects.filter(data__year=anoalterado, data__month=mesalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']        
            elif 'iamante' in filt:
                query_carregado = Carga.objects.filter(data__year=anoalterado, data__month=mesalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
            else:
                query_carregado = Carga.objects.filter(data__year=anoalterado, data__month=mesalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']            
            pesocarregado_porcliente = query_carregado if query_carregado != None else 0
            comissaopordata[chave_dict] = pesocarregado_porcliente        
        for k,v in comissaopordata.items():
            dict_element={k:v}
            dict_element.update(comissaopordata_ordenado)
            comissaopordata_ordenado=dict_element
        self.comissao_geral_por_cliente = comissaopordata_ordenado        
        return self.comissao_geral_por_cliente

    def comissao_ultimos_meses(self):
        filt = self.nome_fantasia
        monthdelta = dateutil.relativedelta.relativedelta(months=6)
        numeromes = datetime.datetime.now() - monthdelta
        anoalterado =  numeromes.year
        mesalterado =  numeromes.month
        diaalterado =  numeromes.replace(day=1)
        if 'CDA' in filt:
            query_comissao = Carga.objects.filter(data__gte=diaalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']        
        elif 'iamante' in filt:
            query_comissao = Carga.objects.filter(data__gte=diaalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Semente').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum(F('valornf') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        else:
            query_comissao = Carga.objects.filter(data__gte=diaalterado).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comissao_porcliente = query_comissao if query_comissao != None else 0
        self.comissao_ultimos_meses = comissao_porcliente  
        print(f'Cliente: {filt} - {self.comissao_ultimos_meses}')
        print(type(self.comissao_ultimos_meses))               
        return self.comissao_ultimos_meses




        # if comiabertototalcda == None and comiabertototal == None:
        #         self.comissaoabertocascatotal = 0
        #         return self.comissaoabertocascatotal            
        # elif comiabertototalcda == None and comiabertototal > 0:
        #     self.comissaoabertocascatotal = comiabertototal
        #     return self.comissaoabertocascatotal 
        # elif  comiabertototalcda > 0 and comiabertototal == None:
        #     self.comissaoabertocascatotal = comiabertototalcda
        #     return self.comissaoabertocascatotal 
        # else:
        #     self.comissaoabertocascatotal = comiabertototal + comiabertototalcda
        #     return self.comissaoabertocascatotal 



    def carregadomes(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        carregadomes = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomes = carregadomes
        if self.carregadomes == None:
            self.carregadomes = 0
            return self.carregadomes
        else:
            return self.carregadomes
    
    def carregadomestotal(self):        
        today = datetime.date.today()
        carregadomestotal = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomestotal = carregadomestotal
        if self.carregadomestotal == None:
            self.carregadomestotal = 0
            return self.carregadomestotal
        else:
            return self.carregadomestotal
    
    def carregadomesanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        lastm = today.month - 1 if today.month > 1 else 12
        lastmy = today.year if today.month > lastm else today.year -1
        carregadomesanterior = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomesanterior = carregadomesanterior
        if self.carregadomesanterior == None:
            self.carregadomesanterior = 0
            return self.carregadomesanterior
        else:
            return self.carregadomesanterior
    
    def carregadomesanteriortotal(self):
        
        today = datetime.date.today()
        lastm = today.month - 1 if today.month > 1 else 12
        lastmy = today.year if today.month > lastm else today.year -1
        carregadomesanterior = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomesanterior = carregadomesanterior
        if self.carregadomesanterior == None:
            self.carregadomesanterior = 0
            return self.carregadomesanterior
        else:
            return self.carregadomesanterior

    def carregadomesanteanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        lastmm = today.month - 2 if today.month > 2 else 11
        lastmmy = today.year if today.month > lastmm else today.year -1
        carregadomesanteanterior = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomesanteanterior = carregadomesanteanterior
        if self.carregadomesanteanterior == None:
            self.carregadomesanteanterior = 0
            return self.carregadomesanteanterior
        else:
            return self.carregadomesanteanterior
    
    def carregadomesanteanteriortotal(self):
        
        today = datetime.date.today()
        lastmm = today.month - 2 if today.month > 2 else 11
        lastmmy = today.year if today.month > lastmm else today.year -1
        carregadomesanteanterior = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomesanteanterior = carregadomesanteanterior
        if self.carregadomesanteanterior == None:
            self.carregadomesanteanterior = 0
            return self.carregadomesanteanterior
        else:
            return self.carregadomesanteanterior

    def carregadomestresanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        lastmm3 = today.month - 3 if today.month > 3 else 10
        lastmmy3 = today.year if today.month > lastmm3 else today.year -1
        carregadomestresanterior = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomestresanterior = carregadomestresanterior
        if self.carregadomestresanterior == None:
            self.carregadomestresanterior = 0
            return self.carregadomestresanterior
        else:
            return self.carregadomestresanterior
    
    def carregadomestresanteriortotal(self):
        
        today = datetime.date.today()
        lastmm3 = today.month - 3 if today.month > 3 else 10
        lastmmy3 = today.year if today.month > lastmm3 else today.year -1
        carregadomestresanterior = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomestresanterior = carregadomestresanterior
        if self.carregadomestresanterior == None:
            self.carregadomestresanterior = 0
            return self.carregadomestresanterior
        else:
            return self.carregadomestresanterior
    
    def carregado_geral_por_cliente(self):
        pesospordata = {}
        pesospordata_ordenado = {}
        filt = self.nome_fantasia
        for i in range(0,7):
            monthdelta = dateutil.relativedelta.relativedelta(months=i)
            numeromes = datetime.datetime.now() - monthdelta
            anoalterado =  numeromes.year
            mesalterado =  numeromes.month            
            chave_dict = f'{anoalterado}-{mesalterado}'
            query_carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(data__year=anoalterado, data__month=mesalterado).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
            pesocarregado_porcliente = query_carregado if query_carregado != None else 0
            pesospordata[chave_dict] = pesocarregado_porcliente        
        for k,v in pesospordata.items():
            dict_element={k:v}
            dict_element.update(pesospordata_ordenado)
            pesospordata_ordenado=dict_element
        self.carregado_geral_por_cliente = pesospordata_ordenado
        print(self.carregado_geral_por_cliente)
        return self.carregado_geral_por_cliente
    
    def carregado_geral_por_cliente_somentequatro(self):
        pesospordata = {}
        pesospordata_ordenado = {}
        filt = self.nome_fantasia
        for i in range(0,4):
            monthdelta = dateutil.relativedelta.relativedelta(months=i)
            numeromes = datetime.datetime.now() - monthdelta
            anoalterado =  numeromes.year
            mesalterado =  numeromes.month            
            chave_dict = f'{anoalterado}-{mesalterado}'
            query_carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(data__year=anoalterado, data__month=mesalterado).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
            pesocarregado_porcliente = query_carregado if query_carregado != None else 0
            pesospordata[chave_dict] = pesocarregado_porcliente        
        for k,v in pesospordata.items():
            dict_element={k:v}
            dict_element.update(pesospordata_ordenado)
            pesospordata_ordenado=dict_element
        self.carregado_geral_por_cliente_somentequatro = pesospordata_ordenado
        print(self.carregado_geral_por_cliente_somentequatro)
        return self.carregado_geral_por_cliente_somentequatro
    
    def carregado_geral_por_geral(self):
        pesospordata = {}
        pesospordata_ordenado = {}        
        for i in range(0,7):
            monthdelta = dateutil.relativedelta.relativedelta(months=i)
            numeromes = datetime.datetime.now() - monthdelta
            anoalterado =  numeromes.year
            mesalterado =  numeromes.month            
            chave_dict = f'{anoalterado}-{mesalterado}'
            query_carregado = Carga.objects.filter(data__year=anoalterado, data__month=mesalterado).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
            pesocarregado_porcliente = query_carregado if query_carregado != None else 0
            pesospordata[chave_dict] = pesocarregado_porcliente        
        for k,v in pesospordata.items():
            dict_element={k:v}
            dict_element.update(pesospordata_ordenado)
            pesospordata_ordenado=dict_element
        self.carregado_geral_por_geral = pesospordata_ordenado
        print(f'Toais Carregados: {self.carregado_geral_por_geral}')
        return self.carregado_geral_por_geral

    def carregamento_ultimos_meses(self):
        filt = self.nome_fantasia
        monthdelta = dateutil.relativedelta.relativedelta(months=6)
        numeromes = datetime.datetime.now() - monthdelta
        anoalterado =  numeromes.year
        mesalterado =  numeromes.month
        diaalterado =  numeromes.replace(day=1)
        query_carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(data__gte=diaalterado).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        pesocarregado_porcliente = query_carregado if query_carregado != None else 0
        self.carregamento_ultimos_meses = pesocarregado_porcliente
        return self.carregamento_ultimos_meses


    def carregadosemana(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        carregado = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadosemana = carregado
        if self.carregadosemana == None:
            self.carregadosemana = 0
            return self.carregadosemana
        else:
            return self.carregadosemana
    
    def carregadosemanatotal(self):
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        carregado = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        agendado = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(situacao='Agendado').values('veiculo').aggregate(pesov=Sum('veiculo'))['pesov']
        
        if carregado == None and agendado == None:
            self.carregadosemanatotal = 0
            return self.carregadosemanatotal
        elif carregado == None and agendado > 0:
            self.carregadosemanatotal = agendado
            return self.carregadosemanatotal
        elif carregado > 0 and agendado == None:
            self.carregadosemanatotal = carregado
            return self.carregadosemanatotal
        else:
            self.carregadosemanatotal = carregado + agendado
            return self.carregadosemanatotal 

    def agendadoordemsemana(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        agendadoordem = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(pesot=Sum('veiculo'))['pesot']
        self.agendadoordemsemana = agendadoordem
        if self.agendadoordemsemana == None:
            self.agendadoordemsemana = 0
            return self.agendadoordemsemana
        else:
            return self.agendadoordemsemana
    
    def agendadosemana(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        agendado = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(pesot=Sum('veiculo'))['pesot']
        self.agendadosemana = agendado
        if self.agendadosemana == None:
            self.agendadosemana = 0
            return self.agendadosemana
        else:
            return self.agendadosemana
    
    
    def agendadosemanaseguinte(self):
        filt = self.nome_fantasia
        nexttoday = datetime.date.today() + datetime.timedelta(days=7)
        nextmonday = nexttoday - datetime.timedelta(days=nexttoday.weekday())
        nextsunday = nexttoday - datetime.timedelta(days=nexttoday.weekday()) + datetime.timedelta(days=6)
        nextagendado = Carga.objects.filter(data__gte=nextmonday).filter(data__lte=nextsunday).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Agendado').values('veiculo').aggregate(pesot=Sum('veiculo'))['pesot']
        self.agendadosemanaseguinte = nextagendado
        if self.agendadosemanaseguinte == None:
            self.agendadosemanaseguinte = 0
            return self.agendadosemanaseguinte
        else:
            return self.agendadosemanaseguinte

    def totalsemana(self):        
        return self.agendadosemana + self.agendadoordemsemana + self.carregadosemana


    def saldopedido(self):
        filt = self.nome_fantasia
        totalped = Pedido.objects.filter(cliente__nome_fantasia=filt).filter(situacao='a').filter(ativo=True).values('quantidade_pedido').aggregate(pesototal=Sum('quantidade_pedido'))['pesototal']
        self.totalped = totalped
        carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']            
        self.carregado = carregado

        if self.totalped == None:
            self.saldopedido = 0
            return self.saldopedido
        elif self.carregado == None or self.carregado == 0:
            self.saldopedido = self.totalped
            return self.saldopedido
        else:
            saldoreal = self.totalped - self.carregado
            self.saldopedido = saldoreal
            return self.saldopedido

    

    def saldoprevisto(self):
        filt = self.nome_fantasia
        totalped = Pedido.objects.filter(cliente__nome_fantasia=filt).filter(situacao='a').filter(ativo=True).values('quantidade_pedido').aggregate(pesototal=Sum('quantidade_pedido'))['pesototal']
        self.totalped = totalped
        carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']            
        self.carregado = carregado
        previsto = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Agendado').values('pedido').aggregate(veiculot=Sum('veiculo'))['veiculot']
        self.previsto = previsto

        if self.totalped == None:
            self.saldoprevisto = 0
            return self.saldoprevisto
        elif self.carregado == None or self.carregado == 0:            
            if self.previsto != None and self.previsto != 0:
                self.saldoprevisto = self.totalped - self.previsto
                return self.saldoprevisto
            else:
                self.saldoprevisto = self.totalped
                return self.saldoprevisto
        elif self.previsto == None or self.previsto == 0:
            saldoreal = self.totalped - self.carregado
            self.saldoprevisto = saldoreal
            return self.saldoprevisto        
        else:
            saldoprevisto = self.totalped - self.carregado - self.previsto
            self.saldoprevisto = saldoprevisto
            return self.saldoprevisto
    
    def locaiscarrega(self):
        filt = self.nome_fantasia
        locais = Pedido.objects.filter(cliente__nome_fantasia=filt).filter(situacao='a').filter(ativo=True).values('contrato').aggregate(quanti=Count('contrato'))['quanti']
        self.locaiscarrega = locais
        return self.locaiscarrega 
    
    def previsao_dias_da_semana(self):
        previsao_dias_da_semana = {}
        previsao_dias_da_semana_count = {}
        def dias_da_semana():                  
            today = datetime.datetime.now()   
            duas_semanas = []
            for i in range(14):
                data_atual = today if today.weekday() == i else today - timedelta(days=today.weekday() - i)
                dia_da_semana_numero = data_atual.weekday()
                data_atual_timestamp = data_atual.timestamp()
                day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
                data_atual_humana = day_fromtmsp.strftime("%Y-%m-%d") 
                duas_semanas.append(data_atual_humana)        
            return duas_semanas
        for i in dias_da_semana():
            total = 0
            total_count = 0
            filtdata = i
            filt_nome = self.nome_fantasia
            carregado = Carga.objects.filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
            carregado_count = Carga.objects.order_by('placa').filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Carregado').values('peso').distinct('placa').count()
            agendado = Carga.objects.filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Agendado').values('veiculo').aggregate(pesov=Sum('veiculo'))['pesov']
            agendado_count = Carga.objects.order_by('placa').filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Agendado').values('veiculo').distinct('placa').count()
            if carregado and agendado:
                total = carregado + agendado
                total_count = carregado_count + agendado_count
            elif carregado:
                total = carregado
                total_count = carregado_count
            elif agendado:
                total = agendado
                total_count = agendado_count
            data_regular = datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%d/%m/%Y')
            previsao_dias_da_semana[data_regular] = total
            previsao_dias_da_semana_count[data_regular] = total_count
        self.previsao_dias_da_semana = previsao_dias_da_semana, previsao_dias_da_semana_count
        return self.previsao_dias_da_semana 
    
    
    def previsao_dias_da_semana_dois(self):
        previsao_dias_da_semana = {}
        previsao_dias_da_semana_count = {}
        def dias_da_semana():                  
            today = datetime.datetime.now()   
            duas_semanas = []
            for i in range(14):
                data_atual = today if today.weekday() == i else today - timedelta(days=today.weekday() - i)
                dia_da_semana_numero = data_atual.weekday()
                data_atual_timestamp = data_atual.timestamp()
                day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
                data_atual_humana = day_fromtmsp.strftime("%Y-%m-%d") 
                duas_semanas.append(data_atual_humana)                           
            print(f'Duas Semanas: {duas_semanas}')
            return duas_semanas
        for i in dias_da_semana():
            total = 0
            total_count = 0
            filtdata = i
            filt_nome = self.nome_fantasia
            carregado = 0
            carregado_count = Carga.objects.order_by('placa').filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Carregado').values('peso').distinct('placa').count()
            agendado = 0
            agendado_count = Carga.objects.order_by('placa').filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Agendado').values('veiculo').distinct('placa').count()
            
            total = carregado + agendado
            total_count = carregado_count + agendado_count
            
            data_regular = datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%d/%m/%Y')
            previsao_dias_da_semana[data_regular] = total
            previsao_dias_da_semana_count[data_regular] = total_count
        self.previsao_dias_da_semana = previsao_dias_da_semana, previsao_dias_da_semana_count

        return self.previsao_dias_da_semana 

    def previsao_dias_da_semana_somente_carregado(self):
        previsao_dias_da_semana = {}
        previsao_dias_da_semana_count = {}
        def dias_da_semana():                  
            today = datetime.datetime.now()   
            duas_semanas = []
            for i in range(7):
                data_atual = today if today.weekday() == i else today - timedelta(days=today.weekday() - i)
                dia_da_semana_numero = data_atual.weekday()
                data_atual_timestamp = data_atual.timestamp()
                day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
                data_atual_humana = day_fromtmsp.strftime("%Y-%m-%d") 
                duas_semanas.append(data_atual_humana)        
            for i in range(7):
                data_atual = (today + timedelta(days=7)) if today.weekday() == i else (today + timedelta(days=7)) - timedelta(days=today.weekday() - i)
                dia_da_semana_numero = data_atual.weekday()
                data_atual_timestamp = data_atual.timestamp()
                day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
                data_atual_humana = day_fromtmsp.strftime("%Y-%m-%d") 
                duas_semanas.append(data_atual_humana)                                    
            return duas_semanas
        for i in dias_da_semana():
            total = 0
            total_count = 0
            filtdata = i
            filt_nome = self.nome_fantasia
            carregado = Carga.objects.filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
            carregado_count = Carga.objects.order_by('placa').filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Carregado').values('peso').distinct('placa').count()
            agendado = Carga.objects.filter(data_agenda=filtdata).filter(pedido__cliente__nome_fantasia=filt_nome).filter(situacao='Agendado').values('veiculo').aggregate(pesov=Sum('veiculo'))['pesov']            
            if carregado and agendado:
                total = carregado + agendado
                total_count = carregado_count
            elif carregado:
                total = carregado
                total_count = carregado_count
            elif agendado:
                total = agendado
                total_count = 0
            data_regular = datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%d/%m/%Y')
            previsao_dias_da_semana[data_regular] = total
            previsao_dias_da_semana_count[data_regular] = total_count
        self.previsao_dias_da_semana_somente_carregado = previsao_dias_da_semana, previsao_dias_da_semana_count
        return self.previsao_dias_da_semana_somente_carregado 

    def dias_da_semana_model_cliente(self): 
        today = datetime.datetime.now()
        dias_escritos=["Segunda-Feira","Terça-Feira","Quarta-Feira","Quinta-Feira","Sexta-Feira","Sábado","Domingo"]
        semana_atual = {}
        semana_seguinte = {}            
        for i in range(7):
            data_atual = today if today.weekday() == i else today - timedelta(days=today.weekday() - i)
            dia_da_semana_numero = data_atual.weekday()
            data_atual_timestamp = data_atual.timestamp()
            day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
            data_atual_humana = day_fromtmsp.strftime("%d/%m/%Y") 
            dia_escrito = dias_escritos[dia_da_semana_numero]
            semana_atual[dia_escrito] = data_atual_humana                    
        for i in range(7):
            data_atual = (today + timedelta(days=7)) if today.weekday() == i else (today + timedelta(days=7)) - timedelta(days=today.weekday() - i)
            dia_da_semana_numero = data_atual.weekday()
            data_atual_timestamp = data_atual.timestamp()
            day_fromtmsp = datetime.datetime.fromtimestamp(data_atual_timestamp)
            data_atual_humana = day_fromtmsp.strftime("%d/%m/%Y") 
            dia_escrito = dias_escritos[dia_da_semana_numero]
            semana_seguinte[dia_escrito] = data_atual_humana           
        
        
        return semana_atual, semana_seguinte
    

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome_fantasia

def set_default_cliente():
    return Cliente.objects.get_or_create(nome='Cliente Deletado')[0] #(objeto, boolean)

class Datasemcarga(Base):
    data_semcarga = models.DateField('Data', help_text="dd/mm/aaaa | Data Sem Descarga")
    cliente       = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    obs           = models.TextField('Observação', max_length=2000, blank=True)
    history       = HistoricalRecords()

    class Meta:
        ordering = ['-data_semcarga']
        verbose_name = 'Data Sem Descarga'
        verbose_name_plural = 'Datas Sem Descarga'
    
    def __str__(self):
        return f'{self.cliente}: Sem descarga dia {self.data_semcarga}'




class Transportadora(Base):
    recebe_email_notafiscal  = models.BooleanField('Recebe Nota Fiscal E-mail', default=False)
    email_notafiscal         = models.EmailField('E-mail Nota Fiscal', max_length=30, blank=True)
    recebe_email_comprovante = models.BooleanField('Recebe Comprovante E-mail', default=False)
    nome                     = models.CharField('Nome', max_length=20, unique=True)
    cidade                   = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado                   = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    contato                  = models.CharField('Contato', max_length=30, blank=True)
    telefone                 = models.CharField('Telefone', max_length=15, blank=True, help_text="digite apenas números")
    email                    = models.EmailField('E-mail', max_length=30,blank=True)
    obs                      = models.TextField('Observação', max_length=500, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Transportadora'
        verbose_name_plural = 'Transportadoras'

    def __str__(self):
        return self.nome




    


class Pedido(Base):
    
    

    SIT_CHOICES = (
        ('a', 'Aberto'),
        ('b', 'Fechado'),
        ('c', 'Cancelado')
    )

    TIPO_CHOICES = (
        ('Saco 50Kg', 'Saco 50Kg'),
        ('Saco 40Kg', 'Saco 40Kg'),
        ('Fardo 30Kg', 'Fardo 30Kg'),
        ('Big Bag', 'Big Bag')
    )

    contrato      = NameField('Numero', max_length=9, unique=True)
    situacao      = models.CharField('Situação', max_length=12, choices=SIT_CHOICES, default='Aberto')
    data          = models.DateField(default=timezone.now, help_text="dd/mm/aaaa")
    fornecedor    = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    cliente       = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    preco_produto = models.DecimalField('R$ Produto', max_digits=8, decimal_places=2)
    preco_frete   = models.DecimalField('Frete', max_digits=5, decimal_places=2)

    comissaoc = models.DecimalField('Comissão C', max_digits=4, decimal_places=2 )
    comissaof = models.DecimalField('Comissão F', max_digits=4, decimal_places=2 ,null=True, blank=True )

    prazopgto      = models.CharField('Prazo Pgto', max_length=20,null=True, blank=True )
    modalidadepgto = models.CharField('Mod. Pgto', max_length=30,null=True, blank=True )

    renda    = models.DecimalField('Renda', max_digits=4, decimal_places=2)
    inteiro  = models.DecimalField('Inteiro', max_digits=4, decimal_places=2)
    impureza = models.DecimalField('Impureza', max_digits=4, decimal_places=2,null=True, blank=True)
    umidade  = models.DecimalField('Umidade', max_digits=4, decimal_places=2)

    gessado   = models.DecimalField('Gessado', max_digits=4, decimal_places=2,null=True,blank=True)
    bbranca   = models.DecimalField('B. Branca', max_digits=4, decimal_places=2,null=True, blank=True)
    amarelo   = models.DecimalField('Amarelo', max_digits=4, decimal_places=2,null=True, blank=True)
    manchpic  = models.DecimalField('Man / Pic', max_digits=4, decimal_places=2,null=True, blank=True)
    vermelhos = models.DecimalField('Vermelhos', max_digits=4, decimal_places=2,null=True, blank=True)

    variedade         = models.CharField('Variedade', max_length=12)
    produto           = models.CharField('Produto', max_length=17, choices=PROD_CHOICES,default='Arroz em Casca')
    tipo              = models.CharField('Tipo', max_length=12, choices=TIPO_CHOICES, default='Saco 50Kg')
    quantidade_pedido = models.PositiveIntegerField('Quant. Pedido', help_text="Peso em Kg")

    pedido_arquivo = models.FileField('Pedido ', upload_to=get_file_path_pedidos, null=True, blank=True)
    

    obs     = models.TextField('Observação', max_length=500, blank=True)
    history = HistoricalRecords()


    
    def comissaorecebida(self):
        filt = self.contrato
        comissaorecebida = Carga.objects.filter(pedido__contrato=filt).filter(pgcomissao=False).values('pedido').aggregate(receb=Count('pgcomissao'))['receb']
        self.comissaorecebida = comissaorecebida
        return self.comissaorecebida

    def totalcomissaocasca(self):
        filt = self.contrato
        totalcomissaocasca = Carga.objects.filter(pedido__contrato=filt).filter(situacao='Carregado').filter(peso__gt=1).values('pedido').aggregate(pesot=Sum('peso'))['pesot']
        self.totalcomissaocasca = totalcomissaocasca
        
        totalcomissaocascacda = Carga.objects.filter(pedido__contrato=filt).filter(situacao='Carregado').filter(peso__gt=1).values('pedido').aggregate(valorcom=Sum('valornf'))['valorcom']
        self.totalcomissaocascacda = totalcomissaocascacda

        if self.totalcomissaocasca != None or self.totalcomissaocascacda != None:
            if self.produto == 'Arroz em Casca':
                if 'CDA' in self.cliente.nome:
                    self.totalcomissaocasca =  (round(((float(self.totalcomissaocascacda) - (float(self.totalcomissaocascacda) * 0.07)) * float(self.comissaoc / 100)),2))
                    return self.totalcomissaocasca
                else:
                    self.totalcomissaocasca =  (round((((self.totalcomissaocasca / 50 ) * float(self.preco_produto)) * float(self.comissaoc / 100)),2))
                    return self.totalcomissaocasca
            elif self.produto == 'Semente':
                self.totalcomissaocasca = (round(((float(self.totalcomissaocascacda) * float(self.comissaoc / 100))),2))
                return self.totalcomissaocasca
            else:
                return 0
        else:
            return 0

    def saldototalcomissaocasca(self):
        filt = self.contrato
        saldototalcomissaocasca = Carga.objects.filter(pedido__contrato=filt).filter(pgcomissao=False).exclude(vpcomissaoc=None).exclude(peso=None).filter(vpcomissaoc__isnull=False).filter(peso__gt=1).values('pedido').aggregate(pesot=Sum('peso'))['pesot']
        self.saldototalcomissaocasca = saldototalcomissaocasca
        
        saldototalcomissaocascacda = Carga.objects.filter(pedido__contrato=filt).filter(pgcomissao=False).exclude(vpcomissaoc=None).exclude(valornf=None).filter(vpcomissaoc__isnull=False).filter(peso__gt=1).values('pedido').aggregate(valorcom=Sum('valornf'))['valorcom']
        self.saldototalcomissaocascacda = saldototalcomissaocascacda

        if self.saldototalcomissaocascacda != None:
            if self.produto == 'Arroz em Casca':
                if 'CDA' in self.cliente.nome:
                    self.saldototalcomissaocasca =  (round(((float(self.saldototalcomissaocascacda) - (float(self.saldototalcomissaocascacda) * 0.07)) * float(self.comissaoc / 100)),2))
                    return self.saldototalcomissaocasca
                elif self.saldototalcomissaocasca != None:
                    self.saldototalcomissaocasca =  (round((((self.saldototalcomissaocasca / 50 ) * float(self.preco_produto)) * float(self.comissaoc / 100)),2))
                    return self.saldototalcomissaocasca
                else:
                    return 0
            elif self.produto == 'Semente':
                self.saldototalcomissaocasca = (round(((float(self.saldototalcomissaocascacda) * float(self.comissaoc / 100))),2))
                return self.saldototalcomissaocasca
            else:
                return 0
        else:
            return 0

    
    
    def carregado(self):
        filt = self.contrato
        carregado = Carga.objects.filter(pedido__contrato=filt).values('pedido').aggregate(pesot=Sum('peso'))['pesot']    
        self.carregado = carregado
        if self.carregado == None:
            return 0
        else:
            return self.carregado

    def saldo(self):
        if self.situacao != 'a':
            return 0
        elif self.carregado == None:
            return self.quantidade_pedido
        else:
            return self.quantidade_pedido - self.carregado
    
    def previsto(self):
        filt = self.contrato 
        previsto = Carga.objects.filter(pedido__contrato=filt).filter(peso=0).values('pedido').aggregate(pesot=Sum('veiculo'))['pesot']    
        self.previsto = previsto
        if self.previsto == None:
            return 0
        else:
            return self.previsto
    
    def saldoprevisto(self):
        filt1 = self.contrato
        carregado = Carga.objects.filter(pedido__contrato=filt1).values('pedido').aggregate(pesot=Sum('peso'))['pesot']    
        self.carregado = carregado
        filt2 = self.contrato 
        previsto = Carga.objects.filter(pedido__contrato=filt2).filter(peso=0).values('pedido').aggregate(pesov=Sum('veiculo'))['pesov']    
        self.previsto = previsto
        if self.situacao != 'a':
            return 0
        elif self.carregado == None and self.previsto == None:
            return self.quantidade_pedido
        elif self.previsto == None:
            return self.quantidade_pedido - self.carregado
        elif self.carregado == None: 
            return self.quantidade_pedido - self.previsto
        else:
            return self.quantidade_pedido - self.carregado - self.previsto
    
    class Meta:
        ordering = ['-data','situacao','cliente']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos' 


    def __str__(self):
        return self.contrato   


class FaturaCargasComiFrete(Base):
    numero                 = models.CharField('Número Fatura', max_length=20, unique=True,  null=True, blank=True)
    empresa                = models.ForeignKey(EmpresaCorretora, on_delete=models.PROTECT, null=True, blank=True)
    data_fatura            = models.DateField('Data Fatura', null=True, blank=True, default=None, help_text="dd/mm/aaaa")
    data_fatura_vencimento = models.DateField('Data Vencimento Fatura', null=True, blank=True, default=None, help_text="dd/mm/aaaa")
    valor_total_fatura     = models.DecimalField('Valor Fatura', max_digits=20, decimal_places=2,  null=True, blank=True)
    transportadora         = models.ForeignKey(Transportadora, on_delete=models.PROTECT, null=True, blank=True)
    obs                    = models.TextField('Observação', max_length=500, blank=True, null=True)
    enviada_cobranca       = models.BooleanField('Enviada Cobrança?', default=False)
    pagamento_fatura       = models.BooleanField('Fatura Paga?', default=False)
    history                = HistoricalRecords()

    class Meta: 
        verbose_name = 'Fatura Terceiros'    
        verbose_name_plural = 'Faturas Terceiros'    
    
    def __str__(self):
        return self.numero

class PagamentoFaturaCargasComiFrete(Base):
    fatura                = models.ForeignKey(FaturaCargasComiFrete, on_delete=models.PROTECT, limit_choices_to = {'pagamento_fatura': False})
    data_fatura_pagamento = models.DateField('Data Pagamento Fatura', null=True, blank=True, help_text="dd/mm/aaaa")
    valor_pago_fatura     = models.DecimalField('Valor Pago Fatura', max_digits=20, decimal_places=2,  null=True, blank=True)
    pagador               = models.CharField('Pagador', max_length=30,  null=True, blank=True)
    conta_pagadora        = models.TextField('Conta Pagador', max_length=200, unique=True,  null=True, blank=True)
    obs                    = models.TextField('Observação', max_length=500, blank=True)
    history               = HistoricalRecords()

    class Meta: 
        verbose_name = 'Pagamento Fatura Terceiros'    
        verbose_name_plural = 'Pagamentos Faturas Terceiros'    
    
    def __str__(self):
        return self.fatura.numero



def get_default_transp_name():
    return Transportadora.objects.get(nome="GDX Log")


class Carga(Base):
    STATUS_CHOICES = (
        ('Agendado', 'Agendado'),
        ('Carregado','Carregado')
    )

    RODOTREM   = 51000
    BITREM     = 39000
    BICACAMBA  = 36900
    VANDERLEIA = 36000
    LSTRUCADA  = 33000
    TOCO       = 25500

    VEICULO_CHOICES = (
        (RODOTREM, 'Rodotrem'),
        (BITREM, 'Bitrem'),
        (BICACAMBA, 'Bicaçamba'),
        (VANDERLEIA, 'Vanderléia'),
        (LSTRUCADA, 'LS Trucada'),
        (TOCO, 'Toco')
    )

    
    chegada     = models.BooleanField('Chegou', default=False)
    ordem       = models.BooleanField('Ordem', default=False)
    tac         = models.BooleanField('TAC', default=False)
    pedido      = models.ForeignKey(Pedido, on_delete=models.PROTECT, limit_choices_to = {'situacao': 'a'})
    data        = models.DateField(help_text="dd/mm/aaaa")
    data_agenda = models.DateField('Data', null=True, blank=True, default=None, help_text="dd/mm/aaaa")
    buonny      = models.CharField('Buonny', max_length=15)
    transp      = models.ForeignKey(Transportadora, on_delete=models.PROTECT, default=get_default_transp_name)
    
    situacao  = models.CharField('Situação', max_length=12, choices=STATUS_CHOICES, default='Agendado')
    placa     = NameField('Placa', max_length=7, help_text="Somente dígitos")
    motorista = models.CharField('Motorista', max_length=25)
    peso      = models.PositiveIntegerField('Peso', default=0 ,blank=True, null=True)
    veiculo   = models.IntegerField('Veículo', choices=VEICULO_CHOICES)
    valor_mot = models.DecimalField('Frete', max_digits=5, decimal_places=2, null=True, blank=True)
    
    notafiscal  = models.CharField('NF', max_length=8,  null=True, blank=True)
    notafiscal2 = models.CharField('NF 2', max_length=8, unique=True,  null=True, blank=True)
    valornf     = models.DecimalField('Valor NF', max_digits=8, decimal_places=2,  null=True, blank=True)

    pgcomissao  = models.BooleanField('Pago', default=False)
    vpcomissaoc = models.DecimalField('Valor Comissao', max_digits=7, decimal_places=2, null=True, blank=True, default=0 )
    vpcomissaof = models.DecimalField('Valor Comissao F', max_digits=7, decimal_places=2, null=True, blank=True, default=0 )

    renda    = models.DecimalField('Renda', max_digits=4, decimal_places=2, null=True, blank=True)
    inteiro  = models.DecimalField('Inteiro', max_digits=4, decimal_places=2, null=True, blank=True)
    impureza = models.DecimalField('Impureza', max_digits=4, decimal_places=2,null=True, blank=True)
    umidade  = models.DecimalField('Umidade', max_digits=4, decimal_places=2, null=True, blank=True)

    gessado   = models.DecimalField('Gessado', max_digits=4, decimal_places=2,null=True,blank=True)
    bbranca   = models.DecimalField('B.Branca', max_digits=4, decimal_places=2,null=True, blank=True)
    amarelo   = models.DecimalField('Amarelo', max_digits=4, decimal_places=2,null=True, blank=True)
    manchpic  = models.DecimalField('Manch/Pic', max_digits=4, decimal_places=2,null=True, blank=True)
    vermelhos = models.DecimalField('Vermelhos', max_digits=4, decimal_places=2,null=True, blank=True)

    obs          = models.TextField('Observação', max_length=500, blank=True)
    obs_comissao = models.TextField('Observação Comissão', max_length=500, null=True, blank=True)

    gera_comi_frete  = models.BooleanField('Comi Frete', default=False)
    comi_frete_ton   = models.DecimalField('Comi Frete', max_digits=8, decimal_places=2, help_text="Valor por tonelada", null=True, blank=True)
    comi_frete_total = models.DecimalField('Comi F Total', max_digits=8, decimal_places=2, help_text="Valor Total", null=True, blank=True)
    
    comprovante_descarga = models.FileField('Comprovante Descarga', upload_to=get_file_path_comprovantes, null=True, blank=True)
    data_descarga        = models.DateField('Data Descarga', null=True, blank=True, default=None, help_text="dd/mm/aaaa")
    obs_descarga         = models.TextField('Observação Descarga', max_length=500, null=True, blank=True)

    nota_fiscal_arquivo = models.FileField('Nota Fiscal', upload_to=get_file_path_notafiscal, null=True, blank=True)
    nota_fiscal_xml     = models.FileField('NF Xml', upload_to=get_file_path_notafiscal, null=True, blank=True)

    fatura_frete_terceiros = models.ForeignKey(FaturaCargasComiFrete, on_delete=models.PROTECT, null=True, blank=True, limit_choices_to = {'pagamento_fatura': False})

    history      = HistoricalRecords()


    def valorcarga(self):
        if self.peso:
            if self.pedido.produto == 'Arroz em Casca':
                return ((self.peso / 50) * float(self.pedido.preco_produto))
            else:
                return ((self.peso / 30) * float(self.pedido.preco_produto))
        else:
            return 0

    @property
    def comissaocasca(self):
        if self.peso:
            if self.pedido.produto == 'Arroz em Casca':
                if 'CDA' in self.pedido.cliente.nome:
                    if self.notafiscal and self.notafiscal2:
                        return (round((((float(self.valornf) - (float(self.valornf) * 0.022589053)) * float(self.pedido.comissaoc / 100))),2))
                    if self.valornf != None:
                        return (round((((float(self.valornf) - (float(self.valornf) * 0.07)) * float(self.pedido.comissaoc / 100))),2))
                    else:
                        return 0
                else:
                    return (round((((self.peso / 50 ) * float(self.pedido.preco_produto)) * float(self.pedido.comissaoc / 100)),2))
            elif self.pedido.produto == 'Semente':
                return (round(((float(self.valornf) * float(self.pedido.comissaoc / 100))),2))
            else:
                return 0
        else:
            pass
    
    


    def icms(self):
        if self.pedido.cliente.estado == 'SP' or self.pedido.cliente.estado == 'PR':
            if self.peso:
                return (round(((self.peso / 1000) * float(self.pedido.preco_frete)) * 0.12,2 )) 
            else:
                return (round(((self.veiculo / 1000) * float(self.pedido.preco_frete)) * 0.12,2 ))
        else:
            if self.peso:
                return (round(((self.peso / 1000) * float(self.pedido.preco_frete)) * 0.07,2 )) 
            else:
                return (round(((self.veiculo / 1000) * float(self.pedido.preco_frete)) * 0.07,2 ))
    

    def data_intervalo_cargaedescarga(self):
        if self.data_agenda:
            intervalo = self.data - self.data_agenda
            self.data_intervalo_cargaedescarga = intervalo
            return self.data_intervalo_cargaedescarga.days
        else:
            pass
    
    def validate_unique(self, exclude=None):
        if self.notafiscal:
            qs = Carga.objects.filter(notafiscal=self.notafiscal).exclude(id=self.id)
            print(qs)
            if qs.filter(pedido__fornecedor__nome=self.pedido.fornecedor.nome).exists():
                print('nota fiscal já existe no DB')
                raise ValidationError("Esta Nota Fiscal com este Produtor já existe!")
            super(Carga, self).validate_unique(exclude)
    
    def save(self, *args, **kwargs):
        self.validate_unique()
        if self.pk is not None:
            orig = Carga.objects.get(pk=self.pk)
            if "GDX" in orig.transp.nome and "GDX" not in self.transp.nome:
                self.gera_comi_frete = True
        if not self.pk:
            if "GDX" in self.transp.nome:
                self.gera_comi_frete = False
            else:
                self.gera_comi_frete = True
        if not self.peso:
            self.peso = 0
        if not self.comi_frete_ton and self.gera_comi_frete == True:
            self.comi_frete_ton = 0
        if not self.comi_frete_total:
            if self.gera_comi_frete == True and self.comi_frete_ton != None and self.peso > 0:
                self.comi_frete_total =  self.comi_frete_ton * Decimal(self.peso / 1000)
        if self.comi_frete_ton and self.comi_frete_total :
            if self.comi_frete_ton > 0 and self.comi_frete_total > 0:
                self.gera_comi_frete = True
        super(Carga, self).save(*args, **kwargs)

    class Meta:
        ordering = ['situacao', '-data']
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'


    def __str__(self):
        return f'{self.placa} - {self.motorista}'



