from django.urls import path, include
from . import views, htmx_views

urlpatterns = [
    path('', views.sorteio_familia, name='sorteio_familia'),
    path('configuracoes_sorteio/', include('cultoparafamilia.sorteio_familia.configuracoes_sorteio.urls')),
]

htmx_urlpatterns = [
    path('reset_view/', htmx_views.reset_view, name='reset_view'),
    path('sort_geral/', htmx_views.sort_geral, name='sort_geral'),
    path('sort_menor/', htmx_views.sort_menor, name='sort_menor'),
    path('sort_niverCasamento/', htmx_views.sort_niverCasamento, name='sort_niverCasamento'),
    path('sort_visitante/', htmx_views.sort_visitante, name='sort_visitante'),
    path('sort_dinamica/', htmx_views.sort_dinamica, name='sort_dinamica'),
    path('sort_alameda/', htmx_views.sort_alameda, name='sort_alameda'),
    path('sort_jdcopacabana/', htmx_views.sort_jdcopacabana, name='sort_jdcopacabana'),
    path('sort_jdcopacabana2/', htmx_views.sort_jdcopacabana2, name='sort_jdcopacabana2'),
    path('sort_novadivineia/', htmx_views.sort_novadivineia, name='sort_novadivineia'),
    path('sort_novadivineia2/', htmx_views.sort_novadivineia2, name='sort_novadivineia2'),
    path('sort_piedade/', htmx_views.sort_piedade, name='sort_piedade'),
    path('sort_veneza4/', htmx_views.sort_veneza4, name='sort_veneza4'),
    path('sort_ensaio/', htmx_views.sort_ensaio, name='sort_ensaio'),
    path('sort_dinamica_ensaio/', htmx_views.sort_dinamica_ensaio, name='sort_dinamica_ensaio'),
    path('sort_dinamica_mae_pai/', htmx_views.sort_dinamica_mae_pai, name='sort_dinamica_mae_pai'),
    path('sort_dinamica_filhos_pais/', htmx_views.sort_dinamica_filhos_pais, name='sort_dinamica_filhos_pais'),
]

urlpatterns += htmx_urlpatterns