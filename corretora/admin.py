from django.contrib import admin
from django.utils.formats import date_format


from .models import *
from simple_history.admin import SimpleHistoryAdmin

from django.forms import TextInput, Textarea
from django.db import models


from django.db.models import Sum








@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('cidade', 'estado')



class DatasemcargaAdmin(SimpleHistoryAdmin):
    list_display = ('get_data', 'cliente','ativo','get_data_alterado','get_data_criado')
    search_fields = ['data_semcarga', 'cliente']
    list_filter = ('data_semcarga', 'cliente')
    fieldsets = (
        ('Data Sem Descarga', {
            'fields': ('ativo','data_semcarga','cliente')
        }),        
        ('Observação', {
            'fields': ('obs',)
        }),    
    )
    history_list_display = ['data_semcarga','cliente','ativo','changed_fields']

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            camposalterados = str(delta.changed_fields)
            return camposalterados
        else:
            return 'Sem Alterações'
    

    def get_data(self,obj):
        return date_format(obj.data_semcarga, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_data.short_description = 'Data S/ Desc.'
    
    def get_data_criado(self,obj):        
        return obj.criados.strftime("%d/%m/%Y %H:%M:%S")
    get_data_criado.short_description = 'Criado'
    
    def get_data_alterado(self,obj):        
        return obj.modificado.strftime("%d/%m/%Y %H:%M:%S")
    get_data_alterado.short_description = 'Atualização'

admin.site.register(Datasemcarga, DatasemcargaAdmin)


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome','cpf_cnpj','get_insc','cidade','ativo','get_modificado') 
    fieldsets = (
        ('Situação', {
            'fields': ('ativo',)
        }),
        (None, {
            'fields': ('nome','cnpj_cpf','insc_estadual')
        }),
        ('Dados Bancáros',{
            'fields': ('banco','agencia','conta')
        }),
        (None, {
            'fields': (('cidade', 'estado'), 'endereco')
        }),
        ('Observação', {
            'fields': ('obs',)
        }),
    )
    
    
    # fields = [ 'nome','endereco',('cidade','estado'),('cnpj_cpf','insc_estadual'),('banco','agencia','conta')]
    search_fields = ['nome','endereco','cidade__cidade','cidade__estado']
    list_filter = ('ativo',)

    def get_modificado(self,obj):
        return date_format(obj.modificado, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_modificado.short_description = 'Atualização'



    def cpf_cnpj(self,obj):
        
        cpff = obj.cnpj_cpf
        if cpff:
            if len(cpff) <= 11:
                return f'{cpff[0:3]}.{cpff[3:6]}.{cpff[6:9]}-{cpff[9:]}'
            elif len(cpff) < 16:
                return f'{cpff[0:2]}.{cpff[2:5]}.{cpff[5:8]}/{cpff[8:12]}.{cpff[12:]}'
            else:
                return cpff
    cpf_cnpj.short_description = "CPF/CNPJ"

    def get_insc(self,obj):
        insc = obj.insc_estadual
        if insc:
            return f'{insc[0:3]}/{insc[3:]}'
    get_insc.short_description = "Insc. Estadual"

            

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia','cpf_cnpj','get_insc','cidade','ativo','get_modificado','dias_descarga','veiculos_dia','color')
    fieldsets = (
        ('Situação', {
            'fields': ('ativo',)
        }),
        ('Dados', {
            'fields': ('nome','nome_fantasia','cnpj_cpf','insc_estadual')
        }),
        ('Dados', {
            'fields': (('cidade', 'estado'), 'endereco','telefone', ('dias_descarga', 'veiculos_dia'))
        }),
        ('Observação', {
            'fields': ('obs','color')
        }),
    )
    
    # fields = [ 'nome','endereco','nome_fantasia',('cidade','estado')]
    search_fields = ['nome','nome_fantasia','cnpj_cpf','insc_estadual','ativo','endereco','cidade__cidade','cidade__estado']
    list_filter = ('ativo',)

    def get_modificado(self,obj):
        return date_format(obj.modificado, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_modificado.short_description = 'Atualização'

    def cpf_cnpj(self,obj):
        cpff = obj.cnpj_cpf
        if cpff:
            if len(cpff) <= 11:
                return f'{cpff[0:3]}.{cpff[3:6]}.{cpff[6:9]}-{cpff[9:]}'
            elif len(cpff) < 16:
                return f'{cpff[0:2]}.{cpff[2:5]}.{cpff[5:8]}/{cpff[8:12]}.{cpff[12:]}'
            else:
                return cpff
    cpf_cnpj.short_description = "CPF/CNPJ"
        
    def get_insc(self,obj):
        insc = obj.insc_estadual
        if insc:
            return f'{insc[0:3]}/{insc[3:]}'
    get_insc.short_description = "Insc. Estadual"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('contrato','situacao','get_data','fornecedor','get_cidade','cliente','get_preco','produto','renda','inteiro','variedade','tipo','get_peso_tipo','get_peso_total' ,'ativo','get_modificado')
    fieldsets = (
        ('Situação', {
            'fields': ('ativo','carregado','saldo')
        }),
        ('Dados', {
            'fields': ('contrato','situacao','data')
        }),
        ('Origem / Destino',{
            'fields': ('fornecedor','cliente')
        }),
        ('Dados do Produto', {
            'fields': (('produto','tipo'),('preco_produto','variedade'),'quantidade_pedido',('renda','inteiro','impureza', 'umidade','gessado','bbranca','amarelo','manchpic','vermelhos'))
        }),
        ('Comissão', {
            'fields': ('comissaoc','comissaof')
        }),
        ('Pagamento', {
            'fields': ('prazopgto','modalidadepgto')
        }),
        ('Observação', {
            'fields': ('obs',)
        }),
    )
    
    readonly_fields = [
        'carregado','saldo'
    ]
    
    # fields = ['contrato','situacao','data','fornecedor','cliente',('produto','preco_produto'),'quantidade_pedido',('renda','inteiro','impureza', 'umidade'),('variedade','tipo')]
    list_filter = ('ativo','situacao','tipo',)
    search_fields = ['contrato','quantidade_pedido','produto','situacao','data','fornecedor__nome','cliente__nome','preco_produto', 'variedade','tipo','quantidade_pedido']

    def get_modificado(self,obj):
        return date_format(obj.modificado, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_modificado.short_description = 'Atualização'

    def get_data(self,obj):
        return date_format(obj.data, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_data.short_description = 'Data'

    def get_preco(self,obj):
        valor = obj.preco_produto
        if valor:
            return f'R${valor}'
    get_preco.short_description = 'Preço'

    def get_peso_total(self,obj):
        peso = obj.quantidade_pedido
        if peso:
            return peso
    get_peso_total.short_description = "Quantidade Kg"

    def get_peso_tipo(self,obj):
        peso = obj.quantidade_pedido
        tipo = obj.tipo
        if peso:
            if tipo == 'Fardo 30Kg':
                fardo = peso / 30
                return f'{int(fardo)} Fardos'
            elif tipo == 'Saco 50Kg':
                saco = peso / 50
                return f'{int(saco)} Sacos'
            else:
                return peso
            
    get_peso_tipo.short_description = "Quantidade Unidade"

    def get_cidade(self,obj):
        return obj.fornecedor.cidade
    get_cidade.short_description = "Cidade"

@admin.register(Transportadora)
class TransportadoraAdmin(admin.ModelAdmin):
    list_display = ('nome','contato','email','telefone','cidade','estado','ativo','get_modificado')
    fields = ['ativo', ('nome','contato'),('cidade','estado'),('email','telefone'),'obs']

    def get_modificado(self,obj):
        return date_format(obj.modificado, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_modificado.short_description = 'Atualização'

# @admin.register(Carga)
class CargaAdmin(SimpleHistoryAdmin):
    list_display = ('placa','motorista','situacao','pedido','get_data','buonny','tac','ordem','get_fornecedor','get_cidade_fornecedor','get_cliente','transp','veiculo','notafiscal','get_modificado')
    fieldsets = (
    ('Agendamento', {
        'fields': ('pedido', ('data', 'buonny') )
    }),
    ('Carga', {
        'fields': (('ordem','tac','chegada'),'transp','situacao',('placa','motorista'),('peso','veiculo'),('notafiscal','notafiscal2','valornf'))
    }),
    ('Classificação', {
        'fields': (('renda','inteiro','impureza', 'umidade'),('gessado','bbranca','amarelo'),('manchpic','vermelhos'))
    }),
    ('Observação', {
            'fields': ('obs',)
        }),
    )
    raw_id_fields = ('pedido', )
    list_filter = ('ativo','situacao','pedido__fornecedor','pedido__cliente','pedido__situacao')
    search_fields = ['pedido__contrato','situacao','data','pedido__fornecedor__nome','placa','pedido__cliente__nome','pedido__tipo','motorista','peso','veiculo','buonny','notafiscal','notafiscal2','valornf']
    history_list_display = ["situacao","ordem","get_data","peso","agendamento","notafiscal","pedido","motorista","placa","valornf","valor_mot","changed_fields"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            camposalterados = str(delta.changed_fields)
            return camposalterados
        else:
            return 'Sem Alterações'
    
    def valor_mot(self,obj):
        valor = obj.valor_mot
        if valor:
            valor = f'R$ {valor}'
            return valor
    valor_mot.short_description = 'Preço'

    def get_data(self,obj):
        return date_format(obj.data, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_data.short_description = 'Data'
    
    def ordem(self,obj):
        if obj.ordem == True:
            return 'Enviada'
        else:
            return "Não"        
    
    def agendamento(self,obj):
        if obj.data_agenda:
            return date_format(obj.data_agenda, format='SHORT_DATE_FORMAT', use_l10n=True)
        else:
            return 'Sem Data'
    agendamento.short_description = 'Data Agenda'

    def get_modificado(self,obj):
        return date_format(obj.modificado, format='SHORT_DATE_FORMAT', use_l10n=True)
    get_modificado.short_description = 'Atualização'

    def get_cidade_fornecedor(self, obj):
        return obj.pedido.fornecedor.cidade
    get_cidade_fornecedor.short_description = 'Origem'

    def get_fornecedor(self,obj):
        return obj.pedido.fornecedor.nome
    get_fornecedor.short_description = 'Fornecedor'

    def get_cliente(self,obj):
        return obj.pedido.cliente.nome_fantasia
    get_cliente.short_description = 'Cliente'
     
admin.site.register(Carga, CargaAdmin)
    
    
    