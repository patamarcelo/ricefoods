from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse

from django.db.models import F, FloatField, Sum, Avg, Count
from easy_pdf.views import PDFTemplateResponseMixin

import datetime
# Graficos
import json
# Graficos

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin
from django.views.generic.list import MultipleObjectMixin



from .models import *

from .filters import CargasFilter
from django_filters.views import FilterView
from . import filters

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render





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
        context['pesototal'] = filter.qs.filter(situacao='Carregado').filter(peso__gt=0).values('peso').aggregate(Sum('peso'))
        context['agendatotal'] = filter.qs.filter(situacao='Agendado').filter(peso=0).values('veiculo').aggregate(Sum('veiculo'))            
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
        context['pedidos'] = Pedido.objects.order_by('situacao','cliente','-data','-id').all()[0:100]
        context['chart'] = Pedido.objects.order_by('data','id').all
        context['fornecedores'] = Fornecedor.objects.order_by('nome').all
        context['cargas'] = Carga.objects.order_by('situacao','-data','ordem','chegada','buonny','pedido__cliente').all()[0:100]
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
               'variedade','produto','tipo','quantidade_pedido','obs' )
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
        return queryset.filter(data_agenda__gte=filt1).filter(data_agenda__lte=filt2)

    def get_context_data(self, **kwargs):
        context = super(CargasAgendamentoView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        return context

class CargasView(LoginRequiredMixin, ListView):
    login_url = 'login'
    
    models = Carga
    paginate_by = 30
    ordering = ['situacao','-data','ordem','chegada','buonny','pedido__cliente'] 
    template_name = 'cargas.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

    def get_context_data(self, **kwargs):
        context = super(CargasView, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.order_by('-nome').all
        return context

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
        return context

class CreateageCargasView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    
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
        context = super().get_context_data(**kwargs)        
        context["pedidos"] = Pedido.objects.filter(situacao="a").all()
        context['clientes'] = Cliente.objects.order_by('-nome').all
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
        context = super().get_context_data(**kwargs)        
        context["pedidos"] = Pedido.objects.filter(situacao="a").all()
        context['clientes'] = Cliente.objects.order_by('-nome').all
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



class UpdatecomissCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    
    model = Carga
    template_name = 'carga_comiss.html'
    success_message = 'Comissão atualizada com sucesso!!'
    fields = ('pgcomissao', 'vpcomissaoc', 'vpcomissaof')
    success_url = reverse_lazy('cargas')

     


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
    