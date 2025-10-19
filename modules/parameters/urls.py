from django.urls import path

from . import views

urlpatterns = [
    path('ramos/', views.ramos_index_view, name='parameters_ramos'),
    path('ramos/create/', views.create_ramo_view, name='parameters_ramos_create'),
    path('ramos/<str:ramo_id>/get/', views.get_ramo_view, name='parameters_ramos_query'),
    path('ramos/<str:ramo_id>/edit/', views.edit_ramo_view, name='parameters_ramos_edit'),
    path('ramos/<str:ramo_id>/delete/', views.delete_ramo_view, name='parameters_ramos_delete'),
]
