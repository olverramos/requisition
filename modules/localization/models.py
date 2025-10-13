from django_mongoengine import Document, fields
import mongoengine
import json

module_folder = 'modules/localization'


class Country(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    capital_code = fields.StringField(max_length=100, verbose_name='Nombre', null=True, blank=True)

    meta = {
        'collection': 'localization_country',
        'ordering': ['name'],
    }
    
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


class State(Document):
    country = fields.ReferenceField(Country, verbose_name="País", reverse_delete_rule=mongoengine.DENY)
    code = fields.StringField(verbose_name='Código', max_length=10)
    short = fields.StringField(verbose_name='Nombre Corto', null=-True, blank=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    capital_code = fields.StringField(max_length=100, verbose_name='Nombre', null=True, blank=True)
    
    meta = {
        'collection': 'localization_state',
        'ordering': ['country', 'name'],
        'indexes': [
            {
                'fields': ['country', 'code'],
                'unique': True,
            }
        ]
    }
    
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


class City(Document):
    country = fields.ReferenceField(Country, verbose_name="País", reverse_delete_rule=mongoengine.DENY)
    state = fields.ReferenceField(State, verbose_name="Departamento", null=True, blank=True, reverse_delete_rule=mongoengine.NULLIFY)
    code = fields.StringField(verbose_name='Código', max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    
    meta = {
        'collection': 'localization_city',
        'ordering': ['country', 'state', 'code'],
        'indexes': [
            {
                'fields': ['country', 'code'],
                'unique': True,
            },
            {
                'fields': ['country', 'state', 'name'],
            }
        ]
    }
    
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
