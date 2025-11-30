from django.urls import path

from . import views

urlpatterns = [
    path('requests/', views.requests_index_view, name='operative_requests'),
    path('requests/applicant_search/', views.requests_applicant_search_view, name='operative_requests_applicant_search'),
    path('requests/taker_search/', views.requests_taker_search_view, name='operative_requests_taker_search'),
    path('requests/create/', views.create_request_view, name='operative_requests_create'),
    path('requests/<str:operative_request_id>/query/', views.query_request_view, name='operative_requests_query'),
    path('requests/<str:operative_request_id>/paymentregister/', views.payment_register_request_view, name='operative_requests_payment_register'),
    path('requests/<str:operative_request_id>/attachmentdocuments/', views.attachment_documents_request_view, name='operative_requests_attachment_documents'),
    path('requests/<str:operative_request_id>/documents/', views.documents_request_view, name='operative_requests_documents'),
    path('requests/<str:operative_request_id>/documents/create/', views.create_document_request_view, name='operative_requests_documents_create'),
    path('requests/<str:operative_request_id>/documents/<str:document_id>/delete/', views.delete_document_request_view, name='operative_requests_documents_delete'),
    path('requests/documents/<str:document_id>/get/', views.get_document_request_view, name='operative_requests_documents_get'),
    path('requests/<str:operative_request_id>/assign/', views.assign_request_view, name='operative_requests_assign'),
    path('requests/<str:operative_request_id>/loaddocuments/', views.load_documents_request_view, name='operative_requests_load_documents'),
    path('requests/<str:operative_request_id>/validate/', views.validate_request_view, name='operative_requests_validate'),
    path('requests/<str:operative_request_id>/edit/', views.edit_request_view, name='operative_requests_edit'),
    path('requests/<str:operative_request_id>/get/', views.get_request_view, name='operative_requests_get'),
    path('requests/<str:operative_request_id>/delete/', views.delete_request_view, name='operative_requests_delete'),
]
