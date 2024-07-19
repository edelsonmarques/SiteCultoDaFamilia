from django.urls import path
from . import views, htmx_views

urlpatterns = [
    path('', views.arearestritafamilia, name='arearestritafamilia'),
]

htmx_urlpatterns = [
    path('insert_list/', htmx_views.insert_list, name='insert_list'),
    path('exclude_post/<str:id_post>', htmx_views.exclude_post, name='exclude_post'),
    path('save_post/<str:id_post>', htmx_views.save_post, name='save_post'),
    path('edit_post/<str:id_post>', htmx_views.edit_post, name='edit_post'),
    path('save_list_post/<str:id_post>', htmx_views.save_list_post, name='save_list_post'),
    path('edit_list_post/<str:id_post>', htmx_views.edit_list_post, name='edit_list_post'),
    path('none_page/', htmx_views.none_page, name='none_page'),
]

urlpatterns += htmx_urlpatterns
