from django.db import models
import json

module_folder = 'modules/localization'


class Country(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    capital_code = models.CharField(max_length=2, null=True, blank=True, verbose_name='Código de la Capital')
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/countries.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            country = Country.objects.get(pk=data["id"])
                        except Country.DoesNotExist:
                            country = Country()
                            country.id = data['id']
                            country.name = data['name']
                            if 'capital_code' in data.keys():
                                country.capital_code = data['capital_code']
                            country.save()

                            print (f'País {country} creado')

        except FileNotFoundError:
            pass

    class Meta:
        db_table = 'localization_countries'
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['name']

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="País")
    code = models.CharField(max_length=2, verbose_name='Código')
    short = models.CharField(max_length=2, null=True, blank=True, verbose_name='Nombre Corto')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    capital_code = models.CharField(max_length=2, null=True, blank=True, verbose_name='Código Capital')
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/states.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    country = None
                    if 'country_id' in data.keys():
                        try:
                            country = Country.objects.get(pk=data["country_id"])
                        except Country.DoesNotExist:
                            country = None
                    if country is not None:
                        if 'code' in data.keys() and 'name' in data.keys():
                            try:
                                state = State.objects.get(country=country, code=data['code'])
                            except State.DoesNotExist:
                                state = None
                        if state is None:  
                            state = State()
                            state.country = country
                            state.code = data['code']
                            state.name = data['name']
                            if 'short' in data.keys():
                                state.short = data['short']
                            if 'capital_code' in data.keys():
                                state.capital_code = data['capital_code']
                            state.save()

                            print (f'Departamento {state} creado')
        except FileNotFoundError:
            pass

    class Meta:
        db_table = 'localization_states'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['country', 'name']
        unique_together = ['country', 'code']


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="País")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="Departamento", null=True, blank=True)
    code = models.CharField(max_length=2, verbose_name='Código')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/cities.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    country = None
                    state = None
                    if 'country_id' in data.keys():
                        try:
                            country = Country.objects.get(pk=data["country_id"])
                        except Country.DoesNotExist:
                            country = None
                    if country is not None:
                        if 'state_code' in data.keys():
                            try:
                                state = State.objects.get(country=country, code=data['state_code'])
                            except State.DoesNotExist:
                                state = None

                        if 'code' in data.keys() and 'name' in data.keys():
                            try:
                                city = City.objects.get(country=country, code=data['code'])
                            except City.DoesNotExist:
                                city = None
                        if city is None:  
                            city = City()
                            city.country = country
                            city.state = state
                            city.code = data['code']
                            city.name = data['name']
                            city.save()
                            
                            print (f'Ciudad {city} creado')
        except FileNotFoundError:
            pass

    class Meta:
        db_table = 'localization_cities'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['country', 'state', 'code']
        unique_together = ['country', 'code']
