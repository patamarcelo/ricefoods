from django.db import models
from django.db.models import Sum
from django.utils import timezone


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
    quantidade_pedido = models.PositiveIntegerField('Quantidade Pedido', help_text="Peso em Tonelada")
    

    obs = models.TextField('Observação', max_length=125, blank=True)    
    
    def totalcomissaocasca(self):
        filt = self.contrato
        totalcomissaocasca = Carga.objects.filter(pedido__contrato=filt).filter(peso__gt=1).values('pedido').aggregate(pesot=Sum('peso'))['pesot']
        self.totalcomissaocasca = totalcomissaocasca
        if self.totalcomissaocasca != None:
            if self.produto == 'Arroz em Casca':
                self.totalcomissaocasca =  (round((((self.totalcomissaocasca / 50 ) * float(self.preco_produto)) * float(self.comissaoc / 100)),2))
                return self.totalcomissaocasca
            else:
                return 0
        else:
            pass

    
    
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
        if self.carregado == None:
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
    TOCO = 28000

    VEICULO_CHOICES = (
        (RODOTREM, 'Rodotrem'),
        (BITREM, 'Bitrem'),
        (BICACAMBA, 'Bicaçamba'),
        (VANDERLEIA, 'Vanderléia'),
        (LSTRUCADA, 'LS Trucada'),
        (TOCO, 'Toco')
    )

    

    ordem = models.BooleanField('Ordem', default=False)
    tac = models.BooleanField('TAC', default=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, limit_choices_to = {'situacao': 'a'})
    data = models.DateField(help_text="dd/mm/aaaa")
    buonny = models.CharField('Buonny', max_length=15)
    transp = models.ForeignKey(Transportadora, on_delete=models.PROTECT, default='GDX Log')
    
    situacao = models.CharField('Situação', max_length=12, choices=STATUS_CHOICES, default='Agendado')
    placa = NameField('Placa', max_length=7)
    motorista = models.CharField('Motorista', max_length=20)
    peso = models.PositiveIntegerField('Peso', default=0 ,blank=True, null=True)
    veiculo = models.IntegerField('Veículo', choices=VEICULO_CHOICES)
    valor_mot = models.DecimalField('Frete', max_digits=5, decimal_places=2, null=True, blank=True)
    
    notafiscal = models.CharField('NF', max_length=8, unique=True,  null=True, blank=True)
    notafiscal2 = models.CharField('NF 2', max_length=8, unique=True,  null=True, blank=True)
    valornf = models.DecimalField('Valor NF', max_digits=8, decimal_places=2,  null=True, blank=True)

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

    def comissaocasca(self):
        if self.peso:
            if self.pedido.produto == 'Arroz em Casca':
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

