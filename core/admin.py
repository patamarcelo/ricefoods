from django.contrib import admin

from .models import Servicos, Sobre, Sobretopico, Subservicos, Projetos, Subprojetos, Inicial


@admin.register(Servicos)
class ServicosAdmin(admin.ModelAdmin):
    list_display = ('servico','descricao','item1','item2','imagem','modificado')

@admin.register(Inicial)
class InicialAdmin(admin.ModelAdmin):
    list_display = ('inicio','descricao','palavras','modificado')


@admin.register(Sobre)
class SobreAdmin(admin.ModelAdmin):
    list_display = ('titulo','texto','pessoa','imagem','modificado')

@admin.register(Sobretopico)
class SobretopicoAdmin(admin.ModelAdmin):
    list_display = ('sobretopico', 'descricao','modificado','icone')

@admin.register(Subservicos)
class SubservicosAdmin(admin.ModelAdmin):
    list_display = ('subservico','topico1','descricao1','topico2','descricao2','topico3','descricao3','modificado')

@admin.register(Projetos)
class ProjetosAdmin(admin.ModelAdmin):
    list_display = ('titulo','subtitulo','descricao','descricao2','area','area2','area3','area4','link','imagem','modificado')

@admin.register(Subprojetos)
class SubprojetosAdmin(admin.ModelAdmin):
    list_display = ('titulo','descricao','topico1','topico2','imagem','modificado')


