from django.urls import path

from . import views

urlpatterns = [
    path('states/', views.StatesAjax.as_view(), name='localization_states'),
    path('cities/', views.CitiesAjax.as_view(), name='localization_cities'),
]
