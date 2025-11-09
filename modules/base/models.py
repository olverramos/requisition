from django_mongoengine import Document, fields
import datetime
import json

module_folder = 'modules/base'


class PersonType(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(verbose_name='Nombre')

    meta = {
        'collection': 'base_persontypes',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/persontypes.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            person_type = PersonType.objects.get(id=data["id"])
                        except PersonType.DoesNotExist:
                            person_type = PersonType()
                            person_type.id = data['id']
                            person_type.name = data['name']
                            person_type.save()

                            print (f'Tipo de Persona {person_type} creada')

        except FileNotFoundError:
            pass


class DocumentType(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(verbose_name='Nombre')
    person_type = fields.ReferenceField(PersonType, verbose_name="Tipo de Persona")

    meta = {
        'collection': 'base_documenttypes',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/documenttypes.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    person_type = None
                    if 'person_type' in data.keys():
                        try:
                            person_type = PersonType.objects.get(id=data["person_type"])
                        except PersonType.DoesNotExist:
                            person_type = None

                    if person_type is not None and 'id' in data.keys() and 'name' in data.keys():
                        try:
                            document_type = DocumentType.objects.get(id=data["id"])
                        except DocumentType.DoesNotExist:
                            document_type = DocumentType()
                            document_type.person_type = person_type
                            document_type.id = data['id']
                            document_type.name = data['name']
                            document_type.save()

                            print (f'Tipo de Documento {document_type} creado')

        except FileNotFoundError:
            pass


class Applicant(Document):
    identification = fields.StringField(verbose_name='Identificacíon', unique=True)
    name = fields.StringField(verbose_name='Nombre')
    email = fields.EmailField(verbose_name='Email', unique=True)
    phone_number = fields.StringField(verbose_name='Teléfono', null=True, blank=True)
    state = fields.ReferenceField('localization.State', verbose_name="Departamento", null=True, blank=True)
    city = fields.ReferenceField('localization.City', verbose_name="Ciudad", null=True, blank=True)
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'base_applicants',
        'ordering': ['email'],
        'indexes': [
            ('email',), 
        ]
    }
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        from modules.localization.models import State, City
        try:
            with open(f'{module_folder}/scripts/data/applicants.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    state = None
                    if 'state_code' in data.keys():
                        try:
                            state = State.objects.get(code=data["state_code"])
                        except State.DoesNotExist:
                            state = None
                    city = None
                    if 'city_code' in data.keys():
                        try:
                            city = City.objects.get(code=data["city_code"])
                            if city.state is not None:
                                state = city.state
                        except City.DoesNotExist:
                            city = None

                    if 'identification' in data.keys() and 'name' in data.keys() and 'email' in data.keys():
                        try:
                            applicant = Applicant.objects.get(identification=data["identification"])
                        except Applicant.DoesNotExist:
                            applicant = Applicant()
                            applicant.identification = data['identification']
                            applicant.name = data['name']
                            applicant.email = data['email']
                            applicant.phone_number = data['phone_number']
                            applicant.state = state
                            applicant.city = city
                            applicant.created_at = datetime.datetime.now()
                            applicant.save()

                            print (f'Solicitante {applicant} creado')
        except FileNotFoundError:
            pass


class Taker(Document):
    person_type = fields.ReferenceField(PersonType, verbose_name="Tipo de Persona")
    document_type = fields.ReferenceField(DocumentType, verbose_name="Tipo de Documento")
    identification = fields.StringField(verbose_name='Identificacíon', unique=True)
    name = fields.StringField(verbose_name='Nombre')
    email = fields.EmailField(verbose_name='Email', null=True, blank=True)
    phone_number = fields.StringField(verbose_name='Teléfono', null=True, blank=True)
    contact_name = fields.StringField(verbose_name='Nombre Contacto', null=True, blank=True)
    address = fields.StringField(verbose_name='Dirección', null=True, blank=True)
    state = fields.ReferenceField('localization.State', verbose_name="Departamento", null=True, blank=True)
    city = fields.ReferenceField('localization.City', verbose_name="Ciudad", null=True, blank=True)
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'base_takers',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        from modules.localization.models import State, City
        try:
            with open(f'{module_folder}/scripts/data/takers.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    person_type = None
                    if 'person_type' in data.keys():
                        try:
                            person_type = PersonType.objects.get(id=data["person_type"])
                        except PersonType.DoesNotExist:
                            person_type = None

                    document_type = None
                    if 'document_type' in data.keys():
                        try:
                            document_type = DocumentType.objects.get(id=data["document_type"])
                            if person_type is not None and document_type.person_type.id != person_type.id:
                                document_type = None
                        except DocumentType.DoesNotExist:
                            document_type = None
                    
                    state = None
                    if 'state_code' in data.keys():
                        try:
                            state = State.objects.get(code=data["state_code"])
                        except State.DoesNotExist:
                            state = None
                            
                    city = None
                    if 'city_code' in data.keys():
                        try:
                            city = City.objects.get(code=data["city_code"])
                            if city.state is not None:
                                state = city.state
                        except City.DoesNotExist:
                            city = None

                    if person_type is not None and document_type is not None and \
                        'identification' in data.keys() and 'name' in data.keys() \
                        and 'email' in data.keys():
                        try:
                            taker = Taker.objects.get(identification=data["identification"])
                        except Taker.DoesNotExist:
                            taker = Taker()
                            taker.person_type = person_type
                            taker.document_type = document_type
                            taker.identification = data['identification']
                            taker.name = data['name']
                            taker.email = data['email']
                            taker.phone_number = data['phone_number']
                            taker.contact_name = data['contact_name']
                            taker.address = data['address']
                            taker.state = state
                            taker.city = city
                            taker.created_at = datetime.datetime.now()
                            taker.save()

                            print (f'Tomador {taker} creado')
        except FileNotFoundError:
            pass
