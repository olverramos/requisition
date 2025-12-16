from django.urls import path

from . import views

urlpatterns = [
    path('documentclass/', views.documentclass_index_view, name='parameters_documentclass'),
    path('documentclass/create/', views.create_documentclass_view, name='parameters_documentclass_create'),
    path('documentclass/<str:document_class_id>/get/', views.get_documentclass_view, name='parameters_documentclass_query'),
    path('documentclass/<str:document_class_id>/edit/', views.edit_documentclass_view, name='parameters_documentclass_edit'),
    path('documentclass/<str:document_class_id>/delete/', views.delete_documentclass_view, name='parameters_documentclass_delete'),

    path('ramo/', views.ramos_index_view, name='parameters_ramos'),
    path('ramo/create/', views.create_ramo_view, name='parameters_ramos_create'),
    path('ramo/<str:ramo_id>/get/', views.get_ramo_view, name='parameters_ramos_query'),
    path('ramo/<str:ramo_id>/edit/', views.edit_ramo_view, name='parameters_ramos_edit'),
    path('ramo/<str:ramo_id>/delete/', views.delete_ramo_view, name='parameters_ramos_delete'),
    path("ramo/<str:ramo_id>/fields/", views.ajax_getfields, name="parameters_ramos_getfields"),
    path("ramo/<str:ramo_id>/documents/", views.ajax_getdocuments, name="parameters_ramos_getdocuments"),

    path('field/', views.ramo_field_index_view, name='parameters_ramo_field'),
    path('field/create/', views.create_field_view, name='parameters_field_create'),
    path('field/<str:field_id>/get/', views.get_field_view, name='parameters_field_query'),
    path('field/<str:field_id>/edit/', views.edit_field_view, name='parameters_field_edit'),
    path('field/<str:field_id>/delete/', views.delete_field_view, name='parameters_field_delete'),

]
