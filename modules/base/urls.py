from django.urls import path

from . import views

urlpatterns = [
    path('applicant/', views.applicants_index_view, name='base_applicants'),
    path('applicant/create/', views.create_applicant_view, name='base_applicants_create'),
    path('applicant/<str:applicant_id>/get/', views.get_applicant_view, name='base_applicants_query'),
    path('applicant/<str:applicant_id>/edit/', views.edit_applicant_view, name='base_applicants_edit'),
    path('applicant/<str:applicant_id>/delete/', views.delete_applicant_view, name='base_applicants_delete'),

    path('takers/', views.takers_index_view, name='base_takers'),
    path('takers/create/', views.create_taker_view, name='base_takers_create'),
    path('takers/<str:taker_id>/get/', views.get_taker_view, name='base_takers_query'),
    path('takers/<str:taker_id>/edit/', views.edit_taker_view, name='base_takers_edit'),
    path('takers/<str:taker_id>/delete/', views.delete_taker_view, name='base_takers_delete'),
]
