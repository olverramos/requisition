from django_mongoengine import Document, fields, EmbeddedDocument
from modules.parameters.models import DocumentClass
from core.templatetags.tools import currency
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
        try:
            return f"{self.field.name}: {self.value}"
        except:
            return f"{self.value}"
    

class RequestDocument(EmbeddedDocument):
    document_name = fields.StringField(verbose_name='Nombre')
    document_title = fields.StringField(verbose_name='Título')
    filename = fields.StringField(verbose_name='Nombre Archivo')
    file_type = fields.StringField(verbose_name='Tipo Archivo')
    content = fields.StringField(verbose_name='Contenido Base64')

    def __str__(self):
        return f"{self.document_name} - {self.filename}"


class OperativeRequestDocument(Document):
    operative_request = fields.ReferenceField('OperativeRequest', verbose_name="Solicitud")
    document_class = fields.ReferenceField('parameters.DocumentClass', verbose_name="Clase de Documento")
    title = fields.StringField(verbose_name='Título')
    filename = fields.StringField(verbose_name='Nombre Archivo')
    file_type = fields.StringField(verbose_name='Tipo Archivo')
    content = fields.StringField(verbose_name='Contenido Base64')
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Actualizado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'operative_requestdocuments',
       # 'ordering': ['operative_request', 'document_class'],
    }
    
    def __str__(self):
        return f"{self.operative_request} - {self.document_class} - {self.filename}"
    

class RequestFile(EmbeddedDocument):
    filename = fields.StringField(verbose_name='Nombre Archivo')
    file_type = fields.StringField(verbose_name='Tipo Archivo')
    content = fields.StringField(verbose_name='Contenido Base64')

    def __str__(self):
        return f"{self.filename}"


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
    values_fields = fields.StringField(verbose_name='Valores de Campos', max_length=50, null=True, blank=True)
    ###### Cambio
    request_documents = fields.ListField(
        fields.EmbeddedDocumentField(RequestDocument), blank=True,
    )
    request_receipt = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    request_rc_receipt = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    request_police = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    request_rc_police = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    payment_receipt = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    payment_rc_receipt = fields.EmbeddedDocumentField(RequestFile, null=True, blank=True)
    ###### Cambio
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Actualizado por', max_length=50, null=True, blank=True)
    validated_at = fields.DateTimeField(verbose_name="Fecha Validación", null=True, blank=True)
    validated_by = fields.StringField(verbose_name='Validado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'operative_requests',
        'ordering': ['number'],
        'indexes': [
            ('number',), 
        ]
    }
    
    @staticmethod
    def fix_values():
        operative_request_list = OperativeRequest.objects.all()
        for operative_request in operative_request_list:
            values_fields = []
            for request_field in operative_request.request_fields:
                request_field.value = request_field.value.replace('"', '"')
                values_fields.append(request_field.value)
            operative_request.values_fields = '|'.join(values_fields)
            operative_request.save()

    @staticmethod
    def fix_documents():
        operative_request_document_list = OperativeRequestDocument.objects.all()
        for operative_request_document in operative_request_document_list:
            document_class = DocumentClass.objects.get(id=operative_request_document.document_class.id)
            operative_request_document.title = document_class.name
            operative_request_document.save()


    @staticmethod
    def migrate_documents():
        operative_request_list = OperativeRequest.objects.all()
        for operative_request in operative_request_list:
            for document in operative_request.request_documents:

                document_class = DocumentClass.objects.get(id=document.document_name)

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = document.document_title
                operative_request_document.filename = document.filename
                operative_request_document.file_type = document.file_type
                operative_request_document.content = document.content
                operative_request_document.save()

            if operative_request.request_receipt:

                document_class = DocumentClass.objects.get(id='request_receipt')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Recibo de Pago'
                operative_request_document.filename = operative_request.request_receipt.filename
                operative_request_document.file_type = operative_request.request_receipt.file_type
                operative_request_document.content = operative_request.request_receipt.content
                operative_request_document.save()

            if operative_request.request_rc_receipt:
                document_class = DocumentClass.objects.get(id='request_rc_receipt')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Recibo de Pago RC'
                operative_request_document.filename = operative_request.request_rc_receipt.filename
                operative_request_document.file_type = operative_request.request_rc_receipt.file_type
                operative_request_document.content = operative_request.request_rc_receipt.content
                operative_request_document.save()

            if operative_request.request_police:
                document_class = DocumentClass.objects.get(id='request_police')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Poliza'
                operative_request_document.filename = operative_request.request_police.filename
                operative_request_document.file_type = operative_request.request_police.file_type
                operative_request_document.content = operative_request.request_police.content
                operative_request_document.save()

            if operative_request.request_rc_police:
                document_class = DocumentClass.objects.get(id='request_rc_police')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Poliza RC'
                operative_request_document.filename = operative_request.request_rc_police.filename
                operative_request_document.file_type = operative_request.request_rc_police.file_type
                operative_request_document.content = operative_request.request_rc_police.content
                operative_request_document.save()

            if operative_request.payment_receipt:
                document_class = DocumentClass.objects.get(id='payment_receipt')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Comprobante de Pago'
                operative_request_document.filename = operative_request.payment_receipt.filename
                operative_request_document.file_type = operative_request.payment_receipt.file_type
                operative_request_document.content = operative_request.payment_receipt.content
                operative_request_document.save()

            if operative_request.payment_rc_receipt:
                document_class = DocumentClass.objects.get(id='payment_rc_receipt')

                operative_request_document = OperativeRequestDocument()
                operative_request_document.operative_request = operative_request
                operative_request_document.document_class = document_class
                operative_request_document.title = 'Comprobante de Pago RC'
                operative_request_document.filename = operative_request.payment_rc_receipt.filename
                operative_request_document.file_type = operative_request.payment_rc_receipt.file_type
                operative_request_document.content = operative_request.payment_rc_receipt.content
                operative_request_document.save()

    def __str__(self):
        return f"{self.number} - {self.taker}"
    
    @staticmethod
    def getNextNumber():
        next_number = 1
        request_list = OperativeRequest.objects().order_by('-number')
        if request_list.count() > 0:
            max_request = request_list.first()
            next_number = max_request.number + 1
        return next_number        

    @staticmethod
    def update_status():
        operative_request_list = OperativeRequest.objects.all()
        operative_request_status = None

        police_document_class_list = DocumentClass.objects.filter(document_type='POLICE')
        receipt_document_class_list = DocumentClass.objects.filter(document_type='RECEIPT')
        payment_document_class_list = DocumentClass.objects.filter(document_type='PAYMENT')

        for operative_request in operative_request_list:
            document_list = OperativeRequestDocument.objects.filter(operative_request=operative_request)
            police_document_list = document_list.filter(document_class__in=police_document_class_list)
            receipt_document_list = document_list.filter(document_class__in=receipt_document_class_list)
            payment_document_list = document_list.filter(document_class__in=payment_document_class_list)

            if police_document_list.count() > 0:
                operative_request_status = RequestStatus.objects.get(id='3')
            if receipt_document_list.count() > 0:
                operative_request_status = RequestStatus.objects.get(id='3')
            if payment_document_list.count() > 0:
                operative_request_status = RequestStatus.objects.get(id='4')
            if operative_request_status is not None and operative_request.status.id < operative_request_status.id:
                operative_request.status = operative_request_status
                operative_request.save()

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


    def query(self):
        request_data = {}
        request_data['id'] = str(self.id)
        request_data['number'] = self.number

        request_data['applicant_phone_number'] = str(self.applicant.phone_number)
        request_data['applicant_name'] = str(self.applicant)

        request_data['taker_person_type_id'] = str(self.taker.person_type.id)
        request_data['taker_person_type'] = str(self.taker.person_type)
        request_data['taker_document_type_id'] = str(self.taker.document_type.id)
        request_data['taker_document_type'] = str(self.taker.document_type)
        request_data['taker_identification'] = str(self.taker.identification)
        request_data['taker_name'] = str(self.taker.name)
        request_data['taker_phone_number'] = str(self.taker.phone_number)
        request_data['taker_contact_name'] = str(self.taker.contact_name)
        
        request_data['ramo_id'] = str(self.ramo.id)
        request_data['ramo'] = str(self.ramo)
        
        request_data['status_id'] = str(self.status.id)
        request_data['status'] = str(self.status)
        request_data['value'] = currency(self.value)
        request_data['assigned_to'] = str(self.assigned_to) if self.assigned_to else ''
        request_data['assigned_to_id'] = str(self.assigned_to.id) if self.assigned_to else ''
        request_data['assigned_at'] = self.assigned_at.strftime("%Y-%m-%d %H:%M") if self.assigned_at else ''
        request_data['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else ''
        request_data['created_by'] = self.created_by if self.created_by else ''
        request_data['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M") if self.updated_at else ''
        request_data['updated_by'] = self.updated_by if self.updated_by else ''
        request_data['validated_at'] = self.validated_at.strftime("%Y-%m-%d %H:%M") if self.validated_at else ''
        request_data['validated_by'] = self.validated_by if self.validated_by else ''
        request_data['request_receipt'] = None
        if self.request_receipt is not None:
            request_data['request_receipt'] = {
                'filename': self.request_receipt.filename,
                'file_type': self.request_receipt.file_type,
                'content': self.request_receipt.content,
            }
        request_data['request_rc_receipt'] = None
        if self.request_rc_receipt is not None:
            request_data['request_rc_receipt'] = {
                'filename': self.request_rc_receipt.filename,
                'file_type': self.request_rc_receipt.file_type,
                'content': self.request_rc_receipt.content,
            }
        request_data['request_police'] = None
        if self.request_police is not None:
            request_data['request_police'] = {
                'filename': self.request_police.filename,
                'file_type': self.request_police.file_type,
                'content': self.request_police.content,
            }
        request_data['request_rc_police'] = None
        if self.request_rc_police is not None:
            request_data['request_rc_police'] = {
                'filename': self.request_rc_police.filename,
                'file_type': self.request_rc_police.file_type,
                'content': self.request_rc_police.content,
            }
        request_data['payment_receipt'] = None
        if self.payment_receipt is not None:
            request_data['payment_receipt'] = {
                'filename': self.payment_receipt.filename,
                'file_type': self.payment_receipt.file_type,
                'content': self.payment_receipt.content,
            }
        request_data['payment_rc_receipt'] = None
        if self.payment_rc_receipt is not None:
            request_data['payment_rc_receipt'] = {
                'filename': self.payment_rc_receipt.filename,
                'file_type': self.payment_rc_receipt.file_type,
                'content': self.payment_rc_receipt.content,
            }

        request_data['observations'] = self.observations if self.observations else ''

        request_data['fields'] = {}
        for request_field in self.request_fields:
            try:
                request_data['fields'][str(request_field.field.name)] = {
                    'value': request_field.value,
                    'field': request_field.field,
                }
            except:
                pass
        request_data['documents'] = {}
        
        for document_field in self.request_documents:
            request_data['documents'][str(document_field.document_name)] = {
                'document_name': document_field.document_name,
                'document_title': document_field.document_title,
                'filename': document_field.filename,
                'file_type': document_field.file_type,
                'content': document_field.content,
            }

        return request_data

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
    