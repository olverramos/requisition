from django.urls import path

from . import views

urlpatterns = [
    path('requests/', views.requests_index_view, name='parameters_requests'),
    path('requests/create/', views.create_request_view, name='parameters_requests_create'),
    path('requests/<str:request_id>/get/', views.get_request_view, name='parameters_requests_query'),
    path('requests/<str:request_id>/delete/', views.delete_request_view, name='parameters_requests_delete'),
]
