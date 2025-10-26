from django_mongoengine import Document, fields, EmbeddedDocument
import datetime
import json

module_folder = 'modules/operative'


class RequestStatus(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(verbose_name='Nombre')

    meta = {
        'collection': 'operative_requeststatuses',
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
            with open(f'{module_folder}/scripts/data/requeststatuses.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            request_status = RequestStatus.objects.get(id=data["id"])
                        except RequestStatus.DoesNotExist:
                            request_status = RequestStatus()
                            request_status.id = data['id']
                            request_status.name = data['name']
                            request_status.save()

                            print (f'Estado de Solicitud {request_status} creado')

        except FileNotFoundError:
            pass


class RequestField(EmbeddedDocument):
    field = fields.ReferenceField('parameters.RamoField', verbose_name="Campo")
    value = fields.StringField(verbose_name='Valor')

    def __str__(self):
        return f"{self.field} - {self.value}"
    

class RequestDocument(EmbeddedDocument):
    document_name = fields.StringField(verbose_name='Nombre')
    document_title = fields.StringField(verbose_name='Título')
    filename = fields.StringField(verbose_name='Nombre Archivo')
    file_type = fields.StringField(verbose_name='Tipo Archivo')
    content = fields.StringField(verbose_name='Contenido Base64')

    def __str__(self):
        return f"{self.field} - {self.value}"
    

class OperativeRequest(Document):
    applicant = fields.ReferenceField('base.Applicant', verbose_name="Solicitante")
    taker = fields.ReferenceField('base.Taker', verbose_name="Tomador")
    ramo = fields.ReferenceField('parameters.Ramo', verbose_name="Ramo")
    number = fields.IntField(verbose_name='Número de Solicitud')
    value = fields.IntField(verbose_name='Valor')
    status = fields.ReferenceField(RequestStatus, verbose_name="Estado")
    assigned_to = fields.ReferenceField('auths.Account', verbose_name="Asignado a", null=True, blank=True)
    assigned_at = fields.DateTimeField(verbose_name="Fecha Asignación", null=True, blank=True)
    assigned_by = fields.StringField(verbose_name='Asignado por', max_length=50, null=True, blank=True)
    observations = fields.StringField(verbose_name='Observaciones', null=True, blank=True)
    request_fields = fields.ListField(
        fields.EmbeddedDocumentField(RequestField), blank=True,
    )
    request_documents = fields.ListField(
        fields.EmbeddedDocumentField(RequestDocument), blank=True,
    )
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'operative_requests',
        'ordering': ['number'],
        'indexes': [
            ('number',), 
        ]
    }
    
    def __str__(self):
        return f"{self.number}"
    
    @staticmethod
    def getNextNumber():
        next_number = 1
        request_list = OperativeRequest.objects().order_by('-number')
        if request_list.count() > 0:
            max_request = request_list.first()
            next_number = max_request.number + 1
        return next_number        

    @staticmethod
    def init_table():
        from modules.authentication.models import Account
        from modules.base.models import Applicant, Taker
        from modules.parameters.models import Ramo
        
        try:
            with open(f'{module_folder}/scripts/data/requests.json') as data_fp:
                data_list = json.load(data_fp)

                for data in data_list:
                    applicant = None
                    if 'applicant_email' in data.keys():
                        try:
                            applicant = Applicant.objects.get(email=data["applicant_email"])
                        except Applicant.DoesNotExist:
                            applicant = None

                    taker = None
                    if 'taker_identification' in data.keys():
                        try:
                            taker = Taker.objects.get(identification=data["taker_identification"])
                        except Taker.DoesNotExist:
                            taker = None

                    ramo = None
                    if 'ramo' in data.keys():
                        try:
                            ramo = Ramo.objects.get(id=data["ramo"])
                        except Ramo.DoesNotExist:
                            ramo = None

                    status = None
                    if 'status' in data.keys():
                        try:
                            status = RequestStatus.objects.get(id=data["status"])
                        except RequestStatus.DoesNotExist:
                            status = None

                    assigned_to = None
                    if 'assigned_to' in data.keys():
                        try:
                            assigned_to = Account.objects.get(id=data["assigned_to"])
                        except Account.DoesNotExist:
                            assigned_to = None

                    if status is not None and applicant is not None \
                        and taker is not None and ramo is not None \
                        and 'number' in data.keys() and 'value' in data.keys():

                        try:
                            operative_request = OperativeRequest.objects.get(number=data["number"])
                        except OperativeRequest.DoesNotExist:
                            operative_request = OperativeRequest()
                            operative_request.number = data['number']
                            operative_request.value = data['value']
                            operative_request.applicant = applicant
                            operative_request.taker = taker
                            operative_request.ramo = ramo
                            operative_request.status = status
                            operative_request.assigned_to = assigned_to
                            if assigned_to is not None:
                                operative_request.assigned_at = datetime.datetime.now()
                            operative_request.observations = data['observations']
                            
                            operative_request.request_fields = []
                            if 'fields' in data.keys():
                                for field_data in data['fields']:
                                    ramo_field = None
                                    if 'field' in field_data.keys():
                                        ramo_field_name = field_data["field"]
                                        ramo_field = None
                                        for ramo_field_item in ramo.ramo_fields:
                                            if ramo_field_item.name == ramo_field_name:
                                                ramo_field = ramo_field_item
                                                break

                                    if ramo_field is not None and 'value' in field_data.keys():
                                        value = field_data["value"]
                                        
                                        field:RequestField = RequestField()
                                        field.field = ramo_field
                                        field.value = value
                                    operative_request.request_fields.append(field)

                            operative_request.request_documents = []
                            if 'request_documents' in data.keys():
                                for request_documents_data in data['request_documents']:
                                    if 'document_name' in request_documents_data.keys() and \
                                       'filename' in request_documents_data.keys() and \
                                       'file_type' in request_documents_data.keys() and \
                                       'content' in request_documents_data.keys():

                                        request_document = RequestDocument()
                                        request_document.document_name = request_documents_data["document_name"]
                                        request_document.filename = request_documents_data["filename"]
                                        request_document.file_type = request_documents_data["file_type"]
                                        request_document.content = request_documents_data["content"]

                                    operative_request.request_documents.append(request_document)
                            
                            operative_request.created_at = datetime.datetime.now()
                            operative_request.save()

                            print (f'Solicitud {operative_request} creada')
        except FileNotFoundError:
            pass

class RequestEvent(Document):
    operative_request = fields.ReferenceField(OperativeRequest, verbose_name="Solicitud")
    status = fields.ReferenceField(RequestStatus, verbose_name="Estado")
    observations = fields.StringField(verbose_name='Observaciones', null=True, blank=True)
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'operative_requestevents',
        'ordering': ['created_at'],
        'indexes': [
            ('operative_request',), 
        ]
    }
    