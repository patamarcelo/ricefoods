"""ricef URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from django.conf.urls.static import static
from django.conf import settings

from corretora.views import *
from corretora import views 

urlpatterns = [
    path('painel/', admin.site.urls),
    path('', include('core.urls')),
    path('contas/', include('django.contrib.auth.urls')),
    path('sistema/', TemplateView.as_view(template_name='index2.html'), name='index2'),

    path('corretora/', BaseView.as_view(), name='corretora'), 
    path('corretora/dashboard', BasetwoView.as_view(), name='dashboard'), 
    

    path('corretora/pedidos/', PedidosView.as_view(), name='pedidos'), 
    path('corretora/pedidos/add', CreatePedidosView.as_view(), name='add_pedidos'), 
    path('corretora/pedidos/<int:pk>/update', UpdatePedidosView.as_view(), name='upd_pedidos'), 
    path('corretora/pedidos/<int:pk>/delete', DeletePedidosView.as_view(), name='del_pedidos'),

    path('corretora/fornecedores/', FornecedoresView.as_view(), name='fornecedores'), 
    path('corretora/fornecedores/add', CreateFornecedoresView.as_view(), name='add_fornecedor'),
    path('corretora/fornecedores/<int:pk>/update', UpdateFornecedoresView.as_view(), name='upd_fornecedores'), 
    path('corretora/fornecedores/<int:pk>/delete', DeleteFornecedoresView.as_view(), name='del_fornecedores'),

    path('corretora/cargas/', CargasView.as_view(), name='cargas'), 
    
    path('corretora/tabelacargas/', CargasTabelaTesteView.as_view(), name='tabelacargas'), 
    path('corretora/tabelapedidos/', CargasTabelaPedidosView.as_view(), name='tabelapedidos'), 
    path('corretora/tabeladash/', ResumoTabelasAjaxView.as_view(), name='tabeladashboarbase'), 
    
    path('corretora/cargasmb/', CargasmbView.as_view(), name='cargasmb'), 
    path('corretora/cargasterceiros/', CargasViewTerceiros.as_view(), name='cargasterceiros'), 
    path('corretora/agendamento', CargasAgendamentoView.as_view(), name='agendamento'), 
    path('corretora/agendamentoTeste', CargasAgendamentoViewTeste.as_view(), name='agendamentoTeste'), 
    path('corretora/cf', CargasFiltradasView.as_view(), name='cargasfiltro'), 
    path('corretora/cfcomifrete', CargasFiltradasComissaoFreteView.as_view(), name='cargasfiltro_comifrete'), 
    path('corretora/cargas/add', CreateCargasView.as_view(), name='add_cargas'),
    path('corretora/cargas/add/age', CreateageCargasView.as_view(), name='add_age_cargas'),
    path('corretora/cargas/<int:pk>/update', UpdateCargasView.as_view(), name='upd_cargas'), 
    path('corretora/cargas/<int:pk>/detail', DetailCargasView.as_view(), name='detail_cargas'), 
    path('corretora/cargas/<int:pk>/comissao', ComissCargasView.as_view(), name='detail_cargas_comiss'), 
    path('corretora/cargas/<int:pk>/update/class', UpdateclassCargasView.as_view(), name='upd_class'), 
    path('corretora/cargas/<int:pk>/update/comiss', UpdatecomissCargasView.as_view(), name='upd_comiss'), 
    path('corretora/cargas/<int:pk>/update/chegada', UpdatechegadaCargasView.as_view(), name='upd_chegada'), 
    path('corretora/cargas/<int:pk>/delete', DeleteCargasView.as_view(), name='del_cargas'),

    path('corretora/cargas/update', UpdateAjaxOrdemView.as_view(), name="cargas_ajax_update"),
    path('corretora/cargas/updatechegada', UpdateAjaxChegadaView.as_view(), name="cargas_ajax_update_chegada"),
    path('corretora/cargas/updatebuonny', UpdateAjaxBuonnyView.as_view(), name="cargas_ajax_update_buonny"),
    path('corretora/cargas/updateclassificacao', UpdateAjaxClassificacaoView.as_view(), name="cargas_ajax_update_classificacao"),
    path('corretora/cargas/updatecartaovp', UpdateAjaxCartaoVpView.as_view(), name="cargas_ajax_update_cartaovp"),
    path('corretora/cargas/updatecomifrete', UpdateAjaxComifreteView.as_view(), name="cargas_ajax_update_comifrete"),
    path('corretora/cargas/<int:pk>/updatecompdescarga', UpdatecomprovdescargaCargasView.as_view(), name="update_comprovante_descarga"),
    
    path('corretora/cargas/carjasJsonTeste', CargasViewJsonTeste.as_view(), name="cargas_json_teste"),
    path('corretora/cargas/carjasJsonTeste2', CargasViewJsonTeste2.as_view(), name="cargas_json_teste_ad"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


admin.site.site_header = 'Corretora de Cereais'
admin.site.site_title = 'Corretora de Cereais'
admin.site.index_title = 'Corretora | Painel de Controle'
