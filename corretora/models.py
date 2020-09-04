from django.db import models
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models import F, FloatField, Sum, Avg, Count

import datetime


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).upper()


class Base(models.Model):
    criados = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)

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


class Cidade(Base):
    cidade = models.CharField('Cidade', max_length=40, unique=True)
    estado = models.TextField('Estado', max_length=12, choices=UF_CHOICES)

    class Meta:
        ordering = ['cidade']
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return f'{self.cidade} - {self.estado}'


PROD_CHOICES = (
    ('Arroz em Casca', 'Arroz em Casca'),
    ('Arroz Beneficiado', 'Arroz Benenficiado')
)


class Fornecedor(Base):
    nome = models.CharField('Nome', max_length=50)
    cnpj_cpf = models.CharField('CNPJ/CPF', max_length=14, unique=True, null=True, help_text="digite apenas números")
    insc_estadual = models.CharField('Inscrição Estadual',  unique=True, max_length=13,null=True,help_text="digite apenas números")
    banco = models.CharField('Banco', max_length=10, blank=True)
    agencia = models.CharField('Agencia', max_length=5,blank=True, help_text="digite apenas números")
    conta = models.CharField('Conta', max_length=12,blank=True, help_text="digite apenas números")
    endereco = models.CharField('Endereço', max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    obs = models.TextField('Observação', max_length=125, blank=True)

    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.nome

def set_default_fornecedor():
    return Fornecedor.objects.get_or_create(nome='Fornecedor Deletado')[0] #(objeto, boolean)
       

class Cliente(Base):
    nome = models.CharField('Nome', max_length=50)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=50)
    cnpj_cpf = models.CharField('CNPJ/CPF', max_length=14,  unique=True,  null=True, help_text="digite apenas números")
    insc_estadual = models.CharField('Inscrição Estadual',  unique=True,  max_length=10, help_text="digite apenas números",null=True)
    telefone = models.CharField('Telefone',max_length=11, help_text="digite apenas números", null=True)
    endereco = models.CharField('Endereço', max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    obs = models.TextField('Observação', max_length=125, blank=True)

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
        
            
        if 'CDA' in filt:
            if comisemanacda == None:
                self.comissaosemanacasca = 0
                return self.comissaosemanacasca            
            else:
                self.comissaosemanacasca = comisemanacda
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
            
        if 'CDA' in filt:
            if comimescascacda == None:
                self.comissaomescasca = 0
                return self.comissaomescasca            
            else:
                self.comissaomescasca = comimescascacda
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
        lastm = today.month - 1 if today.month > 1 else 12
        lastmy = today.year if today.month > lastm else today.year -1
        comimesanteriorcascacda = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteriorcasca = Carga.objects.filter(data__year=lastmy, data__month=lastm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
            
        if 'CDA' in filt:
            if comimesanteriorcascacda == None:
                self.comissaomescascaanterior = 0
                return self.comissaomescascaanterior            
            else:
                self.comissaomescascaanterior = comimesanteriorcascacda
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
        lastmm = today.month - 2 if today.month > 2 else 12
        lastmmy = today.year if today.month > lastmm else today.year -1
        comimesanteanteriorcascacda = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimesanteanteriorcasca = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
            
        if 'CDA' in filt:
            if comimesanteanteriorcascacda == None:
                self.comissaomescascaanteanterior = 0
                return self.comissaomescascaanteanterior            
            else:
                self.comissaomescascaanteanterior = comimesanteanteriorcascacda
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
        lastmm3 = today.month - 3 if today.month > 3 else 12
        lastmmy3 = today.year if today.month > lastmm3 else today.year -1
        comimescascatresanteriorcda = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comimestresanteriorcasca = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
            
        if 'CDA' in filt:
            if comimescascatresanteriorcda == None:
                self.comissaomescascatresanterior = 0
                return self.comissaomescascatresanterior            
            else:
                self.comissaomescascatresanterior = comimescascatresanteriorcda
                return self.comissaomescascatresanterior
        else:
            if comimestresanteriorcasca == None:
                self.comissaomescascatresanterior = 0
                return self.comissaomescascatresanterior
            else:
                self.comissaomescascatresanterior = comimestresanteriorcasca
                return self.comissaomescascatresanterior
            
    
    
    def comissaoabertocasca(self):
        filt = self.nome_fantasia               
        comiabertocda = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
        comiaberto = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome_fantasia=filt).filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))['somacomi']
            
        if 'CDA' in filt:
            if comiabertocda == None:
                self.comissaoabertocasca = 0
                return self.comissaoabertocasca            
            else:
                self.comissaoabertocasca = comiabertocda
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
        
        if comiabertototalcda == None and comiabertototal == None:
                self.comissaoabertocascatotal = 0
                return self.comissaoabertocascatotal            
        elif comiabertototalcda == None and comiabertototal > 0:
            self.comissaoabertocascatotal = comiabertototal
            return self.comissaoabertocascatotal 
        elif  comiabertototalcda > 0 and comiabertototal == None:
            self.comissaoabertocascatotal = comiabertototalcda
            return self.comissaoabertocascatotal 
        else:
            self.comissaoabertocascatotal = comiabertototal + comiabertototalcda
            return self.comissaoabertocascatotal 



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

    def carregadomesanteanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        lastmm = today.month - 2 if today.month > 2 else 12
        lastmmy = today.year if today.month > lastmm else today.year -1
        carregadomesanteanterior = Carga.objects.filter(data__year=lastmmy, data__month=lastmm).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomesanteanterior = carregadomesanteanterior
        if self.carregadomesanteanterior == None:
            self.carregadomesanteanterior = 0
            return self.carregadomesanteanterior
        else:
            return self.carregadomesanteanterior

    def carregadomestresanterior(self):
        filt = self.nome_fantasia
        today = datetime.date.today()
        lastmm3 = today.month - 3 if today.month > 3 else 12
        lastmmy3 = today.year if today.month > lastmm3 else today.year -1
        carregadomestresanterior = Carga.objects.filter(data__year=lastmmy3, data__month=lastmm3).filter(pedido__cliente__nome_fantasia=filt).filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']
        self.carregadomestresanterior = carregadomestresanterior
        if self.carregadomestresanterior == None:
            self.carregadomestresanterior = 0
            return self.carregadomestresanterior
        else:
            return self.carregadomestresanterior
    
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
        carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(pedido__situacao='a').filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']            
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
        carregado = Carga.objects.filter(pedido__cliente__nome_fantasia=filt).filter(pedido__situacao='a').filter(situacao='Carregado').values('peso').aggregate(pesot=Sum('peso'))['pesot']            
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
    

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome_fantasia

def set_default_cliente():
    return Cliente.objects.get_or_create(nome='Cliente Deletado')[0] #(objeto, boolean)


class Transportadora(Base):
    nome = models.CharField('Nome', max_length=20, unique=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    estado = models.TextField('Estado', max_length=12, choices=UF_CHOICES)
    contato = models.CharField('Contato', max_length=30, blank=True)
    telefone = models.CharField('Telefone', max_length=15, blank=True, help_text="digite apenas números")
    email = models.EmailField('E-mail', max_length=30,blank=True)
    obs = models.TextField('Observação', max_length=125, blank=True)    

    class Meta:
        ordering = ['criados','nome']
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
        ('Fardo 30Kg', 'Fardo 30Kg'),
        ('Big Bag', 'Big Bag')
    )

    contrato = NameField('Numero', max_length=9, unique=True)
    situacao = models.CharField('Situação', max_length=12, choices=SIT_CHOICES, default='Aberto')
    data = models.DateField(default=timezone.now, help_text="dd/mm/aaaa")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    preco_produto = models.DecimalField('Preço Produto', max_digits=8, decimal_places=2)
    preco_frete = models.DecimalField('Frete', max_digits=5, decimal_places=2)

    comissaoc = models.DecimalField('Comissão C', max_digits=4, decimal_places=2 )
    comissaof = models.DecimalField('Comissão F', max_digits=4, decimal_places=2 ,null=True, blank=True )

    prazopgto = models.CharField('Prazo Pgto', max_length=20,null=True, blank=True )
    modalidadepgto = models.CharField('Mod. Pgto', max_length=30,null=True, blank=True )

    renda = models.DecimalField('Renda', max_digits=4, decimal_places=2)
    inteiro = models.DecimalField('Inteiro', max_digits=4, decimal_places=2)
    impureza = models.DecimalField('Impureza', max_digits=4, decimal_places=2,null=True, blank=True)
    umidade = models.DecimalField('Umidade', max_digits=4, decimal_places=2)

    gessado = models.DecimalField('Gessado', max_digits=4, decimal_places=2,null=True,blank=True)
    bbranca = models.DecimalField('B. Branca', max_digits=4, decimal_places=2,null=True, blank=True)
    amarelo = models.DecimalField('Amarelo', max_digits=4, decimal_places=2,null=True, blank=True)
    manchpic = models.DecimalField('Manch/ Pic', max_digits=4, decimal_places=2,null=True, blank=True)
    vermelhos = models.DecimalField('Vermelhos', max_digits=4, decimal_places=2,null=True, blank=True)

    variedade = models.CharField('Variedade', max_length=12)
    produto = models.CharField('Produto', max_length=17, choices=PROD_CHOICES,default='Arroz em Casca')
    tipo = models.CharField('Tipo', max_length=12, choices=TIPO_CHOICES, default='Saco 50Kg')
    quantidade_pedido = models.PositiveIntegerField('Quantidade Pedido', help_text="Peso em Kg")
    

    obs = models.TextField('Observação', max_length=500, blank=True)    


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
        ordering = ['data', 'cliente','situacao']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos' 


    def __str__(self):
        return self.contrato   





class Carga(Base):
    STATUS_CHOICES = (
        ('Agendado', 'Agendado'),
        ('Carregado','Carregado')
    )

    RODOTREM = 51000
    BITREM = 39000
    BICACAMBA = 37000
    VANDERLEIA = 36000
    LSTRUCADA = 32000
    TOCO = 26000

    VEICULO_CHOICES = (
        (RODOTREM, 'Rodotrem'),
        (BITREM, 'Bitrem'),
        (BICACAMBA, 'Bicaçamba'),
        (VANDERLEIA, 'Vanderléia'),
        (LSTRUCADA, 'LS Trucada'),
        (TOCO, 'Toco')
    )

    
    chegada = models.BooleanField('Chegou', default=False)
    ordem = models.BooleanField('Ordem', default=False)
    tac = models.BooleanField('TAC', default=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, limit_choices_to = {'situacao': 'a'})
    data = models.DateField(help_text="dd/mm/aaaa")
    buonny = models.CharField('Buonny', max_length=15)
    transp = models.ForeignKey(Transportadora, on_delete=models.PROTECT, default='GDX Log')
    
    situacao = models.CharField('Situação', max_length=12, choices=STATUS_CHOICES, default='Agendado')
    placa = NameField('Placa', max_length=7)
    motorista = models.CharField('Motorista', max_length=25)
    peso = models.PositiveIntegerField('Peso', default=0 ,blank=True, null=True)
    veiculo = models.IntegerField('Veículo', choices=VEICULO_CHOICES)
    valor_mot = models.DecimalField('Frete', max_digits=5, decimal_places=2, null=True, blank=True)
    
    notafiscal = models.CharField('NF', max_length=8, unique=True,  null=True, blank=True)
    notafiscal2 = models.CharField('NF 2', max_length=8, unique=True,  null=True, blank=True)
    valornf = models.DecimalField('Valor NF', max_digits=8, decimal_places=2,  null=True, blank=True)

    pgcomissao = models.BooleanField('Pago', default=False)
    vpcomissaoc = models.DecimalField('Valor Comissao', max_digits=7, decimal_places=2, null=True, blank=True, default=0 )
    vpcomissaof = models.DecimalField('Valor Comissao F', max_digits=7, decimal_places=2, null=True, blank=True, default=0 )

    renda = models.DecimalField('Renda', max_digits=4, decimal_places=2, null=True, blank=True)
    inteiro = models.DecimalField('Inteiro', max_digits=4, decimal_places=2, null=True, blank=True)
    impureza = models.DecimalField('Impureza', max_digits=4, decimal_places=2,null=True, blank=True)
    umidade = models.DecimalField('Umidade', max_digits=4, decimal_places=2, null=True, blank=True)

    gessado = models.DecimalField('Gessado', max_digits=4, decimal_places=2,null=True,blank=True)
    bbranca = models.DecimalField('B.Branca', max_digits=4, decimal_places=2,null=True, blank=True)
    amarelo = models.DecimalField('Amarelo', max_digits=4, decimal_places=2,null=True, blank=True)
    manchpic = models.DecimalField('Manch/Pic', max_digits=4, decimal_places=2,null=True, blank=True)
    vermelhos = models.DecimalField('Vermelhos', max_digits=4, decimal_places=2,null=True, blank=True)

    obs = models.TextField('Observação', max_length=125, blank=True) 


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
                    if self.valornf != None:
                        return (round((((float(self.valornf) - (float(self.valornf) * 0.07)) * float(self.pedido.comissaoc / 100))),2))
                    else:
                        return 0
                else:
                    return (round((((self.peso / 50 ) * float(self.pedido.preco_produto)) * float(self.pedido.comissaoc / 100)),2))
            else:
                return 0
        else:
            pass
    
    


    def icms(self):
        if self.pedido.cliente.estado == 'SP':
            if self.peso:
                return (round(((self.peso / 1000) * float(self.pedido.preco_frete)) * 0.12,2 )) 
            else:
                return (round(((self.veiculo / 1000) * float(self.pedido.preco_frete)) * 0.12,2 ))
        else:
            if self.peso:
                return (round(((self.peso / 1000) * float(self.pedido.preco_frete)) * 0.07,2 )) 
            else:
                return (round(((self.veiculo / 1000) * float(self.pedido.preco_frete)) * 0.07,2 ))

    class Meta:
        ordering = ['situacao', 'data']
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'


    def __str__(self):
        return f'{self.placa} - {self.motorista}'

