from django.urls import path

from . import views

urlpatterns = [
    path('requests/', views.requests_index_view, name='operative_requests'),
    path('requests/search/', views.requests_search_view, name='operative_requests_search'),
    path('requests/create/', views.create_request_view, name='operative_requests_create'),
    path('requests/<str:request_id>/get/', views.get_request_view, name='operative_requests_query'),
    path('requests/<str:request_id>/delete/', views.delete_request_view, name='operative_requests_delete'),
]
