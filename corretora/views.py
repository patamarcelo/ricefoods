from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from django.core import serializers

from django.core.mail import send_mail, EmailMessage
import re

from django.db.models import Q



from django.db.models import F, FloatField, Sum, Avg, Count
from easy_pdf.views import PDFTemplateResponseMixin

import datetime
# Graficos
import json
from json import dumps
# Graficos

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from braces.views import SuperuserRequiredMixin
from django.views.generic.list import MultipleObjectMixin



from .models import *

from .filters import CargasFilter
from django_filters.views import FilterView
from . import filters

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from .forms import CompDescargaForm

class CargasFiltradasView(LoginRequiredMixin, FilterView):
    login_url = 'login'    
    model = Carga
    template_name = 'cargasfiltro.html'  
    paginate_by = 100
    filterset_class = CargasFilter
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 


    def get_context_data(self, **kwargs):
        context = super(CargasFiltradasView, self).get_context_data(**kwargs)
        context['cargas'] = Carga.objects.all
        queryset = self.get_queryset()
        filter = CargasFilter(self.request.GET, queryset=queryset)                
        context['pesototal'] = filter.qs.filter(situacao='Carregado').filter(peso__gt=0).values('peso').aggregate(Sum(F'peso'))
        context['agendatotal'] = filter.qs.filter(situacao='Agendado').filter(peso=0).values('veiculo').aggregate(Sum('veiculo'))   
        context['motoristas_autocomplete_json'] = json.dumps(
            [
                {
                    'motorista': obj.motorista
                }
                for obj in Carga.objects.order_by('motorista').distinct('motorista').all()   
            ]
        )     
        context['placas_autocomplete_json'] = json.dumps(
            [
                {
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('placa').distinct('placa').all()   
            ]
        )     
        def get_total_comissao():
            total = 0                        
            for carga in filter.qs.filter(pgcomissao=False).filter(situacao='Carregado'):
                if carga.comissaocasca != 0 and carga.comissaocasca != None:
                    total = total + carga.comissaocasca
            return total
        context['comitotal'] = get_total_comissao()
        return context

class CargasFiltradasComissaoFreteView(LoginRequiredMixin, SuperuserRequiredMixin, FilterView):
    login_url = 'login'    
    model = Carga
    template_name = 'cargasfiltro_comissaofrete.html'  
    filterset_class = CargasFilter
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 

    def get_queryset(self):
        filter1 = "GDX"
        return Carga.objects.filter(~Q(transp__nome__startswith=filter1))


    def get_context_data(self, **kwargs):
        context = super(CargasFiltradasComissaoFreteView, self).get_context_data(**kwargs)
        context['cargas'] = Carga.objects.all
        context['transportadoras'] = Transportadora.objects.all
        context['empresas'] = EmpresaCorretora.objects.all
        queryset = self.get_queryset()
        filter = CargasFilter(self.request.GET, queryset=queryset)                
        context['pesototal'] = filter.qs.filter(situacao='Carregado').filter(peso__gt=0).values('peso').aggregate(Sum(F'peso'))
        context['agendatotal'] = filter.qs.filter(situacao='Agendado').filter(peso=0).values('veiculo').aggregate(Sum('veiculo'))   
        context['motoristas_autocomplete_json'] = json.dumps(
            [
                {
                    'motorista': obj.motorista
                }
                for obj in Carga.objects.order_by('motorista').distinct('motorista').all()   
            ]
        )     
        context['placas_autocomplete_json'] = json.dumps(
            [
                {
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('placa').distinct('placa').all()   
            ]
        )     
        def get_total_comissao():
            total = 0                        
            for carga in filter.qs.filter(pgcomissao=False).filter(situacao='Carregado'):
                if carga.comissaocasca != 0 and carga.comissaocasca != None:
                    total = total + carga.comissaocasca
            return total
        context['comitotal'] = get_total_comissao()
        return context

class BasetwoView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    login_url = 'login'    
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(BasetwoView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.order_by('situacao','cliente','-data','-id').all
        context['chart'] = Pedido.objects.order_by('data','id').all
        context['fornecedores'] = Fornecedor.objects.order_by('nome').all
        context['cargas'] = Carga.objects.order_by('situacao','-data','pedido__cliente','ordem','buonny','pedido_id').all
        context['clientes'] = Cliente.objects.order_by('-nome').all
        
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        context['carga_ok_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        context['carga_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_rus_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_ok_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        context['carga_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_cda_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        
        context['total_ped_abert_rus'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='Ruston').values('contrato').aggregate(Count('contrato'))
        context['total_abert_rus'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='Ruston').values('contrato').aggregate(Sum('quantidade_pedido'))
        context['total_carr_rus'] = Carga.objects.filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('peso'))
        context['total_agen_rus'] = Carga.objects.filter(pedido__situacao='a').exclude(pedido__contrato='901').filter(pedido__ativo=True).filter(situacao='Agendado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('veiculo'))
        context['total_agen_rus2'] = Carga.objects.filter(pedido__contrato='901').filter(situacao='Agendado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('veiculo'))
        
        context['total_ped_abert_cda'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='CDA').values('contrato').aggregate(Count('contrato'))
        context['total_abert_cda'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='CDA').values('contrato').aggregate(Sum('quantidade_pedido'))
        context['total_carr_cda'] = Carga.objects.filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('peso'))
        context['total_agen_cda'] = Carga.objects.filter(pedido__situacao='a').exclude(pedido__contrato='900').filter(pedido__ativo=True).filter(situacao='Agendado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('veiculo'))
        context['total_agen_cda2'] = Carga.objects.filter(pedido__contrato='900').filter(situacao='Agendado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('veiculo'))
        
        context['comisemrus'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        context['comisemcda'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        
        context['comimesrus'] = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        context['comimescda'] = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        
        context['comiaberus'] = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        context['comiabecda'] = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        
        return context

class BaseView(LoginRequiredMixin, TemplateView):
    login_url = 'login'    
    template_name = 'basecorretora.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.order_by('situacao','cliente','-data','-id')[:100]
        context['chart'] = Pedido.objects.order_by('data','id').all
        context['fornecedores'] = Fornecedor.objects.order_by('nome').all
        context['cargas'] = Carga.objects.order_by('situacao','-data','ordem','chegada','buonny','pedido__cliente')[:100]
        context['clientes'] = Cliente.objects.order_by('-nome').all
        
        # today = datetime.date.today()
        # monday = today - datetime.timedelta(days=today.weekday())
        # sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        # context['carga_ok_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        # context['carga_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        # context['carga_rus_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        # context['carga_ok_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        # context['carga_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        # context['carga_cda_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        
        # context['total_ped_abert_rus'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='Ruston').values('contrato').aggregate(Count('contrato'))
        # context['total_abert_rus'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='Ruston').values('contrato').aggregate(Sum('quantidade_pedido'))
        # context['total_carr_rus'] = Carga.objects.filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('peso'))
        # context['total_agen_rus'] = Carga.objects.filter(pedido__situacao='a').exclude(pedido__contrato='901').filter(pedido__ativo=True).filter(situacao='Agendado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('veiculo'))
        # context['total_agen_rus2'] = Carga.objects.filter(pedido__contrato='901').filter(situacao='Agendado').filter(pedido__cliente__nome='Ruston').values('pedido').aggregate(Sum('veiculo'))
        
        # context['total_ped_abert_cda'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='CDA').values('contrato').aggregate(Count('contrato'))
        # context['total_abert_cda'] = Pedido.objects.filter(situacao='a').filter(ativo=True).filter(cliente__nome='CDA').values('contrato').aggregate(Sum('quantidade_pedido'))
        # context['total_carr_cda'] = Carga.objects.filter(pedido__situacao='a').filter(pedido__ativo=True).filter(situacao='Carregado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('peso'))
        # context['total_agen_cda'] = Carga.objects.filter(pedido__situacao='a').exclude(pedido__contrato='900').filter(pedido__ativo=True).filter(situacao='Agendado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('veiculo'))
        # context['total_agen_cda2'] = Carga.objects.filter(pedido__contrato='900').filter(situacao='Agendado').filter(pedido__cliente__nome='CDA').values('pedido').aggregate(Sum('veiculo'))
        
        # context['comisemrus'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        # context['comisemcda'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        
        # context['comimesrus'] = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        # context['comimescda'] = Carga.objects.filter(data__year=today.year, data__month=today.month).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        
        # context['comiaberus'] = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome='Ruston').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('peso') / 50) * F('pedido__preco_produto') * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        # context['comiabecda'] = Carga.objects.filter(pgcomissao=False).filter(pedido__cliente__nome='CDA').filter(pedido__produto='Arroz em Casca').filter(situacao='Carregado').values('peso').aggregate(somacomi=Sum((F('valornf') - (F('valornf') * 0.07)) * (F('pedido__comissaoc') / 100), output_field=FloatField()))
        return context

    


class PedidosView(LoginRequiredMixin, ListView):
    login_url = 'login'    
    models = Pedido
    paginate_by = 23
    ordering = ['situacao', 'cliente','-data','-id']
    template_name = 'pedido.html'
    queryset = Pedido.objects.all()
    context_object_name = 'pedidos'


class CreatePedidosView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'    
    model = Pedido
    template_name = 'pedido_form_add.html'
    success_message = "%(contrato)s - %(fornecedor)s - %(cliente)s inserido com sucesso!!"
    fields = '__all__'
    # success_url = reverse_lazy('pedidos')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('pedidos')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_pedidos')
        else:
            return reverse('pedidos')

class UpdatePedidosView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Pedido
    template_name = 'pedido_form.html'
    success_message = 'Pedido %(fornecedor)s -> %(cliente)s atualizado com sucesso!!'
    # fields = '__all__'
    fields = ('ativo','situacao','data','fornecedor','cliente','preco_produto','preco_frete',
                'comissaoc','comissaof','prazopgto','modalidadepgto',
               'renda', 'inteiro', 'impureza', 'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
               'variedade','produto','tipo','quantidade_pedido','obs', 'pedido_arquivo' )
    success_url = reverse_lazy('pedidos')

class DeletePedidosView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    
    model = Pedido
    template_name = 'pedido_del.html'
    success_message = "Pedido excluído com sucesso!!"
    success_url = reverse_lazy('pedidos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePedidosView, self).delete(request, *args, **kwargs)

# <!---------Fornecedores----------------------->

class FornecedoresView(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    models = Fornecedor
    ordering = ['nome']
    template_name = 'fornecedores.html'
    queryset = Fornecedor.objects.all()
    context_object_name = 'fornecedores'

class CreateFornecedoresView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    
    model = Fornecedor
    template_name = 'fornecedor_form_add.html'
    success_message = "%(nome)s cadastrado com sucesso!!"
    fields = '__all__'
    # success_url = reverse_lazy('corretora')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('fornecedores')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_fornecedor')
        else:
            return reverse('fornecedores')

class UpdateFornecedoresView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Fornecedor
    template_name = 'fornecedor_form.html'
    success_message = 'Fornecedor atualizado com sucesso!!'
    fields = '__all__'
    success_url = reverse_lazy('fornecedores')

class DeleteFornecedoresView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    
    model = Fornecedor
    template_name = 'fornecedor_del.html'
    success_message = "Fornecedor excluído com sucesso!!"
    success_url = reverse_lazy('fornecedores')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteFornecedoresView, self).delete(request, *args, **kwargs)


##Cargas <---------------->

# ------------------------------------relatorio_classificacao-----------------------------------
class DetailCargasView(LoginRequiredMixin, ListView):
    model = Carga
    template_name = 'cargas_detail.html'
    context_object_name = 'cargas' 



    def get_context_data(self, **kwargs):
        context = super(DetailCargasView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.filter(pk=self.kwargs.get('pk'))
        context['cargas'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk'))
        context['total'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk')).values('peso').aggregate(Sum('peso'))
        context['totalnf'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk')).values('valornf').aggregate(Sum('valornf')) 
                
        context['mrenda'] = Carga.objects.all().filter(situacao='Carregado').filter(renda__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('renda').aggregate(w_avg=Sum((F('renda') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['minteiro'] = Carga.objects.all().filter(situacao='Carregado').filter(inteiro__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('inteiro').aggregate(w_avg=Sum((F('inteiro') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mimpureza'] = Carga.objects.all().filter(situacao='Carregado').filter(impureza__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('impureza').aggregate(w_avg=Sum((F('impureza') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mumidade'] = Carga.objects.all().filter(situacao='Carregado').filter(umidade__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('umidade').aggregate(w_avg=Sum((F('umidade') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mgessado'] = Carga.objects.all().filter(situacao='Carregado').filter(gessado__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('gessado').aggregate(w_avg=Sum((F('gessado') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mbbranca'] = Carga.objects.all().filter(situacao='Carregado').filter(bbranca__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('bbranca').aggregate(w_avg=Sum((F('bbranca') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mamarelo'] = Carga.objects.all().filter(situacao='Carregado').filter(amarelo__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('amarelo').aggregate(w_avg=Sum((F('amarelo') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mmanchpic'] = Carga.objects.all().filter(situacao='Carregado').filter(manchpic__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('manchpic').aggregate(w_avg=Sum((F('manchpic') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        context['mvermelhos'] = Carga.objects.all().filter(situacao='Carregado').filter(vermelhos__gte=0).filter(pedido_id=self.kwargs.get('pk')).values('vermelhos').aggregate(w_avg=Sum((F('vermelhos') * F('peso')), output_field=FloatField()) / Sum(F('peso'), output_field=FloatField()))
        
        
        return context

# ------------------------------------comissoes-----------------------------------
class ComissCargasView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Carga
    template_name = 'cargas_detail_comiss.html'
    context_object_name = 'cargas' 



    def get_context_data(self, **kwargs):
        context = super(ComissCargasView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.filter(pk=self.kwargs.get('pk'))
        context['cargas'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk'))
        context['totalpeso'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk')).values('peso').aggregate(Sum('peso'))
        context['totalnf'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pedido_id=self.kwargs.get('pk')).values('valornf').aggregate(Sum('valornf'))
        context['totalpago'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pgcomissao=True).filter(pedido_id=self.kwargs.get('pk')).values('vpcomissaoc').aggregate(Sum('vpcomissaoc'))
        context['totalaberto'] = Carga.objects.order_by('data').filter(situacao='Carregado').filter(pgcomissao=False).filter(pedido_id=self.kwargs.get('pk')).values('vpcomissaoc').aggregate(Count('vpcomissaoc'))
        return context

class CargasAgendamentoView(LoginRequiredMixin, ListView):
    login_url = 'login'    
    models = Carga    
    ordering = ['-situacao','-data_agenda','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'agendamento.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    

    def get_queryset(self):
        queryset = Carga.objects.order_by('-situacao','data_agenda')
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
        filt1 = dias_da_semana()[0]
        filt2 = dias_da_semana()[-1]
        return queryset.filter(data_agenda__gte=filt1).filter(data_agenda__lte=filt2).filter(pedido__cliente__nome='Ruston')

    def get_context_data(self, **kwargs):
        context = super(CargasAgendamentoView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        return context

class CargasAgendamentoViewTeste(LoginRequiredMixin, ListView):
    login_url = 'login'    
    models = Carga    
    ordering = ['-situacao','-data_agenda','-modificado','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'agendamentoTeste.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 
    

    def get_context_data(self, **kwargs):
        context = super(CargasAgendamentoViewTeste, self).get_context_data(**kwargs)
        filt1 = datetime.datetime.now() - datetime.timedelta(15)
        filt_data = filt1.strftime("%Y-%m-%d")
        filt2 = 'Ruston - SP'
        context['query_cargas_json'] = json.dumps(
            [
                {
                    'situacao': obj.situacao,
                    'data_agenda' : obj.data_agenda.strftime("%Y-%m-%d"),
                    'placa': obj.placa,
                    'motorista': obj.motorista,
                    'nfiscal': obj.notafiscal,
                    'peso': obj.peso,
                    'veiculo': obj.veiculo,
                    'id': obj.pk,
                    'cliente': obj.pedido.cliente.nome_fantasia
                }
                for obj in Carga.objects.order_by('-situacao','data_agenda','modificado').filter(data_agenda__gte=filt_data).filter(pedido__cliente__nome_fantasia=filt2)
            ]
        )
        return context

class CargasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = ('corretora.view_carga')
    
    models = Carga
    paginate_by = 40
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargas.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    def get_context_data(self, **kwargs):
        context = super(CargasView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        context['cartoesvp'] = CartaoVp.objects.order_by('-cartao_base','cartao_numero').filter(cartao_utilizado=False).distinct('cartao_base')
        context['cartao_vp'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'numero': obj.cartao_numero,
                    'cartaobase': obj.get_cartao_base,
                    'cartaobase_name': obj.cartao_base,
                    'disponivel': obj.cartao_utilizado,
                }
                for obj in CartaoVp.objects.order_by('-cartao_base','cartao_numero').filter(cartao_utilizado=False).all()
            ]
        )
        return context

class CargasViewJsonTeste(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = ('corretora.view_carga')
    
    models = Carga
    # paginate_by = 40
    # ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargasJsonTeste.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset)
        return JsonResponse(data, status=200, safe=False) 

class CargasViewJsonTeste2(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = ('corretora.view_carga')
    
    models = Carga
    # paginate_by = 40
    # ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargasJsonTeste2.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas'


class ResumoTabelasAjaxView(LoginRequiredMixin, TemplateView):
    login_url = 'login'    
    template_name = 'tabelas_dashboard_basecorretora.html'
    

    def get_context_data(self, **kwargs):
        context = super(ResumoTabelasAjaxView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.order_by('situacao','cliente','-data','-id')[:100]
        context['chart'] = Pedido.objects.order_by('data','id').all
        context['fornecedores'] = Fornecedor.objects.order_by('nome').all
        context['cargas'] = Carga.objects.order_by('situacao','-data','ordem','chegada','buonny','pedido__cliente')[:100]
        context['clientes'] = Cliente.objects.order_by('-nome').all

        return context


class CargasTabelaTesteView(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    models = Carga
    
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'tabelas_cargas.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

class CargasTabelaPedidosView(LoginRequiredMixin, ListView):
    login_url = 'login'
    models = Pedido
    ordering = ['situacao','cliente','-data','-id'] 
    template_name = 'tabelas_pedidos.html'
    queryset = Pedido.objects.all()
    context_object_name = 'pedidos' 


class CargasmbView(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    models = Carga
    paginate_by = 30
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargasmb.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    def get_context_data(self, **kwargs):
        context = super(CargasmbView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        return context

class CargasViewTerceiros(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    models = Carga
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargasterceiros.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    def get_context_data(self, **kwargs):
        context = super(CargasViewTerceiros, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        return context


class CreateCargasView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_form_add.html'
    success_message = "%(placa)s - %(motorista)s Incluído com Sucesso!!"
    fields = '__all__'
    exclude = ['obs_comissao']
    # success_url = reverse_lazy('corretora')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('cargas')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_age_cargas')
        else:
            return reverse('cargas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["pedidos"] = Pedido.objects.filter(situacao="a").all()
        context['pedidos_json'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'contrato': obj.contrato,
                    'fornecedor': obj.fornecedor.nome,
                    'cidadef': obj.fornecedor.cidade.cidade,
                    'color': obj.cliente.color,
                    'cliente': obj.cliente.nome_fantasia
                    
                }
                for obj in Pedido.objects.filter(situacao="a").all()
            ]
        )
        return context

class CreateageCargasView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = 'login'
    
    permission_required = ('corretora.add_carga')
    model = Carga
    template_name = 'carga_age_form.html'
    success_message = "%(placa)s - %(motorista)s Agendado com sucesso!!"
    fields = ('ordem','tac','chegada','pedido','situacao','data','buonny','transp','placa','motorista','valor_mot',
                'veiculo','data_agenda','obs')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('cargas')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_age_cargas')
        else:
            return reverse('cargas')
    

    def get_context_data(self, **kwargs):
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
        
        context = super().get_context_data(**kwargs)   
        context['dias_semanas_json'] = json.dumps(dias_da_semana())  
        context['query_cargas_json'] = json.dumps(
            [
                {
                    'cliente': obj.pedido.cliente.nome_fantasia,
                    'data_agenda' : obj.data_agenda.strftime("%Y-%m-%d"),
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('data_agenda').filter(data_agenda__gte=dias_da_semana()[0])
            ]
        )
        context['query_cargas_json_carregado'] = json.dumps(
            [
                {
                    'cliente': obj.pedido.cliente.nome_fantasia,
                    'data_agenda' : obj.data_agenda.strftime("%Y-%m-%d"),
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('placa').filter(situacao='Carregado').filter(data_agenda__gte=dias_da_semana()[0]).distinct('placa')
            ]
        )
        context['pedidos_json'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'contrato': obj.contrato,
                    'fornecedor': obj.fornecedor.nome,
                    'cidadef': obj.fornecedor.cidade.cidade,
                    'color': obj.cliente.color,
                    'cliente': obj.cliente.nome_fantasia
                    
                }
                for obj in Pedido.objects.filter(situacao="a").all()
            ]
        )
        context['agenda_json'] = json.dumps(
            [
                {
                    'nome': obj.nome_fantasia,
                    # 'prev_dias': obj.previsao_dias_da_semana_dois(),
                    'dias_descarga': obj.dias_descarga,
                    'veiculos_dia': obj.veiculos_dia,
                    'descarga_sabado': obj.descarga_sabado
                }
                for obj in Cliente.objects.order_by('-nome').all()
            ]
        )
        context['data_sem_json'] = json.dumps(
            [
                {
                    obj.cliente.nome_fantasia : obj.data_semcarga.strftime("%Y-%m-%d")
                    
                }
                for obj in Datasemcarga.objects.order_by('-cliente__nome_fantasia').all()
            ]
        )
        return context

class UpdateCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_form.html'
    success_message = "%(placa)s - %(motorista)s Alterado com Sucesso!!"
    fields = ('ordem','tac','chegada','pedido','situacao','data','buonny','transp','placa','motorista','valor_mot','peso',
                'veiculo','notafiscal','notafiscal2','valornf','data_agenda','renda','inteiro','impureza',
                'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
                'obs')

    success_url = reverse_lazy('cargas')

    def get_context_data(self, **kwargs):
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
        context = super().get_context_data(**kwargs)  
        context['dias_semanas_json'] = json.dumps(dias_da_semana())  
        context['query_cargas_json'] = json.dumps(
            [
                {
                    'cliente': obj.pedido.cliente.nome_fantasia,
                    'data_agenda' : obj.data_agenda.strftime("%Y-%m-%d"),
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('data_agenda').filter(data_agenda__gte=dias_da_semana()[0])
            ]
        )      
        context['query_cargas_json_carregado'] = json.dumps(
            [
                {
                    'cliente': obj.pedido.cliente.nome_fantasia,
                    'data_agenda' : obj.data_agenda.strftime("%Y-%m-%d"),
                    'placa': obj.placa
                }
                for obj in Carga.objects.order_by('placa').filter(situacao='Carregado').filter(data_agenda__gte=dias_da_semana()[0]).distinct('placa')
            ]
        )
        context['pedidos_json'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'contrato': obj.contrato,
                    'fornecedor': obj.fornecedor.nome,
                    'cidadef': obj.fornecedor.cidade.cidade,
                    'color': obj.cliente.color,
                    'cliente': obj.cliente.nome_fantasia
                    
                }
                for obj in Pedido.objects.filter(situacao="a").all()
            ]
        )
        context['agenda_json'] = json.dumps(
            [
                {
                    'nome': obj.nome_fantasia,
                    # 'prev_dias': obj.previsao_dias_da_semana_dois(),
                    'dias_descarga': obj.dias_descarga,
                    'veiculos_dia': obj.veiculos_dia,
                    'descarga_sabado': obj.descarga_sabado
                }
                for obj in Cliente.objects.order_by('-nome').all()
            ]
        )
        context['data_sem_json'] = json.dumps(
            [
                {
                    obj.cliente.nome_fantasia : obj.data_semcarga.strftime("%Y-%m-%d")
                    
                }
                for obj in Datasemcarga.objects.order_by('-cliente__nome_fantasia').all()
            ]
        )
        return context

class UpdateclassCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_class.html'
    success_message = 'Classificação atualizada com sucesso!!'
    # fields = '__all__'
    fields = ('renda','inteiro','impureza',
                'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
                'obs')
    success_url = reverse_lazy('cargas')

class UpdatechegadaCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_chegada_form.html'
    success_message = 'Dados atualizados com sucesso!!'
    # fields = '__all__'
    fields = ('chegada',)
    success_url = reverse_lazy('cargas')

class UpdateAjaxCartaoVpView(LoginRequiredMixin, UpdateView):
    model = CartaoVp
    fields = ('cartao_utilizado',)

    def get(self, request):
        id1 = request.GET.get("id", None)
        cartao1 = request.GET.get("name")
        
        obj = get_object_or_404(CartaoVp, id=id1)
        obj.cartao_utilizado = cartao1
        obj.save()
        obj1 = get_object_or_404(CartaoVp, id=id1)

        user = {"id": obj1.pk, "name": obj1.cartao_utilizado}

        data = {"user": user}
        return JsonResponse(data)

class UpdateAjaxOrdemView(LoginRequiredMixin, UpdateView):
    model = Carga
    fields = ('ordem',)

    def get(self, request):
        id1 = request.GET.get("id", None)
        ordem1 = request.GET.get("name")
        
        obj = get_object_or_404(Carga, id=id1)
        obj.ordem = ordem1
        obj.save()
        obj1 = get_object_or_404(Carga, id=id1)

        user = {"id": obj1.pk, "name": obj1.ordem}

        data = {"user": user}
        return JsonResponse(data)

class UpdateAjaxChegadaView(LoginRequiredMixin, UpdateView):
    model = Carga
    fields = ('chegada',)

    def get(self, request):
        id1 = request.GET.get("id", None)
        chegada1 = request.GET.get("name")
        
        obj = get_object_or_404(Carga, id=id1)
        obj.chegada = chegada1
        print(obj.chegada)
        obj.save()
        obj1 = get_object_or_404(Carga, id=id1)

        user = {"id": obj1.pk, "name": obj1.chegada}

        data = {"user": user}
        return JsonResponse(data)

class UpdateAjaxBuonnyView(LoginRequiredMixin, UpdateView):
    model = Carga
    fields = ('buonny',)

    def get(self, request):
        id1 = request.GET.get("id", None)
        buonny1 = request.GET.get("name")
        
        obj = get_object_or_404(Carga, id=id1)
        obj.buonny = buonny1
        print(obj.buonny)
        obj.save()
        obj1 = get_object_or_404(Carga, id=id1)

        user = {"id": obj1.pk, "buonny": obj1.buonny}

        data = {"user": user}
        return JsonResponse(data)

class UpdateAjaxClassificacaoView(LoginRequiredMixin, UpdateView):
    model = Carga
    fields = ('renda','inteiro','impureza',
                'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
                'obs')

    def get(self, request):
        id1 = request.GET.get("id", None)
        renda1 = request.GET.get("renda")
        inteiro1 = request.GET.get("inteiro")
        impureza1 = request.GET.get("impureza")
        umidade1 = request.GET.get("umidade")
        gessado1 = request.GET.get("gessado")
        bbranca1 = request.GET.get("bbranca")
        amarelo1 = request.GET.get("amarelo")
        manchpic1 = request.GET.get("manchpic")
        vermelhos1 = request.GET.get("vermelhos")
        obs1 = request.GET.get("obs")
        
        obj = get_object_or_404(Carga, id=id1)
        obj.renda = float((renda1.replace(",", "."))) if renda1 else None
        obj.inteiro = float((inteiro1.replace(",", "."))) if inteiro1 else None
        obj.impureza = float((impureza1.replace(",", "."))) if impureza1 else None
        obj.umidade = float((umidade1.replace(",", "."))) if umidade1 else None
        obj.gessado = float((gessado1.replace(",", "."))) if gessado1 else None
        obj.bbranca = float((bbranca1.replace(",", "."))) if bbranca1 else None        
        obj.amarelo = float((amarelo1.replace(",", "."))) if amarelo1 else None        
        obj.manchpic = float((manchpic1.replace(",", "."))) if manchpic1 else None        
        obj.vermelhos = float((vermelhos1.replace(",", "."))) if vermelhos1 else None        
        obj.obs = obs1 

        obj.save()
        
        obj1 = get_object_or_404(Carga, id=id1)
        data = {"id": obj1.pk, "renda": obj1.renda, "inteiro": obj1.inteiro, "impureza": obj1.impureza, "umidade": obj1.umidade, "gessado": obj1.gessado, "bbranca": obj1.bbranca, "amarelo": obj1.amarelo, "manchpic": obj1.manchpic, "vermelhos": obj1.vermelhos, "obs": obj1.obs }

        print(data)
        return JsonResponse(data)

class UpdateAjaxComifreteView(LoginRequiredMixin, UpdateView):
    model = Carga
    fields = ('renda','inteiro','impureza',
                'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
                'obs')

    def get(self, request):
        id1 = request.GET.get("id", None)
        comi_frete_ton = request.GET.get("renda")
        comi_frete_total = request.GET.get("inteiro")
        print(comi_frete_ton)
        print(comi_frete_total)
        
        obj = get_object_or_404(Carga, id=id1)
        obj.comi_frete_ton = float((comi_frete_ton.replace(".", "").replace(",", "."))) if comi_frete_ton else None
        obj.comi_frete_total = float((comi_frete_total.replace(".", "").replace(",", "."))) if comi_frete_total else None
        obj.save()
        
        obj1 = get_object_or_404(Carga, id=id1)
        data = {"id": obj1.pk, "comi_frete_ton": obj1.comi_frete_ton, "comi_frete_total": obj1.comi_frete_total}

        print(data)
        return JsonResponse(data)

class CreateFaturasComiFreteAjaxView(LoginRequiredMixin, UpdateView):
    model = FaturaCargasComiFrete
    fields = ('numero','empresa',
    'data_fatura', 'data_fatura_vencimento', 
    'valor_total_fatura', 'transportadora', 'obs')
    
    def get(self, request):
        ids_cargas = request.GET.getlist("ids_carga[]")
        ids_formt = [int(x) for x in ids_cargas]
        numero_input = request.GET.get("numero")
        empresa_input = int(request.GET.get("empresa"))
        empresa_format = EmpresaCorretora.objects.filter(id=empresa_input)[0]
        transportadora_input = int(request.GET.get("transportadora"))
        transportadora_format = Transportadora.objects.filter(id=transportadora_input)[0]
        datafatura_input = request.GET.get("datafatura")
        datafatura_input = datetime.datetime.strptime(datafatura_input, '%d/%m/%Y')
        datafatura_format = datafatura_input.strftime("%Y-%m-%d")
        
        datavencimentofatura_input = request.GET.get("datavencimentofatura")
        datavencimentofatura_input = datetime.datetime.strptime(datavencimentofatura_input, '%d/%m/%Y')
        datavencimentofatura_format = datavencimentofatura_input.strftime("%Y-%m-%d")
        valorfatura_input = float(request.GET.get("valorfatura").replace(".", "").replace(",", "."))
        obs_input = request.GET.get("obs")
        nova_fatura = FaturaCargasComiFrete.objects.create(
            numero=numero_input,
            empresa=empresa_format,
            data_fatura=datafatura_format,
            data_fatura_vencimento=datavencimentofatura_format,
            transportadora=transportadora_format,
            valor_total_fatura=valorfatura_input,
            obs=obs_input
            )
        id_nova_fatura = nova_fatura.id
        print(f'id da nova fatura {id_nova_fatura}')
        nova_fatura = FaturaCargasComiFrete.objects.filter(id=id_nova_fatura)[0]

        cargas_fatura = Carga.objects.filter(id__in=ids_formt)
        print(cargas_fatura)
        for i in cargas_fatura:
            i.fatura_frete_terceiros = nova_fatura
            i.save()
            print(i.fatura_frete_terceiros)

        data_fatura = FaturaCargasComiFrete.objects.all().filter(id=id_nova_fatura)[0]
        data = { "numero": data_fatura.numero, "valor": data_fatura.valor_total_fatura, "transp" : data_fatura.transportadora.nome }
        print(data)
        return JsonResponse(data, safe=False)




class UpdatecomissCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_comiss.html'
    success_message = 'Comissão atualizada com sucesso!!'
    fields = ('pgcomissao', 'vpcomissaoc', 'vpcomissaof', 'obs_comissao')
    success_url = reverse_lazy('cargas')

class UpdatecomprovdescargaCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = CompDescargaForm
    model = Carga
    template_name = 'carga_comprovante_descarga.html'
    success_message = 'Comprovante salvo com sucesso!!'
    # fields = ('comprovante_descarga', 'data_descarga', 'obs_descarga')
    success_url = reverse_lazy('cargas')


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.id)
        tranps_get_id = self.object.transp.id
        transp = Transportadora.objects.all().filter(id=tranps_get_id)
        print(transp[0].email)
        return super(UpdatecomprovdescargaCargasView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        return super(UpdatecomprovdescargaCargasView, self).post(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        def boas_vindas():
            hora_atual = datetime.datetime.now()
            hora_atual_print = hora_atual.strftime("%H:%M:%S")
            hora = int(hora_atual.strftime("%H"))
            minutos = int(hora_atual.strftime("%M"))
            segundos = int(hora_atual.strftime("%S"))
            if hora > 11:
                return f"Boa tarde,\n"
            else:
                return f"Bom dia,\n"
        self.object         = self.get_object()
        motorista           = self.object.motorista
        placa               = self.object.placa
        notafiscal          = self.object.notafiscal
        nf_format           = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(notafiscal))
        tranps_get_id       = self.object.transp.id
        transp              = Transportadora.objects.all().filter(id=tranps_get_id)
        transpNome          = transp[0].nome
        transpMail          = transp[0].email
        transpContato       = transp[0].contato
        transp_recebe_email = transp[0].recebe_email_comprovante
        if 'comprovante_descarga' in self.request.FILES:
            comprovante_descarga = self.request.FILES['comprovante_descarga']
        data_descarga        = form.cleaned_data['data_descarga']
        obs_descarga         = form.cleaned_data['obs_descarga']
        subject = f"{transpNome.title()} - Comprovante: {placa} - {motorista.title()} - NF: {nf_format}"
        text = f'{boas_vindas()} \n\n{transpContato.title()}\n\n\nSegue comprovante em anexo: {placa} - {motorista.title()} - NF: {nf_format}\n\n\n'
        if obs_descarga:
            text = f'{boas_vindas()} \n\n{transpContato.title()}\n\n\nSegue comprovante em anexo: {placa} - {motorista.title()} - NF: {nf_format}\n\n\nObs.:\t {obs_descarga}\n\n\n'
        email = ['marcelo@gdourado.com.br',transpMail]
        try:
            if 'comprovante_descarga' in self.request.FILES and transp_recebe_email == True:
                mail = EmailMessage(
                    subject=subject,
                    body=text,
                    from_email='contato@gdourado.com.br',
                    to=email,
                    headers={'Reply-To': 'marcelo@gdourado.com.br'}
                )
                mail.attach(comprovante_descarga.name, comprovante_descarga.read(), comprovante_descarga.content_type)
                mail.send()
                messages.success(self.request, f'Comprovante de {placa} - {motorista.title()} Enviado com successo para {transpNome.title()}')
            else:
                print('Salvo somente no DB')
        except Exception as e:
            print(e)
        return super(UpdatecomprovdescargaCargasView, self).form_valid(form, *args, **kwargs)
    

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(UpdatecomprovdescargaCargasView, self).form_invalid(form, *args, **kwargs)

    

class DeleteCargasView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    login_url = 'login'
    
    model = Carga
    success_message = "%(placa)s - %(motorista)s Excluída com Sucesso!!"
    template_name = 'carga_del.html'
    success_url = reverse_lazy('cargas')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)        
        return super(DeleteCargasView, self).delete(request, *args, **kwargs)
    