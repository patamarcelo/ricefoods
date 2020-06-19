from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse

import datetime
# Graficos
import json
# Graficos

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin



from .models import *



class BaseView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'index2'
    template_name = 'basecorretora.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.order_by('situacao','cliente','-data','-contrato').all
        context['chart'] = Pedido.objects.order_by('data').all
        context['fornecedores'] = Fornecedor.objects.order_by('nome').all
        context['cargas'] = Carga.objects.order_by('situacao','-data','ordem','buonny','pedido_id').all
        
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=6)
        context['carga_ok_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        context['carga_rus_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_rus_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='Ruston').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_ok_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Carregado').values('peso').aggregate(Sum('peso'))
        context['carga_cda_sem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="False").values('veiculo').aggregate(Sum('veiculo'))
        context['carga_cda_sem_ordem'] = Carga.objects.filter(data__gte=monday).filter(data__lte=sunday).filter(pedido__cliente__nome='CDA').filter(situacao='Agendado').filter(ordem="True").values('veiculo').aggregate(Sum('veiculo'))
        return context
    


class PedidosView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'index2'
    models = Pedido
    paginate_by = 23
    ordering = ['situacao', 'cliente','-data','-contrato']
    template_name = 'pedido.html'
    queryset = Pedido.objects.all()
    context_object_name = 'pedidos'


class CreatePedidosView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'index2'
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
    redirect_field_name = 'index2'
    model = Pedido
    template_name = 'pedido_form.html'
    success_message = 'Pedido atualizado com sucesso!!'
    # fields = '__all__'
    fields = ('situacao','data','fornecedor','cliente','preco_produto','preco_frete',
                'comissaoc','comissaof','prazopgto','modalidadepgto',
               'renda', 'inteiro', 'impureza', 'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
               'variedade','produto','tipo','quantidade_pedido','obs' )
    success_url = reverse_lazy('pedidos')

class DeletePedidosView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'index2'
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
    redirect_field_name = 'index2'
    models = Fornecedor
    paginate_by = 23
    ordering = ['nome']
    template_name = 'fornecedores.html'
    queryset = Fornecedor.objects.all()
    context_object_name = 'fornecedores'

class CreateFornecedoresView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'index2'
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
    redirect_field_name = 'index2'
    model = Fornecedor
    template_name = 'fornecedor_form.html'
    success_message = 'Fornecedor atualizado com sucesso!!'
    fields = '__all__'
    success_url = reverse_lazy('fornecedores')

class DeleteFornecedoresView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'index2'
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
        return context


class CargasView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'index2'
    models = Carga
    paginate_by = 23
    ordering = ['situacao','-data','ordem','buonny','pedido_id'] 
    template_name = 'cargas.html'
    queryset = Carga.objects.all()
    context_object_name = 'cargas' 

class CreateCargasView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'index2'
    model = Carga
    template_name = 'carga_form_add.html'
    success_message = "%(placa)s - %(motorista)s inseridos com sucesso!!"
    fields = '__all__'
    # success_url = reverse_lazy('corretora')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('cargas')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_age_cargas')
        else:
            return reverse('cargas')

class CreateageCargasView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'index2'
    model = Carga
    template_name = 'carga_age_form.html'
    success_message = "%(placa)s - %(motorista)s agendado com sucesso!!"
    fields = ('ordem','tac','pedido','situacao','data','buonny','transp','placa','motorista','valor_mot',
                'veiculo','obs')

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse('cargas')
        elif self.request.POST.get('save_and_continue'):
            return reverse('add_age_cargas')
        else:
            return reverse('cargas')

class UpdateCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'index2'
    model = Carga
    template_name = 'carga_form.html'
    success_message = 'Dados atualizados com sucesso!!'
    fields = '__all__'
    # fields = ('ordem','tac','situacao','data','buonny','transp','placa','motorista','valor_mot','peso',
    #             'veiculo','notafiscal','notafiscal2','valornf','renda','inteiro','impureza',
    #             'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
    #             'obs')
    success_url = reverse_lazy('cargas')

class UpdateclassCargasView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'index2'
    model = Carga
    template_name = 'carga_class.html'
    success_message = 'Dados atualizados com sucesso!!'
    # fields = '__all__'
    fields = ('renda','inteiro','impureza',
                'umidade','gessado','bbranca','amarelo','manchpic','vermelhos',
                'obs')
    success_url = reverse_lazy('cargas')

class DeleteCargasView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'index2'
    model = Carga
    success_message = "Carga excluída com sucesso!!"
    template_name = 'carga_del.html'
    success_url = reverse_lazy('cargas')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteCargasView, self).delete(request, *args, **kwargs)
    