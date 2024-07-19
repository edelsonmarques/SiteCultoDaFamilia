from django.urls import path
from . import views, htmx_views

urlpatterns = [
    path('', views.configuracoes_sorteio, name='configuracoes_sorteio'),
]

htmx_urlpatterns = [
    path('config_list/', htmx_views.config_list, name='config_list'),
    path('habilitar_evento/', htmx_views.habilitar_evento, name='habilitar_evento'),
    path('carregar_evento/', htmx_views.carregar_evento, name='carregar_evento'),
    path('selecao_mae_pai/', htmx_views.selecao_mae_pai, name='selecao_mae_pai'),
    path('selecao_filhos_pais/', htmx_views.selecao_filhos_pais, name='selecao_filhos_pais'),
    path('set_sorteios/', htmx_views.set_sorteios, name='set_sorteios'),
    path('set_dinamica_seminario/', htmx_views.set_dinamica_seminario, name='set_dinamica_seminario'),
    path('habilitar_ensaio/', htmx_views.habilitar_ensaio, name='habilitar_ensaio'),
    path('desabilitar_congregacao/', htmx_views.desabilitar_congregacao, name='desabilitar_congregacao'),
    path('historico/', htmx_views.historico, name='historico'),
    
]

urlpatterns += htmx_urlpatterns