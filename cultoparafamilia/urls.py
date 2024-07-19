from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cultoparafamilia, name='cultoparafamilia'),
    path('area_restrita/', include('cultoparafamilia.arearestritafamilia.urls')),
    path('sorteio_familia/', include('cultoparafamilia.sorteio_familia.urls')),
    path('login/', views.login_area_restrita, name='login_area_restrita'),
    path('cadastrar_user/', views.cadastrar_user, name='cadastrar_user'),
    path('logout/', views.logout_area_restrita, name='logout_area_restrita'),
]