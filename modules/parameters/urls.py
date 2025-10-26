from django.urls import path

from . import views

urlpatterns = [
    path('ramo/', views.ramos_index_view, name='parameters_ramos'),
    path('ramo/create/', views.create_ramo_view, name='parameters_ramos_create'),
    path('ramo/<str:ramo_id>/get/', views.get_ramo_view, name='parameters_ramos_query'),
    path('ramo/<str:ramo_id>/edit/', views.edit_ramo_view, name='parameters_ramos_edit'),
    path('ramo/<str:ramo_id>/delete/', views.delete_ramo_view, name='parameters_ramos_delete'),
    path("ramo/<str:ramo_id>/fields/", views.ajax_getfields, name="parameters_ramos_getfields"),
    path("ramo/<str:ramo_id>/documents/", views.ajax_getdocuments, name="parameters_ramos_getdocuments"),

]
