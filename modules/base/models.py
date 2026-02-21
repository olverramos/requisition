from django.db import models
import datetime
import json

module_folder = 'modules/base'


class PersonType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=10)
    name = models.CharField(verbose_name='Nombre')
    
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

    class Meta:
        app_label = 'base'
        db_table = 'base_persontypes'
        verbose_name = 'Tipo de Persona'
        verbose_name_plural = 'Tipos de Personas'
        ordering = ['name']


class DocumentType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=10)
    name = models.CharField(verbose_name='Nombre')
    person_type = models.ForeignKey('PersonType', verbose_name="Tipo de Persona", on_delete=models.CASCADE)

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

    class Meta:
        app_label = 'base'
        db_table = 'base_documenttypes'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['name']


class Applicant(models.Model):
    identification = models.CharField(verbose_name='Identificacíon', unique=True)
    name = models.CharField(verbose_name='Nombre')
    email = models.EmailField(verbose_name='Email', unique=True)
    phone_number = models.CharField(verbose_name='Teléfono', unique=True)
    state = models.ForeignKey('localization.State', verbose_name="Departamento", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('localization.City', verbose_name="Ciudad", null=True, blank=True, on_delete=models.SET_NULL)
    account = models.ForeignKey('account.Account', verbose_name="Cuenta", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    
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

    class Meta:
        app_label = 'base'
        db_table = 'base_applicants'
        verbose_name = 'Solicitante'
        verbose_name_plural = 'Solicitantes'
        ordering = ['name']


class Taker(models.Model):
    person_type = models.ForeignKey(PersonType, verbose_name="Tipo de Persona", on_delete=models.PROTECT, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, verbose_name="Tipo de Documento", on_delete=models.PROTECT, null=True, blank=True)
    identification = models.CharField(verbose_name='Identificacíon', unique=True)
    name = models.CharField(verbose_name='Nombre')
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Teléfono', null=True, blank=True)
    contact_name = models.CharField(verbose_name='Nombre Contacto', null=True, blank=True)
    address = models.CharField(verbose_name='Dirección', null=True, blank=True)
    state = models.ForeignKey('localization.State', verbose_name="Departamento", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('localization.City', verbose_name="Ciudad", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

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

    class Meta:
        app_label = 'base'
        db_table = 'base_takers'
        verbose_name = 'Tomador'
        verbose_name_plural = 'Tomadores'
        ordering = ['name']
    