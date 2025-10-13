from django_mongoengine import Document, fields, EmbeddedDocument
import datetime
import json

module_folder = 'modules/base'


class FieldType(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')

    meta = {
        'collection': 'base_fieldtypes',
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
            with open(f'{module_folder}/scripts/data/fieldtypes.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            field_type = FieldType.objects.get(id=data["id"])
                        except FieldType.DoesNotExist:
                            field_type = FieldType()
                            field_type.id = data['id']
                            field_type.name = data['name']
                            field_type.save()

                            print (f'Tipo de Campo {field_type} creada')

        except FileNotFoundError:
            pass



class FieldOption(EmbeddedDocument):
    name = fields.StringField(max_length=100, verbose_name='Nombre')


class RamoField(EmbeddedDocument):
    field_type = fields.ReferenceField(FieldType, verbose_name="Tipo de Campo")
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    mandatory = fields.BooleanField(verbose_name="Es Obligatorio", dafault=False)
    options = fields.ListField(
        fields.EmbeddedDocumentField('FieldOption'), blank=True,
    )


class AvailableDocument(EmbeddedDocument):
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    mandatory = fields.BooleanField(verbose_name="Es Obligatorio", dafault=False)


class Ramo(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=20)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    ramo_fields = fields.ListField(
        fields.EmbeddedDocumentField(RamoField), blank=True,
    )
    available_documents = fields.ListField(
        fields.EmbeddedDocumentField(AvailableDocument), blank=True,
    )
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'base_ramos',
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
            with open(f'{module_folder}/scripts/data/ramos.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    import pdb; pdb.set_trace()
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            ramo = Ramo.objects.get(id=data["id"])
                        except Ramo.DoesNotExist:
                            ramo = Ramo()
                            ramo.id = data['id']
                            ramo.name = data['name']
                            ramo.ramo_fields = []
                            if 'fields' in data.keys():
                                for field_data in data['fields']:
                                    field_type = None
                                    if 'field_type' in field_data.keys():
                                        field_type_id = field_data["field_type"]
                                        try:
                                            field_type = FieldType.objects.get(pk=field_type_id)
                                        except FieldType.DoesNotExist:
                                            print (f"Tipo de Campo {field_type} no Existe")
                                            field_type = None

                                    if field_type is not None and 'name' in field_data.keys():
                                        name = field_data["name"]
                                        mandatory = False
                                        if 'mandatory' in field_data.keys():
                                            mandatory = field_data["mandatory"]
                                        
                                        field = RamoField()
                                        field.field_type = field_type
                                        field.name = name
                                        field.mandatory = mandatory
                                        options = []
                                        if 'options' in field_data.keys():
                                            options = field_data["options"]
                                        field.options = options
                                    ramo.ramo_fields.append(field)
                            ramo.available_documents = []
                            if 'available_documents' in data.keys():
                                for available_documents_data in data['available_documents']:
                                    if 'name' in available_documents_data.keys():
                                        name = available_documents_data["name"]
                                        mandatory = False
                                        if 'mandatory' in available_documents_data.keys():
                                            mandatory = available_documents_data["mandatory"]
                                        
                                        available_document = AvailableDocument()
                                        available_document.name = name
                                        available_document.mandatory = mandatory
                                    ramo.available_documents.append(available_document)
                            
                            ramo.created_at = datetime.datetime.now()
                            ramo.save()

                            print (f'Ramo {ramo} creada')

        except FileNotFoundError:
            pass
