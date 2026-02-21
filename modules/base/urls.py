from django.urls import path

from . import views

urlpatterns = [
    path('applicant/', views.applicants_index_view, name='base_applicants'),
    path('applicant/create/', views.create_applicant_view, name='base_applicants_create'),
    path('applicant/<str:applicant_id>/get/', views.get_applicant_view, name='base_applicants_query'),
    path('applicant/<str:applicant_id>/edit/', views.edit_applicant_view, name='base_applicants_edit'),
    path('applicant/<str:applicant_id>/delete/', views.delete_applicant_view, name='base_applicants_delete'),
    path('applicant/search/', views.ajax_search_applicant, name='base_applicants_search'),

    path('taker/', views.takers_index_view, name='base_takers'),
    path('taker/create/', views.create_taker_view, name='base_takers_create'),
    path('taker/<str:taker_id>/get/', views.get_taker_view, name='base_takers_query'),
    path('taker/<str:taker_id>/edit/', views.edit_taker_view, name='base_takers_edit'),
    path('taker/<str:taker_id>/delete/', views.delete_taker_view, name='base_takers_delete'),
    path('taker/search/', views.ajax_search_taker, name='base_takers_search'),

    path("persontype/<str:person_type_id>/getdocumenttypes/", views.ajax_documenttypes, name="base_persontype_documenttypes"),
]
