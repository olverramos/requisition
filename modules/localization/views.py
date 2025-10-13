from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .models import Country, State, City
from django.conf import settings


class StatesAjax(View):

    def get(self, request, *args, **kwargs):
        country_id = settings.COUNTRY
        if 'country' in request.GET and request.GET['country']:
            country_id = request.GET['country']
        
        country = Country.objects.get(pk=country_id)
            
        state_list = State.objects.filter(country=country)
        response_data = [ 
            { 
                'id': str(state.id),
                'name': state.name
            } for state in state_list
        ]

        return JsonResponse(data=response_data, safe=False)


class CitiesAjax(View):

    def get(self, request, *args, **kwargs):
        country_id = settings.COUNTRY
        if 'country' in request.GET and request.GET['country']:
            country_id = request.GET['country']

        state = None
        if 'state' in request.GET and request.GET['state']:
            state_id = request.GET['state']
            state = State.objects.get(pk=state_id)

        country = Country.objects.get(pk=country_id)
            
        city_list = City.objects.filter(country=country)
        if state is not None:
            city_list = city_list.filter(state=state)

        response_data = [ 
            { 
                'id': str(city.id),
                'name': city.name
            } for city in city_list
        ]

        return JsonResponse(data=response_data, safe=False)
